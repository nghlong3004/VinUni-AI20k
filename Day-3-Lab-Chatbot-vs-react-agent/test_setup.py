"""Test the Camping Trip Planner Agent end-to-end."""
import os, sys
sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")  # fix Windows cp1252
from dotenv import load_dotenv
load_dotenv()

from src.core.deepseek_provider import DeepSeekProvider
from src.agent.camping_agent import CampingAgent

llm = DeepSeekProvider(
    model_name=os.getenv("DEFAULT_MODEL", "deepseek-chat"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)
agent = CampingAgent(llm=llm)

question = "Toi muon 30/4 nay di cam trai o dau do quanh Ha Noi, gan Gia Lam, gia dinh 4 nguoi. Cho toi biet dia diem, thoi tiet, phuong tien va dung cu can chuan bi."

print("USER:", question)
print("=" * 60)
answer = agent.run(question)
print("\nCAMPBOT ANSWER:")
print(answer)
