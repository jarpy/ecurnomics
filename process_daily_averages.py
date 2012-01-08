#! /usr/bin/env python

# Batch process to calculate and store daily average prices 

import sys
import os
import datetime
import time


def setup_environment():
    pathname = os.path.dirname(sys.argv[0])
    sys.path.append(os.path.abspath(pathname))
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    

setup_environment()
from ecurnomics.models import Item
from ecurnomics.models import Auction
from ecurnomics.models import AveragePrice

    
def main():
    items = Item.objects.all().order_by('name_single')
    for item in items:
        print "Calculating daily averages for %s" % item
        auctions = Auction.objects.filter(class_tsid=item.class_tsid)
        prices_by_date = {}
        # Collect all the prices, grouped by date
        for auction in auctions:
            auction_date = datetime.date.fromtimestamp(auction.created)
            try:
                prices_by_date[auction_date].append(auction.unit_cost)
            except KeyError: # We don't have an array for this day yet
                prices_by_date[auction_date] = [auction.unit_cost]
        # Calculate the average for each day
        for date in prices_by_date.keys():
            uncorrected_average_price = sum(prices_by_date[date]) / len(prices_by_date[date])
            # Build a filtered set of prices with silly high outlyers removed
            filtered_prices = []
            for price in prices_by_date[date]:
                if(price < (5 * uncorrected_average_price)):
                    filtered_prices.append(price)
            corrected_average_price = sum(filtered_prices) / len(filtered_prices)                 
            
            try:
                datum = AveragePrice.objects.get(date=date, class_tsid=item.class_tsid)
            except AveragePrice.DoesNotExist:
                datum = AveragePrice()
            datum.date = date
            datum.class_tsid = item.class_tsid
            datum.average_price = corrected_average_price
            datum.save()
	# Back off and let some other procs run
	print "Sleeping..."
	time.sleep(5)
            
    


                
if __name__ == '__main__':
    main()
