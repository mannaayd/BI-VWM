from backend.wiring import Wiring

wiring = Wiring()


def create_or_update():
    wiring.task_queue.enqueue_call()


create_or_update()

create_or_update()