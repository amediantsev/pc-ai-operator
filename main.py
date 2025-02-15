import asyncio
import pyperclip
from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext
from browser_use.agent.views import ActionResult
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    )
)
controller = Controller()


@controller.registry.action('Copy text to clipboard')
def copy_to_clipboard(text: str):
    pyperclip.copy(text)
    return ActionResult(extracted_content=text)


@controller.registry.action('Paste text from clipboard')
async def paste_from_clipboard(browser: BrowserContext):
    text = pyperclip.paste()
    # send text to browser
    page = await browser.get_current_page()
    await page.keyboard.type(text)

    return ActionResult(extracted_content=text)


async def main():
    agent = Agent(
        task=(
            "1. Search for the images in google by the query 'картинка - мила киця на унітазі', "
            " choose the funniest one (ignore TikTok, YouTube and any other videos, please),"
            " and copy the image link to clipboard. DON'T FOLLOW ANY LINKS THERE!;\n"
            "2. Go to 'https://web.telegram.org', find the chat 'Saved Messages',"
            " select it, and close the left side bar (with arrow icon);"
            "3. Click to the 'Message' text area (bottom of the selected chat section),"
            " paste the copied url from clipboard to there (not the 'Search' section!),"
            " type there (not the 'Search' section!) the additional text 'Це - ти)))', and send the message."
        ),
        llm=ChatOpenAI(model="gpt-4o-mini"),
        browser=browser,
        controller=controller,
    )
    result = await agent.run()
    print(result)

    input('Press Enter to close the browser...')
    await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
