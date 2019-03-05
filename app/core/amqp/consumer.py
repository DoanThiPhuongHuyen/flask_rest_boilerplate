# coding=utf-8
import logging
from logging import config
from typing import Optional

import configs
from app.core.amqp.connection import CONNECTION_MANAGER

logging.config.dictConfig(configs.LOGGING)
LOGGER = logging.getLogger('main')


class BaseConsumer(object):
    """Base class for consumer"""
    channel = None
    connection_name = None
    __queue_options = {
        'durable': True,
        'auto_delete': True,
        'passive': None,
        'exclusive': None,
        'arguments': None,
    }

    def __init__(self, queue_name: str, queue_options: dict = None, connection: str = 'default'):
        """
        Constructor for Basic Consumer
        :param queue_name: queue name
        :param binding_dict: dictionary, key
        :param queue_options: options for queue
        :param connection: connection key in configs
        """
        if queue_options is not None:
            self.__queue_options = queue_options
        self.queue_name = queue_name
        self.connection_name = connection
        self.connection = CONNECTION_MANAGER.get_connection(self.connection_name)
        self.queue_declare()

    def queue_declare(self):
        """
        Declare queue
        :return:
        """
        self.channel = self.get_channel()
        self.channel.queue_declare(self.queue_name, **self.__queue_options)

    def get_channel(self):
        """
        Get channel of this consumer
        :return:
        """
        if self.channel is None or not self.channel.is_open:
            if not self.connection.is_open:
                self.connection = CONNECTION_MANAGER.get_connection(self.connection_name)
            self.channel = self.connection.channel()
        return self.channel

    def queue_bind(self, exchange_name, routing_key, queue_name=None, arguments=None):
        """Bind queue"""
        if queue_name is None:
            queue_name = self.queue_name
        self.channel = self.get_channel()
        self.channel.queue_bind(queue_name, exchange_name, routing_key=routing_key,
                                arguments=arguments)


class BasicMsgHandler(object):
    exchange = ''
    routing_key = ''

    @classmethod
    def process_msg(cls):
        def processing_msg(channel, method, properties, body):
            LOGGER.info('routing key: {routing_key} | headers: {headers} | body: {body}'.format(
                routing_key=cls.routing_key,
                headers=properties,
                body=body.decode(),
            ))
        return processing_msg


class ConsumeQueue(BaseConsumer):
    active = False

    def start_consuming(self, exchange, routing_key):
        try:
            self.active = True
            self.channel = self.get_channel()
            handler = self.get_handler(exchange, routing_key)
            self.queue_bind(exchange, routing_key)
            self.channel.basic_consume(handler.process_msg(), queue=self.queue_name, no_ack=False)
            LOGGER.info('Start consuming queue {queue}'.format(queue=self.queue_name))
            self.channel.start_consuming()
        except:
            LOGGER.exception(
                'Failed to start connection {connection_name} | queue {queue_name}'.format(
                    connection_name=self.connection_name,
                    queue_name=self.queue_name
                ))
        finally:
            LOGGER.info('Stop consuming queue {queue}'.format(queue=self.queue_name))
            self.active = False

    def stop_consuming(self):
        self.channel.stop_consuming()

    handlers = {}

    @classmethod
    def register(cls, exchange, routing_key, *args, **kwargs):
        def wrapper(handler_cls):
            if exchange not in cls.handlers:
                cls.handlers[exchange] = {}
            handler = cls.handlers[exchange]
            if routing_key not in handler:
                handler[routing_key] = handler_cls
            handler_cls.routing_key = routing_key
            handler_cls.exchange = exchange
            return handler[routing_key]

        return wrapper

    @classmethod
    def register_s(cls):
        def wrapper(handler_cls):
            if handler_cls.exchange not in cls.handlers:
                cls.handlers[handler_cls.exchange] = {}
            handler = cls.handlers[handler_cls.exchange]
            if handler_cls.routing_key not in handler:
                handler[handler_cls.routing_key] = handler_cls
            return handler[handler_cls.routing_key]

        return wrapper

    @classmethod
    def get_handler(cls, exchange, routing_key) -> Optional[BasicMsgHandler]:
        if exchange not in cls.handlers:
            LOGGER.error('exchange {} not registered'.format(exchange))
            return None
        handler = cls.handlers[exchange]
        if routing_key not in handler:
            LOGGER.error('routing key {} for exchange {} not registered'.format(routing_key, exchange))
            return None
        return handler[routing_key]


if __name__ == '__main__':
    routing_keys = {
        'rk1': None,
        'rk2': None,
        'rk3': None,
    }
    consumer = ConsumeQueue('its-queue')
    consumer.start()
