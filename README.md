Пример того, как можно организовать механизм у себя в проекте

В тесте описан сценарий взаимодействия: взять звонок, заглушить микро, подождать, закончить звонок

Обратите внимание, что событие make_call внутри состоит из отправки двух технических сообщений - makeCall1 и makeCall2
Перед отправкой makeCall2 его надо заполнить данными из сообщения resultMakeCall1. Поэтому в обработчике resultMakeCall1 ставится соответствующий флаг
Ожидание resultMakeCall1 происхдит с помощью сообщения {"action": "wait_for_interaction"}, которое ставится в нужный момент в обработчике __make_call в классе EventCollector

В теле теста показан один из примеров, как можно пользоваться телами полученных сообщений после отработки механизма
