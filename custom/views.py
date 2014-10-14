from django.conf import settings
from mezzanine.conf import settings
from mezzanine.pages import page_processors
from mezzanine.pages.models import Page
from mezzanine.galleries.models import Gallery
from mezzanine.utils.views import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from mezzanine.blog.models import BlogPost
from mezzanine.utils.email import send_verification_mail, send_mail_template
from utils import my_login_redirect
from mezzanine.accounts.forms import LoginForm, ProfileForm, PasswordResetForm
from django.contrib.auth import (authenticate, login as auth_login, logout as auth_logout)
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from cartridge.shop.views import *
from cartridge.shop.models import *
from models import WholesaleProduct, RetailProduct, CustomerProfile
from campaign_monitor_api import CampaignMonitorApi
from django.views.decorators.cache import never_cache

USER_TYPE_CHOICES = dict(settings.USER_TYPE_CHOICES)

def home(request, slug, template="pages/index.html", extra_context=None):
  content = Page.objects.get(slug='home').richtextpage.content
  posts = BlogPost.objects.published()[:2]

  # TEMP
  #display_message = True
  #if u"visited" in request.session:
  #  display_message = False
  #request.session['visited'] = True
  # /TEMP

  galleries = Gallery.objects.published()
  for gallery in galleries:
    try:
      gallery.firstimage = gallery.images.all()[0]
    except:
      pass

  return render_to_response("pages/index.html",
  {
  #"home": True,
  "posts": posts,
  #"reviews": reviews,
  #"latest_products": latest_products,
  #"featured_products": featured_products,
  #"nextevent": nextevent,
  #"about_text": about_text,
  #"display_message": display_message,
  "content": content,
  "galleries": galleries,
  }, context_instance = RequestContext(request))


def retail_product(request, slug, template="shop/product.html"):
  """
  Display a product - convert the product variations to JSON as well as
  handling adding the product to either the cart or the wishlist.
  """
  #published_products = Product.objects.published(for_user=request.user) # Can't get this to work with RetailProduct

  published_products = RetailProduct.objects.published()
  product = get_object_or_404(published_products, slug=slug)
  to_cart = (request.method == "POST" and
         request.POST.get("add_wishlist") is None)
  add_product_form = AddProductForm(request.POST or None, product=product,
                    initial={"quantity": 1}, to_cart=to_cart)
  if request.method == "POST":
    if add_product_form.is_valid():
      if to_cart:
        quantity = add_product_form.cleaned_data["quantity"]
        request.cart.add_item(add_product_form.variation, quantity, "retail-shop")
        recalculate_discount(request)
        info(request, "Item added to cart")
        return redirect("basket")
      else:
        skus = request.wishlist
        sku = add_product_form.variation.sku
        if sku not in skus:
          skus.append(sku)
        info(request, "Item added to wishlist")
        response = redirect("shop_wishlist")
        set_cookie(response, "wishlist", ",".join(skus))
        return response
  fields = [f.name for f in ProductVariation.option_fields()]
  fields += ["sku", "image_id"]
  variations = product.variations.all()
  variations_json = simplejson.dumps([dict([(f, getattr(v, f))
                    for f in fields])
                    for v in variations])
  context = {
    "product": product,
    "images": product.images.all(),
    "variations": variations,
    "variations_json": variations_json,
    "has_available_variations": any([v.has_price() for v in variations]),
    "related": product.related_products.published(for_user=request.user),
    "add_product_form": add_product_form,
  }
  return render(request, template, context)


def add_to_cart(request):
  if request.is_ajax():
    if request.method == 'POST':
      shop_slug = request.POST["shop_slug"]
      if shop_slug == "wholesale-shop":
        if not request.user.is_authenticated():
          return HttpResponse("No")
        if not request.user.has_perm('custom.wholesale_customer'):
          return HttpResponse("No")

      id = int(request.POST["id"])
      product = Product.objects.get(id=id)
      add_product_form = AddProductForm(request.POST, product=product, initial={"quantity": 1}, to_cart=True)
      if add_product_form.is_valid():
        quantity = add_product_form.cleaned_data["quantity"]

        # #################################################################################
        # DISCOUNT VOUCHERS October 16th 2012
        # If the product is one of the discount voucher products and
        # either the quantity is > 1 or they've already got one in their basket
        # then tell them no (but send a friendly message)

        try:
          discount_product = Product.objects.get(id=5487)
        except:
          pass
        else:
          if product == discount_product:
            if int(quantity) > 1:
              return HttpResponse("Discount error")
            if request.cart.has_items():
              # contains the product already ?
              for item in request.cart:
                #v = ProductVariation.objects.get(sku=item.sku)
                for dv in discount_product.variations.all():
                  if dv.sku == item.sku:
                    return HttpResponse("Discount error")
        # #################################################################################

        request.cart.add_item(add_product_form.variation, quantity, shop_slug)
        recalculate_discount(request)
        return HttpResponse(request.cart.total_price())
  return HttpResponse("No")


