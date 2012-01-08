#! /usr/bin/env python

# Batch process to calculate and store daily average prices 

import sys
import os
import datetime


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
        # Clear out everything
        AveragePrice.objects.filter(class_tsid=item.class_tsid).delete()
        auctions = Auction.objects.filter(class_tsid=item.class_tsid)
        prices_by_date = {}
        average_unit_cost = item.average_unit_cost
        # Collect all the prices, grouped by date
        for auction in auctions:
            auction_date = datetime.date.fromtimestamp(auction.created)
            try:
                prices_by_date[auction_date].append(auction.unit_cost)
            except KeyError: # We don't have an array for this day yet
                prices_by_date[auction_date] = [auction.unit_cost]
        # Calculate the average for each day
        for date in prices_by_date.keys():
            # Build a filtered set of prices with silly high outlyers removed
            filtered_prices = []
            for price in prices_by_date[date]:
                if(price < (5 * average_unit_cost)):
                    filtered_prices.append(price)
                else:
                    print "Dropped outragous auction of %s becuase %s is way more than %s" % (item.name_single, price, item.average_unit_cost)
            try:
                datum = AveragePrice.objects.get(date=date, class_tsid=item.class_tsid)
            except AveragePrice.DoesNotExist:
                datum = AveragePrice()
            datum.date = date
            datum.class_tsid = item.class_tsid
            try:
                corrected_average_price = sum(filtered_prices) / len(filtered_prices)
                datum.average_price = corrected_average_price
                datum.save()
            except ZeroDivisionError:
                print "No auctions for %s on %s" % (item.name_single, date)

            
            
    


                
if __name__ == '__main__':
    main()
