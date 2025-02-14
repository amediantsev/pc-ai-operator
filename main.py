import asyncio
from browser_use import Agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


async def main():
    agent = Agent(
        task="Go to Reddit, search for 'browser-use', click on the first post and return the first comment.",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
