import django_rq
from shipments.models import Shipment

def update_shipment_status(ids, status):
    for id in ids:
        try:
            shipment = Shipment.objects.get(id=id)
            shipment.shipment_status = status
            shipment.save()
            return True
        except Exception as e:
            print(f"Error updating shipment status: {e}")
            return False

def update_bulk_shipment_status_queue(ids, status):
    queue = django_rq.get_queue("priority")
    
    job = queue.enqueue(update_shipment_status, ids, status)
    return job.id