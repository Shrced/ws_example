from constants.websocket_constants import WebSocketConstants


class EventCollector:
    """Класс для сборки списка сообщений, отправляемых на ws сервер"""

    def __init__(self):
        self.events_list: list = []

    def collect_events(self, workflow: list) -> list:
        """Функция для сборки списка сообщений, отправляемых на ws сервер

        Args:
            workflow: сценарий, по которому сборщик определяет, какие сообщения отправятся на SCPL
        """

        event_handlers = {
            "wait": self.__wait,
            "set_mute": self.__set_mute,
            "make_call": self.__make_call,
            "end_call": self.__end_call,
            "wait_for_interaction": self.__common_handler,
        }

        for event in workflow:
            event_handlers.get(event["action"])(event=event)

        return self.events_list

    def __common_handler(self, event: dict):
        """Обработка фиктивных событий (не посылаются на ws  и не модифицируются)
        Args:
            event: обрабатываемый элемент сценария
        """
        self.events_list.append(event)

    def __wait(self, event: dict):
        """Обработка события ожидания, во время ожидания отправляются pong каждые 5 секунд, читаются ответы сервера.
        Args:
            event: обрабатываемый элемент сценария
        """

        timeout_seconds = int(event["data"]["duration"].seconds)

        while timeout_seconds >= WebSocketConstants().PING_TIMEOUT:
            time_event = WebSocketConstants().SLEEP_EVENT.copy()
            time_event['duration'] = WebSocketConstants().PING_TIMEOUT
            self.events_list.append(time_event)
            self.events_list.append(WebSocketConstants().PONG_EVENT)

            timeout_seconds -= WebSocketConstants().PING_TIMEOUT

        if timeout_seconds > 0:
            time_event = WebSocketConstants().SLEEP_EVENT.copy()
            time_event['duration'] = timeout_seconds
            self.events_list.append(time_event)

    def __set_mute(self, event: dict):
        """Обработка события микрофона
        Args:
            event: обрабатываемый элемент сценария
        """
        mute_event = WebSocketConstants().MUTE_MIC.copy()
        mute_event["data"]["mute"] = event["data"]["mute_status"]
        self.events_list.append(mute_event)

    def __end_call(self, event: dict):
        """Обработка события завершения взаимодействия
        Args:
            event: обрабатываемый элемент сценария
        """
        self.events_list.append(WebSocketConstants().END_CALL)

    def __make_call(self, event: dict):
        make_call = WebSocketConstants().MAKE_CALL_PART_2.copy()
        self.events_list.append(WebSocketConstants().MAKE_CALL_PART_1.copy())
        make_call["data"]["destination"] = event["data"]["destination"]
        self.events_list.append({"action": "wait_for_interaction"})
        self.events_list.append(make_call)

