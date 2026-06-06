import os
from dotenv import load_dotenv
from openai import OpenAI
from hindsight import HindsightClient

load_dotenv()

# Verify API Keys
if not os.getenv("GROQ_API_KEY") or not os.getenv("HINDSIGHT_API_KEY"):
    raise ValueError("Missing API Keys! Please check your .env file.")

# Initialize Groq client using OpenAI SDK compatibility wrapper
groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# Recommended model for fast agent loops
MODEL_NAME = "qwen-2.5-coder-32b" # Or "gpt-4o-mini" / "qwen/qwen3-32b" depending on your provider mappings

# Initialize Hindsight memory layer
hindsight = HindsightClient(api_key=os.getenv("HINDSIGHT_API_KEY"))