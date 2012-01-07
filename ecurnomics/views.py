# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.db.models import Avg,Sum
from django.shortcuts import redirect

import json
import datetime

from ecurnomics.models import Auction
from ecurnomics.models import Item

def list_items(request):
    items = Item.objects.all().order_by('name_single')
    template = loader.get_template('item_list.html')
    context = Context({'items': items})
    return HttpResponse(template.render(context))

def prices_for_item(request, class_tsid):
    auctions = Auction.objects.filter(class_tsid=class_tsid)
    total_cost = Auction.objects.filter(class_tsid=class_tsid).aggregate(Sum('cost'))['cost__sum']
    total_count = Auction.objects.filter(class_tsid=class_tsid).aggregate(Sum('count'))['count__sum']
    average_cost = total_cost / total_count
    template = loader.get_template('price_graph.html')

    price_data = []
    price_data_daily_averages = {} # Keys are datetimes. They point to an array of prices for each datetime.

    for auction in auctions:
        # Drop high outlyers
        if not (auction.cost > 100 * average_cost):
            # Grab the precise time and price
            time_price_datum = [auction.created_milliseconds, (auction.cost / auction.count)]
            price_data.append(time_price_datum)
            # # Add the price to daily averages
            # auction_date = datetime.date.fromtimestamp(auction.created)
            # try:
            #     price_data_daily_averages[auction_date].append(auction.cost)
            # except KeyError: # We don't have an array for this day yet
            #    price_data_daily_averages[auction_date] = [auction.cost,]
    price_data_as_json = json.dumps(price_data)
    print price_data_daily_averages


    item_label = auctions[0].item.name_single
    context = Context({'auctions': auctions,
                       'item_label': item_label,
                       'price_data_as_json': price_data_as_json,
                       'average_cost': "%0.1f" % (average_cost),
                       'total_count': total_count,
                       'total_cost': total_cost})
    return HttpResponse(template.render(context))

def search(request, search_term):
    found_items = Item.objects.filter(name_single__icontains=search_term).order_by('name_single')
    
    template = loader.get_template('search_results.html')
    context = Context({'found_items': found_items, 'search_term': search_term})
    return HttpResponse(template.render(context))

def search_as_http_get(request):
    """
    Somebody sent us "/search?search_term=meat".
    Redirect them to "/search/meat"
    """
    search_term = request.GET['search_term']
    return redirect("/search/%s" % search_term)
    
def home(request):
    template = loader.get_template('home.html')
    context = Context()
    return HttpResponse(template.render(context))
    
