from django.db import models

# Create your models here.
from django.db import models
import time, datetime

# Create your models here.

class Item(models.Model):
    class_tsid = models.CharField(max_length=64, primary_key=True)
    name_single = models.CharField(max_length=64)
    name_plural = models.CharField(max_length=64)
    description = models.TextField()
    base_cost = models.IntegerField()
    category = models.CharField(max_length=64)
    max_stack = models.IntegerField()
    swf_url = models.URLField()
    iconic_url = models.URLField()

    def __unicode__(self):
        return self.name_single

class Auction(models.Model):
    auction_code = models.CharField(max_length=64, primary_key=True)
    class_tsid = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    player_tsid = models.CharField(max_length=16)
    player_name = models.CharField(max_length=64)
    cost = models.IntegerField()
    category = models.CharField(max_length=64)
    created = models.IntegerField()
    created_milliseconds = models.BigIntegerField(max_length=16)
    datetime_created = models.DateTimeField()
    expires = models.IntegerField()
    url = models.CharField(max_length=255)
    count = models.IntegerField()
    unit_cost = models.FloatField()

    item = models.ForeignKey(Item, db_column='class_tsid')


    def __unicode__(self):
        return "%s %s at %s (%.2f/unit)" % (self.count, self.class_tsid, self.cost, self.unit_cost)

    def _get_unit_cost_fixed_decimal(self):
        return "%.2f" % (self.unit_cost)
    unit_cost_fixed_decimal = property(_get_unit_cost_fixed_decimal)

class AveragePrice(models.Model):
    #id = Implicit auto-increment field
    class_tsid = models.CharField(max_length=64)
    date = models.DateTimeField()
    average_price = models.FloatField()
    def _get_date_milliseconds(self):
        return long(time.mktime(self.date.timetuple()) * 1000)
    date_milliseconds = property(_get_date_milliseconds)

    class Meta:
        unique_together = ("class_tsid", "date")

    def __unicode__(self):
        return "%s at %s" % (self.class_tsid, self.date)


    #{
    # : 1,
    # : 2791,
    # "per_page": 1,
    # : 1,
    # : 2791,
    # : {
    #     "PIF164ETGR61NVR-1323991488": {
    #         "player": {
    #             "tsid": "PIF164ETGR61NVR",
    #             "name": "Holgate"
    #     },
    #         "created": "1323991488",
    #         "expires": "1324077888",
    #         "class_tsid": "rookswort",
    #         "category": "herbalism_supplies",
    #         : "5",
    #         : "1600",
    #         : "\/auctions\/PIF164ETGR61NVR\/4eea81c0\/"
    #     }
    #     }
    # } 
    #"url""cost""count""items""total""page""pages""ok"
