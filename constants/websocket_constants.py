class WebSocketConstants:
    """Шаблоны событий, отправляемые ws серверу"""
    PING_TIMEOUT = 5

    @property
    def END_CALL(self):
        return {
            'action': 'endCall',
            'data': {
                'interactionID': ''
            }
        }

    @property
    def MAKE_CALL_PART_1(self):
        return {
            'action': 'makeCall1',
            'data': {
                'destination': '$telephone',
            },
        }

    @property
    def MAKE_CALL_PART_2(self):
        return {
            'action': 'makeCall2',
            'data': {
                'data': 'data',
                'interactionId': ''
            },
        }

    @property
    def MUTE_MIC(self):
        return {
            'action': 'muteMic',
            'data': {
                'workitemID': '',
            }
        }

    @property
    def PONG_EVENT(self):
        return {'action': 'pong'}

    """ Фиктивные события """
    @property
    def SLEEP_EVENT(self):
        return {'action': 'sleep', 'duration': '10'}