def wholesale_product(request, slug, template="shop/product.html"):
  """
  Display a product - convert the product variations to JSON as well as
  handling adding the product to either the cart or the wishlist.
  """
  #published_products = Product.objects.published(for_user=request.user) # Can't get this to work with WholesaleProduct

  published_products = WholesaleProduct.objects.published()
  product = get_object_or_404(published_products, slug=slug)
  to_cart = (request.method == "POST" and
         request.POST.get("add_wishlist") is None)

  add_product_form = ""
  wholesale_logged_in = False
  user_fullname = ""
  if request.user.is_authenticated():
    user_fullname = " ".join([request.user.first_name, request.user.last_name])
    if request.user.has_perm('custom.wholesale_customer'):
      wholesale_logged_in = True
      add_product_form = AddProductForm(request.POST or None, product=product,
                    initial={"quantity": 1}, to_cart=to_cart)
  if request.method == "POST":
    if add_product_form.is_valid():
      if to_cart:
        quantity = add_product_form.cleaned_data["quantity"]
        request.cart.add_item(add_product_form.variation, quantity, "wholesale-shop")
        recalculate_discount(request)
        info(request, "Item added to cart")
        return redirect("basket")
      else:
        skus = request.wishlist
        sku = add_product_form.variation.sku
        if sku not in skus:
          skus.append(sku)
        info(request, "Item added to wishlist")
        response = redirect("shop_wishlist")
        set_cookie(response, "wishlist", ",".join(skus))
        return response
  fields = [f.name for f in ProductVariation.option_fields()]
  fields += ["sku", "image_id"]
  variations = product.variations.all()
  variations_json = simplejson.dumps([dict([(f, getattr(v, f))
                    for f in fields])
                    for v in variations])

  settings.use_editable()
  wholesale_minimum_spend = float(settings.WHOLESALE_MINIMUM_SPEND)

  context = {
    "product": product,
    "images": product.images.all(),
    "variations": variations,
    "variations_json": variations_json,
    "has_available_variations": any([v.has_price() for v in variations]),
    "related": product.related_products.published(for_user=request.user),
    "add_product_form": add_product_form,
    "shop_slug": "wholesale-shop",
    "wholesale_logged_in": wholesale_logged_in,
    "user_fullname": user_fullname,
    "wholesale_minimum_spend": wholesale_minimum_spend,
  }
  return render(request, template, context)


def retail_signup(request, template="accounts/retail_signup.html"):
  form = ProfileForm(request.POST or None)
  if request.method == "POST" and form.is_valid():
    new_user = form.save()

    # Add to campaign monitor
    if bool(form.cleaned_data.get("optin")):
      cm_api = CampaignMonitorApi(settings.CM_API_KEY, settings.CM_CLIENT_ID)
      listid = settings.CM_RETAIL_LIST_ID
      custom_fields = {}
      #try:
      cm_api.subscriber_add(
          listid,
          form.cleaned_data.get("email"),
          form.cleaned_data.get("first_name") + ' ' + form.cleaned_data.get("last_name"),
          custom_fields=custom_fields)
      #except:
      #  pass

    if not new_user.is_active:
      send_verification_mail(request, new_user, "signup_verify")
      info(request, "A verification email has been sent with a link for activating your account.")
    else:
      info(request, "Successfully signed up")
      auth_login(request, new_user)
      return my_login_redirect(request)
  context = {"form": form, "title": "Customer Registration"}
  return render(request, template, context)


