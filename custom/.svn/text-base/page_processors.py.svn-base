# This works but currently I'm not using it

#from django.http import HttpResponseRedirect
from mezzanine.conf import settings
from mezzanine.pages.page_processors import processor_for
from mezzanine.pages.models import Page
from cartridge.shop.models import Category, Product
#from reviews.models import Review

""" 
These are processors which add context to Page-type pages, i.e., not the home page
The homepage context is defined in custom.views.home
And site-wide context is added in custom.context_processors
"""

@processor_for(Category)
def cat_processor(request, page):
  """ Get the subcategories of a category """
  shop_page = Page.objects.get(slug="retail-shop")
  shop_slug = "retail-shop"
  wholesale_logged_in = False
  user_fullname = ""
  if 'wholesale-shop' in request.path:
    shop_page = Page.objects.get(slug="wholesale-shop")
    shop_slug = "wholesale-shop"
    if request.user.is_authenticated():
      user_fullname = " ".join([request.user.first_name, request.user.last_name])
      if request.user.has_perm('custom.wholesale_customer'):
        wholesale_logged_in = True
  shop_categories = Page.objects.published().filter(parent=shop_page).order_by("_order")
  subcategories = Page.objects.published().filter(parent=page).order_by("_order")
  siblingcategories = Page.objects.published().filter(parent=page.parent).order_by("_order")
  for cat in subcategories:
    cat.product_count = Product.objects.published().filter(categories=cat).count()
  referrer = ''
  try:

    # **************************************
    # TODO
    # got to exclude off-site referrers
    # BUT it might be ok
    # **************************************

    referrer=request.META['HTTP_REFERER'].split('/')[3:]
    referrer = "/".join(referrer)[:-1]
  except:
    pass

  current_page = "1"
  if "page" in request.GET:
     current_page = request.GET["page"]

  first_time = True
  if u"visited_before" in request.session:
    del request.session["visited_before"]
    first_time = False
  request.session["visited_before"] = True

  settings.use_editable()
  wholesale_minimum_spend = int(float(settings.WHOLESALE_MINIMUM_SPEND))

  return {
    "shop_categories": shop_categories,
    "subcategories": subcategories,
    "siblingcategories": siblingcategories,
    "referrer": referrer,
    "shop_slug": shop_slug,
    "wholesale_logged_in": wholesale_logged_in,
    "user_fullname": user_fullname, 
    "first_time": first_time,
    "current_page": current_page,
    "wholesale_minimum_spend": wholesale_minimum_spend,
    }


#@processor_for(Gallery)
#def cat_processor(request, page):

# All Page-type pages
"""
@processor_for(RichTextPage)
def homepage_processor(request, page):

  return {
    "foo": "bar",
    }
"""

# Slug-specific
"""
@processor_for("our-story")
def homepage_processor(request, page):

  return {
    "foo": "bar",
    }
"""
# But that's not very useful cos you'd have a custom view anyway if there was something special going on, so...

# It's useful when there's a custom page model. Say we have a model VideosPage...
"""
@processor_for(VideosPage)
def homepage_processor(request, page):

  return {
    "foo": "bar",
    }
"""