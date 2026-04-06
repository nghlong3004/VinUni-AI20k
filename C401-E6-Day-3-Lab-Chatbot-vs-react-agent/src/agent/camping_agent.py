import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(project_root))

from core.gemini_provider import GeminiProvider
from agent import ReActAgent
from tools.location_tools import search_camp_site 
from tools.weather_tools import get_weather_forecast
from tools.get_travel_and_gear_recommendations_tool import get_travel_and_gear_recommendations

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 1. Định nghĩa Tool theo chuẩn để Agent hiểu được
tool_search_camp = {
    "name": "search_camp_site",
    "description": (
        "Tìm kiếm các địa điểm cắm trại, công viên gần một khu vực cụ thể. "
        "YÊU CẦU ĐẦU VÀO LÀ JSON có cấu trúc: "
        '{"location": "<chuỗi địa chỉ, vd: Gia Lam, Ha Noi>", '
        '"radius_km": <số thực, khoảng cách tối đa, vd: 15.0>, '
        '"capacity": <số nguyên, số người tham gia, vd: 4>, '
        '"amenities": <danh sách chuỗi, vd: ["family_friendly"]>}'
    ),
    "func": search_camp_site  # Trỏ trực tiếp đến hàm Python của bạn
}

tool_get_weather = {
    "name": "get_weather_forecast",
    "description": (
        "Get weather forecast from WeatherAPI for a specific location and date. "
        "YÊU CẦU ĐẦU VÀO LÀ JSON có cấu trúc: "
        '{"location": "<chuỗi địa chỉ, vd: Gia Lam, Ha Noi>", '
        '"date": <ngày tháng >, '
    ),
    "func": get_weather_forecast  # Trỏ trực tiếp đến hàm Python của bạn
}

tool_get_travel_and_gear_recommendations = {
    "name": "get_travel_and_gear_recommendations",
    "description": (
        "Combine campsite search and weather forecast into one structured recommendation."
        "This tool does not fabricate live data: it relies on the outputs of"
        "search_camp_site(...) and get_weather_forecast(...)."
    ),
    "func": get_travel_and_gear_recommendations
}

my_tools = [tool_search_camp, tool_get_weather, tool_get_travel_and_gear_recommendations]

# 2. Khởi tạo LLM và Agent
# os.environ.get("PLACES_API_KEY")
# os.environ.get("WEATHER_API_KEY")

script_root = Path(__file__).resolve().parent.parent.parent / "scripts"
sys.path.insert(0, str(script_root))

from evaluate_chatbot_limitations import build_provider

def get_camping_agent() -> ReActAgent:
    """Tạo và trả về ReActAgent đã được cấu hình với LLM và tools."""
    provider_name = os.environ.get("DEFAULT_PROVIDER", "gemini")
    # Sử dụng hàm build_provider để tự động chọn LLM theo file .env (hỗ trợ deepseek)
    llm = build_provider(provider_override=provider_name)
    return ReActAgent(llm=llm, tools=my_tools)

if __name__ == "__main__":
    agent = get_camping_agent()

    # 3. Chạy Agent
    user_prompt = "Tôi muốn 6/4 này đi cắm trại ở đâu đó quanh HN, gần gia lâm thì tốt cho gia đình 4 người. Tôi nên chuẩn bị đồ đạc gì?"
    final_answer = agent.run(user_prompt)

    print("\n=== KẾT QUẢ CUỐI CÙNG ===")
    print(final_answer)