def wholesale_signup(request, template="accounts/wholesale_signup.html"):
  form = ProfileForm(request.POST or None)
  if request.method == "POST" and form.is_valid():
    new_user = form.save()
    g = Group.objects.get(name='Wholesale Customers')
    g.user_set.add(new_user)

    # Add to campaign monitor
    if bool(form.cleaned_data.get("optin")):
      cm_api = CampaignMonitorApi(settings.CM_API_KEY, settings.CM_CLIENT_ID)
      listid = settings.CM_WHOLESALE_LIST_ID

      usertype = ""
      if form.cleaned_data.get("user_type"):
        try:
          usertype = USER_TYPE_CHOICES[form.cleaned_data.get("user_type")]
        except:
          pass
      elif form.cleaned_data.get("user_type_other"):
        usertype = form.cleaned_data.get("user_type_other")

      custom_fields = {"CustomerType": usertype}
      try:
        cm_api.subscriber_add(
          listid,
          form.cleaned_data.get("email"),
          form.cleaned_data.get("first_name") + ' ' + form.cleaned_data.get("last_name"),
          custom_fields=custom_fields)
      except:
        pass

    if not new_user.is_active:
      send_verification_mail(request, new_user, "signup_verify")
      info(request, "A verification email has been sent with a link for activating your account.")
    else:
      info(request, "Successfully signed up")
      auth_login(request, new_user)
      send_registration_confirmation_email(request)
      return my_login_redirect(request, wholesale=True)
  context = {"form": form, "title": "Wholesale Customer Registration"}
  return render(request, template, context)


def retail_login(request, template="accounts/retail_login.html"):
  form = LoginForm(request.POST or None)
  if request.method == "POST" and form.is_valid():
    authenticated_user = form.save()
    info(request, "Successfully logged in")
    auth_login(request, authenticated_user)
    return my_login_redirect(request)
  context = {"form": form, "title": "Customer Login"}
  return render(request, template, context)


def wholesale_login(request, template="accounts/wholesale_login.html"):
  form = LoginForm(request.POST or None)
  if request.method == "POST" and form.is_valid():
    authenticated_user = form.save()
    info(request, "Successfully logged in")
    auth_login(request, authenticated_user)
    return my_login_redirect(request, wholesale=True)
  context = {"form": form, "title": "Wholesale Customer Login"}
  return render(request, template, context)


def retail_logout(request):
  auth_logout(request)
  info(request, "Successfully logged out")
  return redirect(request.GET.get("next", "/retail-shop/"))

def wholesale_logout(request):
  auth_logout(request)
  info(request, "Successfully logged out")
  return redirect(request.GET.get("next", "/wholesale-shop/"))


@never_cache
def cart(request, template="shop/cart.html"):
  """
  Display cart and handle removing items from the cart.
  """

  settings.use_editable()

  wholesale_minimum_spend = float(settings.WHOLESALE_MINIMUM_SPEND)
  total = float(request.cart.total_price())

  cart_formset = CartItemFormSet(instance=request.cart)
  discount_form = DiscountForm(request, request.POST or None)

  wholesale_logged_in = False
  user_fullname = ""
  if request.user.is_authenticated():
    user_fullname = " ".join([request.user.first_name, request.user.last_name])
    if request.user.has_perm('custom.wholesale_customer'):
      wholesale_logged_in = True


#  if not "applied" in request.session:
#    if total > 55.0 and not wholesale_logged_in:
#      discount_form = DiscountForm(request, {"discount_code": "5005XtYTR"})
#      discount_form.set_discount()
#      request.session["applied"] = False
#    else:
#      request.session["applied"] = True
#  else:
#    request.session["applied"] = True
  request.session["applied"] = True


  build_your_own = False
  nextstep = ""
  if u"build_your_own" in request.session:
    build_your_own = request.session['build_your_own']
    nextstep = request.session['nextstep']

  if request.method == "POST":
    valid = True
    if request.POST.get("update_cart"):
      valid = request.cart.has_items()
      if not valid:
        # Session timed out.
        info(request, "Your cart has expired")
      else:
        cart_formset = CartItemFormSet(request.POST,
                         instance=request.cart)
        valid = cart_formset.is_valid()
        if valid:
          cart_formset.save()
          recalculate_discount(request)
          info(request, "Cart updated")
          request.session["applied"] = True
    else:
      valid = discount_form.is_valid()
      if valid:
        discount_form.set_discount()
        request.session["applied"] = True

    if valid:
      return HttpResponseRedirect(reverse("basket"))
  context = {
    "cart_formset": cart_formset,
    "wholesale_logged_in": wholesale_logged_in,
    "user_fullname": user_fullname,
    "wholesale_minimum_spend": int(wholesale_minimum_spend),
    "total": total,
    "build_your_own": build_your_own,
    "build_your_own_nextstep": nextstep,
    "discount_applied": request.session["applied"],
    }
  settings.use_editable()
  if (settings.SHOP_DISCOUNT_FIELD_IN_CART and
    DiscountCode.objects.active().count() > 0):
    context["discount_form"] = discount_form
  return render_to_response(template, context, RequestContext(request))


