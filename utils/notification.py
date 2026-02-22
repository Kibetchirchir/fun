import django_rq

def send_notification(phone_number, message):
    pass

def queue_notification(phone_number, message, queue_name="priority"):
    queue = django_rq.get_queue(queue_name)  
    queue.enqueue(send_notification, phone_number, message)
    return True