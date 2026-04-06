"""
Camping Trip Planner Tools
--------------------------
Tool 1: search_camping_sites      - DeepSeek knowledge base
Tool 2: get_weather_forecast       - Open-Meteo API (free, no key needed)
Tool 3: get_travel_and_gear_recommendations - DeepSeek reasoning
"""

import os
import re
import requests
from datetime import datetime, timedelta


# ─── Internal helper: call DeepSeek directly ─────────────────────────────────

def _ask_llm(system: str, user: str) -> str:
    """Lightweight DeepSeek call used internally by tools."""
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )
    resp = client.chat.completions.create(
        model=os.getenv("DEFAULT_MODEL", "deepseek-chat"),
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()


# ─── WMO weather code → Vietnamese description ───────────────────────────────

_WMO_CODES = {
    0: "Troi quang dang", 1: "Chu yeu quang dang", 2: "Co may mot phan",
    3: "May mu", 45: "Suong mu", 48: "Suong mu dong gia",
    51: "Mua phun nhe", 53: "Mua phun vua", 55: "Mua phun day",
    61: "Mua nhe", 63: "Mua vua", 65: "Mua to",
    80: "Mua rao nhe", 81: "Mua rao vua", 82: "Mua rao manh",
    95: "Co dong", 96: "Co dong co mua da nho", 99: "Co dong co mua da lon",
}

def _wmo_to_vi(code: int) -> str:
    return _WMO_CODES.get(code, f"Ma thoi tiet: {code}")


# ─── Tool 1: search_camping_sites ─────────────────────────────────────────────

def search_camping_sites(query: str) -> str:
    """
    Tim kiem dia diem cam trai phu hop.
    query vi du: 'Gia Lam, Ha Noi, 4 nguoi'
                 'Ba Vi, Ha Noi, gia dinh 6 nguoi'
    """
    system = """Bạn là chuyên gia du lịch dã ngoại Việt Nam với kiến thức sâu về các điểm cắm trại thực tế.
Nhiệm vụ: Gợi ý 3 địa điểm cắm trại THỰC TẾ CÓ TỒN TẠI tại Việt Nam dựa trên yêu cầu của người dùng.

Mỗi địa điểm PHẢI có đủ:
- Tên đầy đủ và địa chỉ cụ thể
- Khoảng cách và thời gian di chuyển từ điểm xuất phát
- Mô tả cảnh quan và tiện ích (có khu vui chơi trẻ em? có cho thuê lều? có BBQ?)
- Đánh giá phù hợp gia đình: Rất phù hợp / Phù hợp / Chấp nhận được
- Lưu ý quan trọng (đặt trước, phí vào cửa, v.v.)

Chỉ gợi ý địa điểm trong bán kính hợp lý và PHÙ HỢP với số người yêu cầu.
Trả lời bằng tiếng Việt, rõ ràng, có thể đọc qua Telegram."""

    result = _ask_llm(system, f"Tìm địa điểm cắm trại: {query}")
    return f"[KẾT QUẢ TÌM KIẾM ĐỊA ĐIỂM]\n{result}"


# ─── Tool 2: get_weather_forecast ─────────────────────────────────────────────

def get_weather_forecast(query: str) -> str:
    """
    Lay du bao thoi tiet cho dia diem va ngay cu the.
    query vi du: 'Gia Lam, Ha Noi, ngay 30/04'
                 'Ba Vi, Ha Noi, 1/5/2026'
    """
    # --- Parse date from query ---
    date_match = re.search(r"(\d{1,2})[/\-\.](\d{1,2})(?:[/\-\.](\d{4}))?", query)
    target_date = None
    date_str_display = ""

    if date_match:
        day   = int(date_match.group(1))
        month = int(date_match.group(2))
        year  = int(date_match.group(3)) if date_match.group(3) else datetime.now().year
        try:
            target_date = datetime(year, month, day)
            date_str_display = target_date.strftime("%d/%m/%Y")
        except ValueError:
            pass

    if not target_date:
        target_date = datetime.now() + timedelta(days=1)
        date_str_display = target_date.strftime("%d/%m/%Y")

    # --- Extract location (remove date part) ---
    location_raw = re.sub(r"[\,\s]*(ngay|ngày|date)?[\s]*\d{1,2}[/\-\.]\d{1,2}([/\-\.]\d{4})?", "", query, flags=re.IGNORECASE).strip().strip(",").strip()
    if not location_raw:
        location_raw = "Ha Noi"

    days_ahead = (target_date - datetime.now()).days

    # --- Geocoding via Open-Meteo ---
    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_resp = requests.get(geo_url, params={
            "name": location_raw, "count": 1, "language": "vi", "format": "json"
        }, timeout=8)
        geo_data = geo_resp.json()

        if not geo_data.get("results"):
            # Fallback: try with simplified name
            simplified = re.sub(r"(quận|huyện|thị xã|thành phố|tỉnh|phường|xã)", "", location_raw, flags=re.IGNORECASE).strip()
            geo_resp = requests.get(geo_url, params={
                "name": simplified, "count": 1, "language": "vi", "format": "json"
            }, timeout=8)
            geo_data = geo_resp.json()

        if not geo_data.get("results"):
            raise ValueError(f"Không tìm thấy tọa độ cho '{location_raw}'")

        geo = geo_data["results"][0]
        lat, lon = geo["latitude"], geo["longitude"]
        place_name = geo.get("name", location_raw)

    except Exception as e:
        return _weather_llm_fallback(location_raw, date_str_display, str(e))

    # --- Weather Forecast via Open-Meteo (up to 16 days) ---
    if 0 <= days_ahead <= 16:
        try:
            wx_url = "https://api.open-meteo.com/v1/forecast"
            wx_resp = requests.get(wx_url, params={
                "latitude": lat, "longitude": lon,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode,windspeed_10m_max",
                "timezone": "Asia/Bangkok",
                "forecast_days": min(days_ahead + 1, 16),
            }, timeout=10)
            wx_data = wx_resp.json()

            daily = wx_data.get("daily", {})
            dates = daily.get("time", [])
            target_str = target_date.strftime("%Y-%m-%d")

            if target_str in dates:
                idx = dates.index(target_str)
                tmax  = daily["temperature_2m_max"][idx]
                tmin  = daily["temperature_2m_min"][idx]
                rain  = daily["precipitation_sum"][idx]
                code  = daily["weathercode"][idx]
                wind  = daily["windspeed_10m_max"][idx]

                rain_note = "Khong mua" if rain < 1 else f"Mua {rain:.1f}mm"
                outdoor_ok = "RAT LY TUONG de cam trai!" if rain < 1 and tmax < 36 else \
                             "Nen chuan bi ao mua" if rain >= 1 else "Qua nong, chon bong mat"

                return (
                    f"[DU BAO THOI TIET THUC TE - Open-Meteo]\n"
                    f"Dia diem: {place_name} ({lat:.2f}, {lon:.2f})\n"
                    f"Ngay: {date_str_display}\n"
                    f"Tinh trang: {_wmo_to_vi(int(code))}\n"
                    f"Nhiet do: {tmin:.0f}°C (dem) - {tmax:.0f}°C (ngay)\n"
                    f"Luong mua: {rain_note}\n"
                    f"Gio manh nhat: {wind:.0f} km/h\n"
                    f"Danh gia: {outdoor_ok}"
                )
            else:
                return _weather_llm_fallback(
                    location_raw, date_str_display,
                    f"Ngay {date_str_display} vuot ngoai du bao 16 ngay cua Open-Meteo"
                )

        except Exception as e:
            return _weather_llm_fallback(location_raw, date_str_display, str(e))
    else:
        return _weather_llm_fallback(
            location_raw, date_str_display,
            f"Ngay {date_str_display} con {days_ahead} ngay nua — vuot kha nang du bao 16 ngay"
        )


def _weather_llm_fallback(location: str, date_str: str, reason: str) -> str:
    """LLM reasoning fallback when Open-Meteo can't cover the date."""
    system = """Bạn là chuyên gia khí hậu Việt Nam.
Dựa trên dữ liệu lịch sử thời tiết, hãy dự đoán thời tiết theo mùa cho địa điểm và ngày được yêu cầu.
Nêu rõ đây là ước tính theo lịch sử khí hậu, không phải dự báo thực tế.
Bao gồm: nhiệt độ trung bình, khả năng mưa, độ ẩm, lời khuyên cho cắm trại."""
    result = _ask_llm(system, f"Thời tiết tại {location} vào ngày {date_str}?")
    return (
        f"[DU BAO THEO LICH SU KHI HAU - LLM Reasoning]\n"
        f"(Ly do: {reason})\n"
        f"{result}"
    )


# ─── Tool 3: get_travel_and_gear_recommendations ──────────────────────────────

def get_travel_and_gear_recommendations(query: str) -> str:
    """
    Goi y phuong tien, gio xuat phat va danh sach dung cu cam trai.
    query vi du: 'tu Ha Noi den Gia Lam, ngay le 30/4, gia dinh 4 nguoi'
    """
    system = """Bạn là chuyên gia tư vấn du lịch dã ngoại gia đình tại Việt Nam.
Cung cấp kế hoạch di chuyển và danh sách đồ dùng CỤ THỂ, THỰC TẾ.

Phần 1 - PHƯƠNG TIỆN & THỜI GIAN:
- Phương tiện phù hợp nhất (lý do)
- Thời gian di chuyển ước tính
- Lưu ý đặc biệt (tắc đường, bãi đỗ xe, v.v.)

Phần 2 - KHUNG GIỜ XUẤT PHÁT (quan trọng):
- Nếu ngày lễ/cuối tuần: cảnh báo điểm tắc, giờ vàng để đi
- Khuyến nghị đi sớm hay tối nhất
- Giờ về lý tưởng

Phần 3 - DANH SÁCH DỤNG CỤ (đầy đủ, theo nhóm):
Chia rõ: Nơi ở | Ăn uống | Chiều sáng | An toàn & Y tế | Giải trí

Trả lời bằng tiếng Việt, cụ thể, có thể thực hiện ngay."""

    result = _ask_llm(system, f"Lập kế hoạch di chuyển và chuẩn bị đồ: {query}")
    return f"[KE HOACH DI CHUYEN & DUNG CU]\n{result}"


# ─── Tool Registry ────────────────────────────────────────────────────────────

CAMPING_TOOL_REGISTRY = {
    "search_camping_sites": {
        "name": "search_camping_sites",
        "description": (
            "Tim kiem dia diem cam trai phu hop gan mot khu vuc tai Viet Nam. "
            "Input: mo ta yeu cau, vi du 'Gia Lam, Ha Noi, 4 nguoi' hoac 'Ba Vi, gia dinh 6 nguoi'. "
            "Tra ve 3 dia diem cu the, co dia chi that, mo ta tien ich va muc do phu hop gia dinh. "
            "PHAI goi tool nay dau tien de tim dia diem truoc khi kiem tra thoi tiet."
        ),
        "function": search_camping_sites,
    },
    "get_weather_forecast": {
        "name": "get_weather_forecast",
        "description": (
            "Lay du bao thoi tiet thuc te cho mot dia diem va ngay cu the. "
            "Input: 'ten dia diem, ngay DD/MM' vi du 'Gia Lam Ha Noi, ngay 30/04'. "
            "Su dung Open-Meteo API cho data thuc te (16 ngay), fallback sang LLM neu xa hon. "
            "Goi tool nay sau search_camping_sites de biet thoi tiet co thuan loi khong."
        ),
        "function": get_weather_forecast,
    },
    "get_travel_and_gear_recommendations": {
        "name": "get_travel_and_gear_recommendations",
        "description": (
            "Goi y phuong tien di chuyen, cac khung gio xuat phat hop ly va danh sach dung cu cam trai day du. "
            "Input: mo ta hanh trinh, vi du 'tu trung tam Ha Noi den Gia Lam, ngay le 30/4, gia dinh 4 nguoi'. "
            "Goi tool nay sau get_weather_forecast, day la buoc cuoi truoc khi tong hop ke hoach."
        ),
        "function": get_travel_and_gear_recommendations,
    },
}


def get_camping_tools() -> list:
    """Return list of camping tools."""
    return list(CAMPING_TOOL_REGISTRY.values())
