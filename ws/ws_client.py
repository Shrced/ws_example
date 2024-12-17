import asyncio
import json
import time

from ws.event_factory.event_request_factory import EventRequestFactory
from ws.event_factory.event_response_factory import EventResponseFactory


class WsClient:
    def __init__(self, user):
        """Инициализация вебсокет клиента
        Args:
            user: пользователь для подключения
        """
        self.socket = None
        self.recv_fabric = EventResponseFactory(self)
        self.send_fabric = EventRequestFactory(self)
        self.url = self.get_ws_url()
        self.stop_flag = False
        self.user = user
        self.access_token = None
        self.wait_flag = False
        self.interaction_id = None
        self.workitem_state_id = None

    def __enter__(self):
        logger.success(f'Оператор {self.user} начал работу')
        return self

    def __exit__(self, exc_type, exc, tb):
        logger.success(f'Оператор {self.user} завершил работу')

    @staticmethod
    def get_ws_url() -> str:
        """Создание ссылки для подключения к ws серверу"""
        return 'url'

    async def message_reader(self):
        """Функция для чтения ws сообщений"""
        while not self.stop_flag:
            response = json.loads(await self.socket.recv())
            await self.recv_fabric.handle_event(response)

    async def message_sender(self, events):
        """Функция для отправки ws сообщений"""
        for event in events:
            await self.send_fabric.handle_event(event)

            if event["action"] in ("wait_for_interaction",):
                timeout = time.time() + 40

                while self.wait_flag is False and time.time() < timeout:
                    await asyncio.sleep(0.1)

                self.wait_flag = False
        self.stop_flag = True

    async def processing(self, events: list):
        """Функция для запуска задач чтения и отправки webscoket сообщений
        Args:
             events: список сообщений для их поочередной отправки на сервер
        """
        async with websockets.connect(
            self.url,
            extra_headers={"cookie": 'cookie'}
        ) as self.socket:
            send_task = asyncio.create_task(self.message_sender(events))
            receive_task = asyncio.create_task(self.message_reader())

            await asyncio.gather(send_task, receive_task)

    def launch_ws(self, events):
        try:
            asyncio.run(self.processing(events=events))

        except ConnectionClosedOK as e:
            pass

        except Exception as error:
            raise error
