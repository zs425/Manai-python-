from cartridge.shop.models import *
from django.db import models
from django.contrib.auth.models import User
from mezzanine.core.fields import FileField
from mezzanine.core.fields import RichTextField
from mezzanine.core.models import Displayable
from mezzanine.core.managers import DisplayableManager
from cartridge.shop.payment.paypal import COUNTRIES
from django.conf import settings
from campaign_monitor_api import CampaignMonitorApi

class WholesaleProduct(Product):
  class Meta:
    permissions = (
          ("wholesale_customer", "Can see wholesale prices and buy wholesale products"),
    )
  objects = DisplayableManager()


class RetailProduct(Product):
  objects = DisplayableManager()
  pass


class CustomerProfile(models.Model):
  """ This is defined as the user profile model in settings:
      AUTH_PROFILE_MODULE = 'custom.CustomerProfile'
  """

  # This field is required.
  user = models.OneToOneField(User)

  street = models.CharField("Street", max_length=50, null=True)
  address_line2 = models.CharField("Address line 2", max_length=50, null=True, blank=True)
  city = models.CharField(max_length=50, null=True)
  state = models.CharField("State/Region", max_length=50, null=True, blank=True)
  country = models.CharField(max_length=2, null=True, choices=COUNTRIES, default='GB')
  postcode = models.CharField(max_length=10, null=True)
  phone = models.CharField(max_length=50, null=True)
  company_name = models.CharField(max_length=50, null=True, blank=True)
  website = models.CharField(max_length=100, null=True, blank=True)
  optin = models.BooleanField("Sign me up to receive occasional emails and special offers from Manai (All your private data is confidential. We will never sell, exchange or market it in any way)", default=False)
  hdyh = models.CharField("How did you hear about us?", max_length=2, choices=settings.HOW_DID_YOU_HEAR_CHOICES, default=settings.GOOGLE, blank=True)
  hdyh_other = models.CharField("Other", max_length=50, null=True, blank=True)
  user_type = models.CharField("Kind of business (if applicable)", max_length=2, choices=settings.USER_TYPE_CHOICES, null=True, blank=True)
  user_type_other = models.CharField("Other", max_length=50, null=True, blank=True)

  description = RichTextField(blank=True)
  image = FileField(verbose_name="Featured Image",
                    upload_to="uploads/profiles", format="Image",
                    max_length=255, null=True, blank=True)