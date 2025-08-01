
from openai import AsyncOpenAI
import asyncio
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
import os
from dotenv import load_dotenv


load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is too much best for the Pakistani people. It is a sunny day with a temperature of 25 degrees Celsius."

# weather_agent = Agent(
#     name="weather_Assistant",
#     instructions="You are a weather assistant provide the information of weather to user..",
#     model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
#     tools=[get_weather]
# )
triage_agent= Agent(
    name="Assistant",
    instructions="""You are a assistant of user provide the user which he demand if the user ask about weather hands off the task to weather agent..""",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    # handoffs=[weather_agent]
)
async def main():
    while True:
        query = input("Enter the query: ")
        if query.lower() == "exit":
            break
        result = await Runner.run(triage_agent, query)
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())