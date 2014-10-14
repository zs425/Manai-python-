"""
Checkout process utilities.
"""

from django.utils.translation import ugettext as _

from mezzanine.conf import settings

from cartridge.shop.models import Order
from cartridge.shop.utils import set_shipping, sign
from django.contrib.auth.models import User, Group
from cartridge.shop import checkout

europe = ("AL","AD","AM","AT","BY","BE","BA","BG","CH","CY","CZ","DE","DK","EE","ES","FO","FI","FR","GE","GI","GR","HU","HR","IE","IS","IT","LT","LU","LV","MC","MK","MT","NO","NL","PO","PT","RO","RU","SE","SI","SK","SM","TR","UA","VA",)

def billship_handler(request, order_form):
    """
    Called when the first step in
    the checkout process with billing/shipping address fields is
    submitted. Relevant setting: ``SHOP_HANDLER_BILLING_SHIPPING``.
    This function will typically contain any shipping calculation
    where the shipping amount can then be set using the function
    ``cartridge.shop.utils.set_shipping``. The Cart object is also
    accessible via ``request.cart``
    """
    settings.use_editable()

    wholesale_logged_in = False
    user_fullname = ""
    if request.user.is_authenticated():
      user_fullname = " ".join([request.user.first_name, request.user.last_name])
      if request.user.has_perm('custom.wholesale_customer'):
        wholesale_logged_in = True

    total = float(request.cart.total_price())
    country = order_form["shipping_detail_country"].value()
    if wholesale_logged_in:
      if country == "GB":
        if total < 150.00:
          set_shipping(request, "UK delivery, Courier service 1-2 days", 15.50)
        elif total >= 150.00 and total < 500.00:
          set_shipping(request, "UK Free delivery, Courier service 1-2 days", 0.00)
        elif total >= 500.00:
          set_shipping(request, "UK Free delivery, Courier service 1-2 days", 0.00)
      elif country in europe:
        if total < 350.00:
          set_shipping(request, "EU delivery, Courier service 2-5 days", 35.00)
        elif order >= 350:
          set_shipping(request, "EU Free delivery, Courier service 2-5 days", 0.00)
      else: #international
        if total < 55.00:
          set_shipping(request, "International Delivery", 13.50)
        elif total >= 55.00 and total < 150.00:
          set_shipping(request, "International Delivery", 25.00)
        elif total >= 150.00:
          raise checkout.CheckoutError, 'Sorry, we do not accept online orders of that amount from outside Europe, because of prohibitive delivery costs. However, please get in touch by calling +44 7624 482 582, sending an email to info@manai.co.uk, or using our online contact form.'
   
    else: # retail

      uk_delivery_rate = float(order_form["uk_delivery_rate"].value())

      if country == "GB":
        if total < 55.00:
          if uk_delivery_rate == 4.00:
            set_shipping(request, "UK Royal Mail Recorded 1st Class 3-5 days", 4.00)
          elif uk_delivery_rate == 7.5:
            set_shipping(request, "UK Royal Mail Special Delivery 1-2 days", 7.50)
        elif total >= 55.00 and total < 150.00:
          set_shipping(request, "UK Courier Service 1-2 days", 13.50)
        elif total >= 150.00:
          set_shipping(request, "UK Courier Service 1-2 days", 13.50)
      elif country in europe:
        if total < 55.00:
          set_shipping(request, "EU Royal Mail Special Delivery 3-5 days", 13.50)
        elif total >= 55.00 and total < 150.00:
          set_shipping(request, "EU Courier Service 3-5 days", 25.00)
        elif total >= 150.00:
          set_shipping(request, "EU Free delivery, Courier Service 3-5 days", 0.00)
      else: #international
        if total < 55.00:
          set_shipping(request, "International Delivery", 13.50)
        elif total >= 55.00 and total < 150.00:
          set_shipping(request, "International Delivery", 25.00)
          # plus 5% discount
        elif total >= 150.00:
          raise checkout.CheckoutError, 'Sorry, we do not accept online orders of that amount from outside Europe, because of prohibitive delivery costs. However, please get in touch by calling +44 7624 482 582, sending an email to info@manai.co.uk, or using our online contact form.'


