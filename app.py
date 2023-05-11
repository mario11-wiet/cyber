from flask import Flask, jsonify, request
import asyncio
from multiprocessing import Process, Queue
from algorithm.website_dominat_color import website_dominant_color

app = Flask(__name__)


async def async_website_dominant_color(queue, url):
    await website_dominant_color(queue, url)


@app.route('/', methods=['GET'])
def color_dominate():
    queue = Queue()
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No url argument provided'}), 400
    p = Process(target=run_async_, args=(queue, url))
    p.start()
    p.join()
    response = queue.get()

    if response['status_code'] != 200:
        return jsonify({'error': response["output"]}), response['status_code']
    return jsonify(response["output"]), 200


def run_async_(queue, url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_website_dominant_color(queue, url))
    loop.close()


if __name__ == '__main__':
    app.run()
