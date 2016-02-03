"""Queue handling functions for sklounst."""

import logging

import gflags
import pika

logger = logging.getLogger(__name__)
FLAGS = gflags.FLAGS

gflags.DEFINE_string(
    'queue_host',
    'localhost',
    'The RabbitMQ host to use.')
gflags.DEFINE_string(
    'queue_name',
    'aircraft_reports',
    'The queue name to use.')


def get_channel():
    "Returns the RabbitMQ queue channel."
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=FLAGS.queue_host))
    channel = connection.channel()
    channel.queue_declare(queue=FLAGS.queue_name, durable=True)
    return channel


def send(channel, message):
    "Sends a message to the work queue."
    channel.basic_publish(exchange='',
                          routing_key=FLAGS.queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2))


def subscribe(channel, callback):
    "Subcribes to a queue."
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue=FLAGS.queue_name)
