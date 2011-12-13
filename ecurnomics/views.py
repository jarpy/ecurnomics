# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.db.models import Avg,Sum
import json


from ecurnomics.models import Auction
from ecurnomics.models import Item

def auctions(request):
    items = Item.objects.all().order_by('name_single')
    template = loader.get_template('auctions/index.html')
    context = Context({'items': items})
    return HttpResponse(template.render(context))

def auctions_for_item(request, class_tsid):
    auctions = Auction.objects.filter(class_tsid=class_tsid)
    total_cost = Auction.objects.filter(class_tsid=class_tsid).aggregate(Sum('cost'))['cost__sum']
    total_count = Auction.objects.filter(class_tsid=class_tsid).aggregate(Sum('count'))['count__sum']
    average_cost = total_cost / total_count
    template = loader.get_template('auctions_for_item/index.html')

    price_data = []
    for auction in auctions:
        # Drop high outlyers
        if not (auction.cost > 100 * average_cost):
            time_price_datum = [auction.created_milliseconds, (auction.cost / auction.count)]
            price_data.append(time_price_datum)
    price_data_as_json = json.dumps(price_data)

    # Try to look up the fancy, human name for the item
    # but fall back to the class_tsid if we don't have it.
    try:
        item_label = auctions[0].item.name_plural
    except:
        item_label = class_tsid
    context = Context({'auctions': auctions,
                       'item_label': item_label,
                       'price_data_as_json': price_data_as_json,
                       'average_cost': "%0.1f" % (average_cost),
                       'total_count': total_count,
                       'total_cost': total_cost})
    return HttpResponse(template.render(context))
