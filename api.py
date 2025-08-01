import asyncio
import os
from typing import Optional

from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from pydantic import BaseModel

load_dotenv()

# API Configuration
API_KEY = os.getenv("API_KEY", "your-secret-api-key-here")  # Set this in your .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI(
    title="Agent API", description="Backend API for AI Agent", version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    message: str


# API Key authentication
async def verify_api_key(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


# Function tools
@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is too much best for the Pakistani people. It is a sunny day with a temperature of 25 degrees Celsius."


Initialize agents
weather_agent = Agent(
    name="weather_Assistant",
    instructions="You are a weather assistant provide the information of weather to user..",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[get_weather],
)

triage_agent = Agent(
    name="Assistant",
    instructions="""You are a assistant of user provide the user which he demand if the user ask about weather hands off the task to weather agent. if the user enter a random word then you should say that you are not able to understand the user's demand.""",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    handoffs=[weather_agent],
)


# API Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(status="healthy", message="Agent API is running")


@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    """Chat with the AI agent"""
    try:
        result = await Runner.run(triage_agent, request.message)
        return ChatResponse(response=result.final_output, success=True)
    except Exception as e:
        return ChatResponse(response="", success=False, error=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy", message="API is operational")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
