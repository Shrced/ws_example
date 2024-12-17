import json
import os
import websockets

from constants.websocket_constants import WebSocketConstants


def record_ws_response(event: dict):
    """Функция для записи полученного ивента

    Args:
        event: полученный ивент
    """
    counter = 0
    filename = "{}{}.json"

    # Одних и тех же сообщений может быть много, поэтому у каждого справа будет свой номер последовательности
    while os.path.isfile(
        f"{root_dir}/ws/received_events/{filename.format(event['action'], counter)}"
    ):
        counter += 1

    filename = filename.format(event['action'], counter)

    with open(f"{root_dir}/ws/received_events/{filename}", "w+", encoding="utf-8") as received_event:
        json.dump(event, received_event)


class EventResponseFactory:
    """Основной обработчик полученных событий"""
    def __init__(self, ws_client):
        self.ws_client = ws_client
        self.event = None

    async def handle_event(self, event: dict):
        """Метод для получения обработчика определенного присланного сообщения

        Args:
            event: обрабатываемое полученное сообщение
        """
        self.event = event

        events_handlers = {
            "ping": self.__ping,
            "resultMakeCall1": self.__get_data,
            "resultMakeCall2": self.__common_response,
            "someAnswer": self.__something,
            "resultMute": self.__common_response,
            "resultEndCall": self.__common_response,

        }
        record_ws_response(self.event)

        try:
            await events_handlers.get(self.event['action'])()

        except TypeError:
            logger.error(
                f"Получено неизвестное событие с именем - {self.event['action']}, оно не может быть обработано клиентом"
            )

        except KeyError:
            logger.error("Фабрика не успела взять данные из события")

    async def __ping(self):
        """Обработчик события отправки pong после ping"""
        await self.ws_client.socket.send(json.dumps(WebSocketConstants().PONG_EVENT))
        logger.success(f'Завершена обработка полученного события: {self.event["action"]}, отправлен pong')

    async def __common_response(self):
        """Общий обработчик полученного события, для таких ничего не требуется, просто его фиксация"""
        logger.success(f'Завершена обработка полученного события: {self.event["action"]}')

    async def __get_data(self):
        """Обработчик получение из него interactionID, workitemID"""
        self.ws_client.interaction_id = self.event['data']['interactionID']
        self.ws_client.workitem_state_id = self.event['data']['workitemID']
        self.ws_client.wait_flag = True
