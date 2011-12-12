from django.db import models

# Create your models here.
from django.db import models
import datetime

# Create your models here.

class Auction(models.Model):
    auction_code = models.CharField(max_length=64, primary_key=True)
    class_tsid = models.CharField(max_length=64)
    cost = models.IntegerField()
    category = models.CharField(max_length=64)
    created = models.IntegerField()
    created_milliseconds = models.BigIntegerField(max_length=16)
    datetime_created = models.DateTimeField()
    expires = models.IntegerField()
    url = models.CharField(max_length=255)
    count = models.IntegerField()
    unit_cost = models.FloatField()

    def __unicode__(self):
        return "%s %s at %s (%.2f/unit)" % (self.count, self.class_tsid, self.cost, self.unit_cost)

    def _get_unit_cost_fixed_decimal(self):
        return "%.2f" % (self.unit_cost)
    unit_cost_fixed_decimal = property(_get_unit_cost_fixed_decimal)
