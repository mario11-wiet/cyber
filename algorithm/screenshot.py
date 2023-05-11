import os
import re
import time

from pyppeteer import launch

from algorithm.const import PATH, PNG, DAY, WIDTH, HEIGHT


async def take_screenshot(url, screenshot_path):
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': WIDTH, 'height': HEIGHT})
    await page.goto(url)
    await page.screenshot({'path': screenshot_path})
    await browser.close()


async def screenshot(url):
    screenshot_path = PATH + re.sub(r'[^\w\s]', '', url) + PNG
    if os.path.exists(screenshot_path):
        created_time = os.path.getctime(screenshot_path)
        if time.time() - created_time > DAY:
            await take_screenshot(url, screenshot_path)
        return screenshot_path

    await take_screenshot(url, screenshot_path)
    return screenshot_path