def checkout_steps(request):
  """
  Display the order form and handle processing of each step.
  """

  # Do the authentication check here rather than using standard
  # login_required decorator. This means we can check for a custom
  # LOGIN_URL and fall back to our own login view.
  settings.use_editable()

  authenticated = request.user.is_authenticated()
  if settings.SHOP_CHECKOUT_ACCOUNT_REQUIRED and not authenticated:
    url = "%s?next=%s" % (settings.LOGIN_URL, reverse("checkout"))
    return HttpResponseRedirect(url)


  wholesale_logged_in = False
  user_fullname = ""
  if authenticated:
    user_fullname = " ".join([request.user.first_name, request.user.last_name])
    if request.user.has_perm('custom.wholesale_customer'):
      wholesale_logged_in = True
      if float(request.cart.total_price()) < float(settings.WHOLESALE_MINIMUM_SPEND):
        return HttpResponseRedirect(reverse("basket"))

  # Determine the Form class to use during the checkout process
  form_class = get_callable(settings.SHOP_CHECKOUT_FORM_CLASS)

  step = int(request.POST.get("step", checkout.CHECKOUT_STEP_FIRST))
  initial = checkout.initial_order_data(request)
  form = form_class(request, step, initial=initial)
  data = request.POST
  checkout_errors = []

  if request.POST.get("back") is not None:
    # Back button in the form was pressed - load the order form
    # for the previous step and maintain the field values entered.
    step -= 1
    form = form_class(request, step, initial=initial)
  elif request.method == "POST":
    form = form_class(request, step, initial=initial, data=data)
    if form.is_valid():
      # Copy the current form fields to the session so that
      # they're maintained if the customer leaves the checkout
      # process, but remove sensitive fields from the session
      # such as the credit card fields so that they're never
      # stored anywhere.
      request.session["order"] = dict(form.cleaned_data)
      sensitive_card_fields = ("card_number", "card_expiry_month",
                   "card_expiry_year", "card_ccv")
      for field in sensitive_card_fields:
        del request.session["order"][field]

      # FIRST CHECKOUT STEP - handle shipping and discount code.
      if step == checkout.CHECKOUT_STEP_FIRST:
        try:
          billship_handler(request, form)
        except checkout.CheckoutError, e:
          checkout_errors.append(e)
        form.set_discount()

      # FINAL CHECKOUT STEP - handle payment and process order.
      if step == checkout.CHECKOUT_STEP_LAST and not checkout_errors:
        # Create and save the inital order object so that
        # the payment handler has access to all of the order
        # fields. If there is a payment error then delete the
        # order, otherwise remove the cart items from stock
        # and send the order reciept email.
        order = form.save(commit=False)
        order.setup(request)
        # Try payment.
        try:
          if order.total == 0: # FOR GROUPONS
            import datetime
            transaction_id = "GROUPON-%s" % str(datetime.datetime.now()).replace(' ','-')
          else:
            transaction_id = payment_handler(request, form, order)
        except checkout.CheckoutError, e:
          # Error in payment handler.
          order.delete()
          checkout_errors.append(e)
          if settings.SHOP_CHECKOUT_STEPS_CONFIRMATION:
            step -= 1
        else:
          # Finalize order - ``order.complete()`` performs
          # final cleanup of session and cart.
          # ``order_handler()`` can be defined by the
          # developer to implement custom order processing.
          # Then send the order email to the customer.
          order.transaction_id = transaction_id
          order.complete(request)
          order_handler(request, form, order)
          checkout.send_order_email(request, order)
          # Set the cookie for remembering address details
          # if the "remember" checkbox was checked.
          response = HttpResponseRedirect(reverse("complete"))
          if form.cleaned_data.get("remember") is not None:
            remembered = "%s:%s" % (sign(order.key), order.key)
            set_cookie(response, "remember", remembered,
                   secure=request.is_secure())
          else:
            response.delete_cookie("remember")


          # Now add the customer to the CAMPAIGN MONITOR
          # subscriber list if they opted in

          addtolist = False
          if authenticated:
            if request.user.get_profile().optin:
              addtolist = True
          else:
            if bool(form.cleaned_data.get("optin")):
              addtolist = True

          if addtolist:
            cm_api = CampaignMonitorApi(settings.CM_API_KEY, settings.CM_CLIENT_ID)
            listid = settings.CM_RETAIL_LIST_ID
            custom_fields = {}
            if wholesale_logged_in:
              listid = settings.CM_WHOLESALE_LIST_ID
              usertype = USER_TYPE_CHOICES[request.user.get_profile().user_type]
              custom_fields = {"CustomerType": usertype}
            try:
              cm_api.subscriber_add(
                listid,
                form.cleaned_data.get("billing_detail_email"),
                form.cleaned_data.get("billing_detail_first_name") + ' ' + form.cleaned_data.get("billing_detail_last_name"),
                custom_fields=custom_fields)
            except:
              pass


          return response

      # If any checkout errors, assign them to a new form and
      # re-run is_valid. If valid, then set form to the next step.
      form = form_class(request, step, initial=initial, data=data,
               errors=checkout_errors)
      if form.is_valid():
        step += 1
        form = form_class(request, step, initial=initial)

  step_vars = checkout.CHECKOUT_STEPS[step - 1]
  template = "shop/%s.html" % step_vars["template"]
  CHECKOUT_STEP_FIRST = step == checkout.CHECKOUT_STEP_FIRST
  context = {"form": form, "CHECKOUT_STEP_FIRST": CHECKOUT_STEP_FIRST,
         "step_title": step_vars["title"], "step_url": step_vars["url"],
         "steps": checkout.CHECKOUT_STEPS, "step": step,
         "wholesale_logged_in": wholesale_logged_in,
         "user_fullname": user_fullname,
         "last_step": step == checkout.CHECKOUT_STEP_LAST,
         #"uk_retail_free_delivery_minimum": settings.UK_RETAIL_FREE_DELIVERY_MINIMUM,
         #"uk_delivery_slow_rate": settings.UK_DELIVERY_SLOW_RATE,
         #"uk_delivery_fast_rate": settings.UK_DELIVERY_FAST_RATE,
         #"europe_delivery_slow_rate": settings.EUROPE_DELIVERY_SLOW_RATE,
         #"europe_delivery_fast_rate": settings.EUROPE_DELIVERY_FAST_RATE,
         #"world_delivery_slow_rate": settings.WORLD_DELIVERY_SLOW_RATE,
         #"world_delivery_fast_rate": settings.WORLD_DELIVERY_FAST_RATE,
         }
  return render_to_response(template, context, RequestContext(request))


