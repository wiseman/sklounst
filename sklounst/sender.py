"""Sends SBS-1 messages to the queue."""

from __future__ import print_function
import logging
import sys

import gflags
import lemapp
import pika

from sklounst import queue

FLAGS = gflags.FLAGS
logger = logging.getLogger(__name__)


def main(argv):
    "Runs."
    channel = queue.get_channel()
    if len(argv) > 1:
        num_messages = int(argv[1])
    else:
        num_messages = 1
    logger.info('Sending %s message(s)', num_messages)
    for i in range(num_messages):
        queue.send(channel, 'OH BOY')


if __name__ == '__main__':
    lemapp.App().run()
