import logging
import threading

import lemapp

from sklounst import queue

logger = logging.getLogger(__name__)

g_lock = threading.Lock()
g_counter = 0


def handler(channel, method, _, body):
    global g_lock, g_counter
    with g_lock:
        g_counter += 1
        counter = g_counter
    if counter % 100 == 0:
        logger.info('Got %s', body)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main(_):
    channel = queue.get_channel()
    queue.subscribe(channel, handler)
    channel.start_consuming()


if __name__ == '__main__':
    lemapp.App().run()
