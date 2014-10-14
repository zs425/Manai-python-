from django import forms
from cartridge.shop.forms import OrderForm
from cartridge.shop.payment.paypal import COUNTRIES
from cartridge.shop import checkout
from mezzanine.conf import settings

class OrderForm(OrderForm):
  def __init__(self,*args,**kwrds):
    super(OrderForm, self).__init__(*args, **kwrds)
    step = args[1]
    first = step == checkout.CHECKOUT_STEP_FIRST
    if first:
      billing_country = forms.Select(choices=COUNTRIES)
      shipping_country = forms.Select(choices=COUNTRIES)
      self.fields['billing_detail_country'].widget = billing_country
      self.fields['shipping_detail_country'].widget = shipping_country