def order_handler(request, order_form, order):
  """
  Default order handler - called when the order is complete and
  contains its final data. Implement your own and specify the path
  to import it from via the setting ``SHOP_HANDLER_ORDER``.
  """
  settings.use_editable()
  items = order.items.all()
  
  customer_type = 'Retail'
  user_id = order.user_id
  
  if user_id:
    try:
      user = User.objects.get(id=user_id)
    except:
      pass
    else:
      if user.has_perm('custom.wholesale_customer'):
        customer_type = 'Wholesale'

  company_name = ''
  website = ''
  fullurl = ''
  if customer_type == 'Wholesale':
    try:
      company_name = user.get_profile().company_name
      website = user.get_profile().website
    except:
      pass
    else:
      if website:
        if "http://" not in website:
          fullurl = "http://" + website
        else:
          fullurl = website

  order_context = {
    "order": order,
    "request": request,
    "order_items": items,
    "customer_type": customer_type,
    "company_name": company_name,
    "website": website,
  }
  order_context.update(order.details_as_dict())
  from mezzanine.utils.email import send_mail_template
  send_mail_template(_(customer_type + " Order Completed on manai.co.uk"), "email/order_alert",
      settings.SERVER_EMAIL, settings.DEFAULT_FROM_EMAIL,
      context=order_context, fail_silently=settings.DEBUG)


def initial_order_data(request):
    """
    Return the initial data for the order form - favours request.POST,
    then session, then the last order deterined by either the current
    authenticated user, or from previous the order cookie set with
    "remember my details".
    """
    if request.method == "POST":
        return dict(request.POST.items())
    if "order" in request.session:
        return request.session["order"]
    previous_lookup = {}
    if request.user.is_authenticated():
        previous_lookup["user_id"] = request.user.id
    remembered = request.COOKIES.get("remember", "").split(":")
    if len(remembered) == 2 and remembered[0] == sign(remembered[1]):
        previous_lookup["key"] = remembered[1]
    initial = {}
    if previous_lookup:
        previous_orders = Order.objects.filter(**previous_lookup).values()[:1]
        if len(previous_orders) > 0:
            initial.update(previous_orders[0])
            # Set initial value for "same billing/shipping" based on
            # whether both sets of address fields are all equal.
            shipping = lambda f: "shipping_%s" % f[len("billing_"):]
            if any([f for f in initial if f.startswith("billing_") and
                shipping(f) in initial and
                initial[f] != initial[shipping(f)]]):
                initial["same_billing_shipping"] = False
    return initial


def send_order_email(request, order):
    """
    Send order receipt email on successful order.
    """
    settings.use_editable()
    order_context = {"order": order, "request": request,
                     "order_items": order.items.all()}
    order_context.update(order.details_as_dict())
    from mezzanine.utils.email import send_mail_template
    send_mail_template(_("Order Receipt"), "email/order_receipt",
        settings.SHOP_ORDER_FROM_EMAIL, order.billing_detail_email,
        context=order_context, fail_silently=settings.DEBUG)


# Set up some constants for identifying each checkout step.
CHECKOUT_STEPS = [{"template": "billing_shipping", "url": "details",
                   "title": _("Details")}]
CHECKOUT_STEP_FIRST = CHECKOUT_STEP_PAYMENT = CHECKOUT_STEP_LAST = 1
if settings.SHOP_CHECKOUT_STEPS_SPLIT:
    CHECKOUT_STEPS[0].update({"url": "billing-shipping",
                              "title": _("Address")})
    CHECKOUT_STEPS.append({"template": "payment", "url": "payment",
                           "title": _("Payment")})
    CHECKOUT_STEP_PAYMENT = CHECKOUT_STEP_LAST = 2
if settings.SHOP_CHECKOUT_STEPS_CONFIRMATION:
    CHECKOUT_STEPS.append({"template": "confirmation", "url": "confirmation",
                           "title": _("Confirmation")})
    CHECKOUT_STEP_LAST += 1
