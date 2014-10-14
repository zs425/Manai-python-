from django.shortcuts import render_to_response
from django.template import RequestContext
from cartridge.shop.models import Product, ProductVariation
from mezzanine.pages.models import Page
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.core.templatetags.mezzanine_tags import thumbnail
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder

def main(request, template="pages/buildyourown.html"):
  step = "basekits"
  subcatslug = ""
  subcat = ""

  if u"step" in request.GET:
    if request.GET["step"]:
      step = request.GET["step"]

  if u"subcat" in request.GET:
    subcatslug = request.GET["subcat"]

  shop_slug = 'retail-shop'
  wholesale_logged_in = False
  user_fullname = ""
  if request.user.is_authenticated():
    user_fullname = " ".join([request.user.first_name, request.user.last_name])
    if request.user.has_perm('custom.wholesale_customer'):
      wholesale_logged_in = True
      shop_slug = 'wholesale-shop'

  stencil_cat_slug = shop_slug + '/glitter-tattoo-stencils'
  glitter_cat_slug = shop_slug + '/cosmetic-body-glitter'

  products = []
  subcats = []
  cat = ""
  if step == "stencils":
    request.session["nextstep"] = 'stencils'
    if not subcatslug:
      subcatslug = stencil_cat_slug
    cat = Page.objects.get(slug=subcatslug, status=CONTENT_STATUS_PUBLISHED)
    subcats = Page.objects.filter(parent=cat, status=CONTENT_STATUS_PUBLISHED)
    products = Product.objects.filter(category=cat, status=CONTENT_STATUS_PUBLISHED)
  elif step == "glitters":
    request.session["nextstep"] = 'glitters'
    if not subcatslug:
      subcatslug = glitter_cat_slug
    cat = Page.objects.get(slug=subcatslug, status=CONTENT_STATUS_PUBLISHED)
    subcats = Page.objects.filter(parent=cat, status=CONTENT_STATUS_PUBLISHED)
    products = Product.objects.filter(category=cat, status=CONTENT_STATUS_PUBLISHED)
  else:
    cat = Page.objects.get(slug='%s/base-kits' % (shop_slug), status=CONTENT_STATUS_PUBLISHED)
    products = Product.objects.filter(category=cat, status=CONTENT_STATUS_PUBLISHED).order_by("ref")

  context = {
    "buildyourown": True,
    "products": products,
    "step": step,
    "subcats": subcats,
    "subcat": subcat, 
    "cat": cat,
    "wholesale_logged_in": wholesale_logged_in,
  }
  return render_to_response(template, context, RequestContext(request))


def productview(request, template="pages/product_pop.html"):
  id = 0
  if u"id" in request.GET:
    id = request.GET["id"]
    product = Product.objects.get(id=id)
    variations = product.variations.all()

    context = {
      "product": product,
      "variations": variations,
      "has_available_variations": any([v.has_price() for v in variations]),
    }
    return render_to_response(template, context, RequestContext(request))
  return HttpResponseRedirect("/")


def get_variation_price(request):
  sku = ""
  if request.is_ajax():
    if u"sku" in request.GET:
      sku = request.GET["sku"]
      price = ProductVariation.objects.get(sku=sku).unit_price
      return HttpResponse(price)
  return HttpResponse("0")


def add_to_cart(request):
  if request.is_ajax():
  
    shop_slug = 'retail-shop'
    wholesale_logged_in = False
    user_fullname = ""
    if request.user.is_authenticated():
      user_fullname = " ".join([request.user.first_name, request.user.last_name])
      if request.user.has_perm('custom.wholesale_customer'):
        wholesale_logged_in = True
        shop_slug = 'wholesale-shop'

    sku = ""
    if u"sku" and u"quantity" and u"nextstep" in request.POST:
      sku = request.POST["sku"]
      quantity = request.POST["quantity"]
      nextstep = request.POST["nextstep"]
      if nextstep:
        request.session['build_your_own'] = True
      variation = ProductVariation.objects.get(sku=sku)
      request.cart.add_item(variation, int(quantity), shop_slug)
      return HttpResponse(request.cart.total_price())
  
  return HttpResponse("No")