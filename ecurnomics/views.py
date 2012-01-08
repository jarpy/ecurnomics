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
from ecurnomics.models import AveragePrice

def list_items(request):
    items = Item.objects.all().order_by('name_single')
    template = loader.get_template('item_list.html')
    context = Context({'items': items})
    return HttpResponse(template.render(context))

def prices_for_item(request, class_tsid):
    auctions = Auction.objects.filter(class_tsid=class_tsid).order_by('-created')[:5000]
    average_unit_cost = Item.objects.get(class_tsid=class_tsid).average_unit_cost
    template = loader.get_template('price_graph.html')

    # Build the data series for all auctions
    # One data-point per auction
    price_data = []
    for auction in auctions:
        # Drop high outlyers
        if (auction.unit_cost < (5 * average_unit_cost)):
            # Grab the precise time and price
            time_price_datum = [auction.created_milliseconds, auction.unit_cost]
            price_data.append(time_price_datum)
    # Render it to JSON that HighCharts can consume
    price_data_as_json = json.dumps(price_data)

    # Build the data series for daily averages of price
    daily_average_data = []
    for daily_average in AveragePrice.objects.filter(class_tsid=class_tsid):
        time_price_datum = [daily_average.date_milliseconds, daily_average.average_price]
        daily_average_data.append(time_price_datum)
    daily_average_data_as_json = json.dumps(daily_average_data)

    item_label = auctions[0].item.name_single
    context = Context({'auctions': auctions,
                       'item_label': item_label,
                       'price_data_as_json': price_data_as_json,
                       'daily_average_data_as_json': daily_average_data_as_json,
                       'average_unit_cost': "%0.2f" % (average_unit_cost),
                       })
    return HttpResponse(template.render(context))

def search(request, search_term):
    found_items = Item.objects.filter(name_single__icontains=search_term).order_by('name_single')
    
    template = loader.get_template('search_results.html')
    context = Context({'found_items': found_items, 'search_term': search_term})
    return HttpResponse(template.render(context))

def search_as_http_get(request):
    """
    Somebody sent us "/search?search_term=meat"
    Redirect them to "/search/meat"
    """
    search_term = request.GET['search_term']
    return redirect("/search/%s" % search_term)
    
def home(request):
    template = loader.get_template('home.html')
    context = Context()
    return HttpResponse(template.render(context))
    
