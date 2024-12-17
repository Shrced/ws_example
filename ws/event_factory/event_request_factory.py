import asyncio
import json

from constants.websocket_constants import WebSocketConstants


class EventRequestFactory:
    """Основной обработчик отправялемых событий"""

    def __init__(self, ws_client):
        self.ws_client = ws_client
        self.event = None

    async def handle_event(self, event: dict):
        """Метод для получения обработчика сообщения"""
        self.event = event
        events_handlers = {
            "sleep": self.__sleep,
            "pong": self.__pong,
            "endCall": self.__call_data_insert_response,
            "muteMic": self.__workitem_state_id_insert,
            "wait_for_interaction": self.__wait_response,
            "makeCall1": self.__common_request,
            "makeCall2": self.__call_data_insert_response

        }

        try:
            await events_handlers.get(self.event['action'])()

        except TypeError:
            logger.error(
                f"Получено неизвестное событие с именем - {self.event['action']}, оно не может быть обработано клиентом"
            )

        except KeyError:
            logger.error("Фабрика не успела взять данные из события")

    @staticmethod
    async def __wait_response():
        """Обработчик - заглушка для ожидание прихода сообщения"""
        logger.success("Ожидаем приход ответного сообщения")

    async def __pong(self):
        """Обработчик события отправки pong после ping"""
        await self.ws_client.socket.send(json.dumps(WebSocketConstants().PONG_EVENT))
        logger.success(
            f'Завершена обработка посылаемого события: {self.event["action"]},'
            f' оно успешно отправлено на сервер'
        )

    async def __sleep(self):
        """Обработчик события для ожидания"""
        duration = self.event['duration']
        await asyncio.sleep(duration)
        logger.success(f'Завершено запланированное ожидание')

    async def __workitem_state_id_insert(self):
        """Обработчик для вставки workitem_state_id в сообщение"""
        self.event['data']['workitemID'] = self.ws_client.workitem_state_id
        await self.ws_client.socket.send(json.dumps(self.event))

    async def __call_data_insert_response(self):
        """Обработчик для вставки interaction_id в сообщение"""
        self.event['data']['workitemID'] = self.ws_client.workitem_state_id
        await self.ws_client.socket.send(json.dumps(self.event))


    async def __common_request(self):
        """Общий вид обработчика сообщения для отправки его на сервер"""
        await self.ws_client.socket.send(json.dumps(self.event))
        logger.success(
            f'Завершена обработка посылаемого события: {self.event["action"]},'
            f' оно успешно отправлено на сервер'
        )
