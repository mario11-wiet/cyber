import asyncio
import aiohttp

from algorithm.const import TIMEOUT
from algorithm.decorator import url_parse
from algorithm.dominant_color import dominant_color
from algorithm.screenshot import screenshot


@url_parse
async def website_dominant_color(queue, url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=TIMEOUT) as response:
                if response.status == 200:
                    screenshot_url = await screenshot(url)
                    dominant = dominant_color(screenshot_url)
                    response_ = {"output": dominant, "status_code": response.status}
                    queue.put(response_)

                else:
                    response_ = {"output": "Website does not exist or is not accessible",
                                 "status_code": response.status}
                    queue.put(response_)
        except aiohttp.ClientError:
            response_ = {"output": "",
                         "status_code": 400}
            queue.put(response_)
        except asyncio.exceptions.TimeoutError:
            response_ = {"output": "",
                         "status_code": 504}
            queue.put(response_)
