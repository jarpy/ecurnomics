# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response

from ecurnomics.models import Auction

def items(request):
    items = Auction.objects.values('class_tsid').distinct().order_by('class_tsid')
    template = loader.get_template('items/index.html')
    context = Context({'items': items})
    return HttpResponse(template.render(context))