def artist_directory(request, template="pages/artist_directory.html"):
  #shop_categories = Page.objects.published().filter(parent=shop_page).order_by("_order")
  content = Page.objects.get(slug='artists-directory').richtextpage.content

  selected_city = ""
  if u"city" in request.GET:
    selected_city = request.GET["city"]

  all_artists = CustomerProfile.objects.filter(user_type__in=settings.DIRECTORY_USER_TYPES).exclude(description__isnull=True).exclude(description__exact='')

  if selected_city:
    artists = CustomerProfile.objects.filter(user_type__in=settings.DIRECTORY_USER_TYPES, city=selected_city)
  else:
    artists = all_artists

  cities = []

  for artist in all_artists:
    artist.fullurl = ""
    if artist.website:
      if "http://" not in artist.website:
        artist.fullurl = "http://" + artist.website
      else:
        artist.fullurl = artist.website
    if artist.city not in cities:
      cities.append(artist.city)

  context = {
    "content": content,
    "artists": artists,
    "cities": cities,
    "selected_city": selected_city,
  }
  return render_to_response(template, context, RequestContext(request))



#def send_mail_template(subject, template, addr_from, addr_to, context=None,
#                       attachments=None, fail_silently=False):

def send_registration_confirmation_email(request):
  """
  Send order receipt email on successful order.
  """
  settings.use_editable()
  context = {"user": request.user, "site_url": settings.SITE_URL}
  template = "email/registration_confirmation"

  send_mail_template( "Thank you for registering with Manai",
                      template,
                      settings.SHOP_ORDER_FROM_EMAIL,
                      request.user.email,
                      context=context,
                      fail_silently=settings.DEBUG)


def shop_feed(request, template="shop/feed.xml"):
  settings.use_editable()
  products = RetailProduct.objects.published()
  context = {
    "products": products,
    "uk_slow_rate": settings.UK_DELIVERY_SLOW_RATE,
    "uk_fast_rate": settings.UK_DELIVERY_FAST_RATE,
    "site_url": settings.SITE_URL,
    "site_title": settings.SITE_TITLE,
  }
  return render_to_response(template, context, RequestContext(request))
