from datetime import timedelta

from ws.event_collector import EventCollector
from ws.websocket_actions import WebSocketActions
from ws.ws_client import WsClient


class TestCallWS:
    telephone = "111444555"

    def test_call(self):
        workflow = [
            WebSocketActions.make_call(destination=self.telephone),
            WebSocketActions.set_mute(True),
            WebSocketActions.wait(timedelta(seconds=5)),
            WebSocketActions.end_call()
        ]

        list_events = EventCollector().collect_events(workflow)

        with WsClient(user="user") as client:
            client.launch_ws(events=list_events)

        data = parse_file(file_name="newWorkitemState1")
        interaction_id = data["interacton_id"]
        assert interaction_id, "Взаимодействие не получилось"
