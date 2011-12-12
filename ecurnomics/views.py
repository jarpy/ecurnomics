# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.db.models import Avg,Sum
import json


from ecurnomics.models import Auction

def items(request):
    items = Auction.objects.values('class_tsid').distinct().order_by('class_tsid')
    template = loader.get_template('items/index.html')
    context = Context({'items': items})
    return HttpResponse(template.render(context))

def item(request, class_tsid):
    items = Auction.objects.filter(class_tsid=class_tsid)
    total_cost = Auction.objects.filter(class_tsid=class_tsid).aggregate(Sum('cost'))['cost__sum']
    total_count = Auction.objects.filter(class_tsid=class_tsid).aggregate(Sum('count'))['count__sum']
    average_cost = total_cost / total_count
    template = loader.get_template('item/index.html')

    #price_data_as_json = json.dumps([[4782374, 50],[342342134, 489]])
    price_data = []
    for item in items:
        time_price_datum = [item.created_milliseconds, item.cost]
        price_data.append(time_price_datum)
    price_data_as_json = json.dumps(price_data)
   
    context = Context({'items': items,
                       'class_tsid': class_tsid,
                       'price_data_as_json': price_data_as_json,
                       'average_cost': average_cost,
                       'total_count': total_count,
                       'total_cost': total_cost})
    return HttpResponse(template.render(context))
