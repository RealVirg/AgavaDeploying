from celery import shared_task
from subscriber import Subscriber


@shared_task
def test_msg(config, queue_name, binding_key, routing_key_request, request):
    subscriber = Subscriber(config)
    subscriber.setup(queue_name, binding_key, routing_key_request, request)
