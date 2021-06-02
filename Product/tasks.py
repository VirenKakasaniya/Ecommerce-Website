from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .email import send_review_email
from .models import OrderItem,Order

@shared_task
def review_order_and_send_mail_task(name,email,data,order_id):
    # print('get')
    ready_to_dispatch = ''
    out_of_stock = ''
    order_status = False
    for i in data:
            id = i['id']
            item = OrderItem.objects.get(id = id)
  
            check_availability = item.check_product_quantity
            
            if check_availability:
                item.update_product_quantity
                ready_to_dispatch = ready_to_dispatch + item.product.name + ', '
                item.status = 'accept'
                item.save()
                order_status = True
            else:
                out_of_stock = out_of_stock + item.product.name + ', '
                item.status = 'reject'
                item.save()
    
    order = Order.objects.get(id = order_id)
    if order_status == True:
        order.status = 'accept'
    else:
        order.status = 'reject'
    order.save()
    
    msg_body = 'Thank You for shopping. '
    if len(ready_to_dispatch)!=0:
        msg_body +=  'We are glad to inform you that your orderitmes listed as ' + ready_to_dispatch + 'are ready to dispatch.'

    if len(out_of_stock) !=0:
        msg_body +=  ' and we are sorry to inform you that products from your order listed as '+out_of_stock  +' are currently out of stock.' 
    return send_review_email(name, email, msg_body)


