from datetime import timedelta

class WebSocketActions:
    """Функции для формирования сценария взаимодействия"""

    @staticmethod
    def wait(duration: timedelta = timedelta(seconds=5)):
        """Любое ожидание

        Args:
            duration: время ожидания
        """
        return {"action": "wait", "data": {"duration": duration}}

    @staticmethod
    def set_mute(mute_status: bool = True):
        """Включить или выключить микрофон оператора, mute_status определяет статус микрофона

        Args:
            mute_status: статус включения микрофона
        """
        return {"action": "set_mute", "data": {"mute_status": mute_status}}

    @staticmethod
    def end_call():
        """Завершение взаимодействия со стороны оператора"""
        return {"action": "end_call"}

    @staticmethod
    def make_call(destination: str):
        """Инициация звонка

        Args:
            destination: телефон
        """
        return {
            "action": "make_call",
            "data": {
                "destination": destination,

            }
        }

    @staticmethod
    def wait_for_interaction():
        """Ожидание поступления взаимодействия"""
        return {"action": "wait_for_interaction"}
