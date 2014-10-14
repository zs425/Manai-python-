
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from mezzanine.core.views import direct_to_template


admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = patterns("",

    # SHOP FEED
    url(r"^retail-shop/feed/$", 'custom.views.shop_feed', name="shop_feed"),

    # WHOLESALE
    url("^wholesale-shop/accounts/signup/$", "custom.views.wholesale_signup", name="wholesale_signup"),
    url("^wholesale-shop/accounts/login/$", "custom.views.wholesale_login", name="wholesale_login"),
    url("^wholesale-shop/accounts/logout/$", "custom.views.wholesale_logout", name="retail_logout"),
    url("^wholesale-shop/product/(?P<slug>.*)/$", "custom.views.wholesale_product", name="wholesale_product"),    
    
    #url("^wholesale-shop/wishlist/$", "cartridge.shop.views.wishlist", name="wholesale_wishlist"),
    #url("^wholesale-shop/invoice/(?P<order_id>\d+)/$", "cartridge.shop.views.invoice", name="wholesale_invoice"),

    
    # RETAIL
    url("^retail-shop/accounts/signup/$", "custom.views.retail_signup", name="retail_signup"),
    url("^retail-shop/accounts/login/$", "custom.views.retail_login", name="retail_login"),
    url("^retail-shop/accounts/logout/$", "custom.views.retail_logout", name="retail_logout"),
    url("^retail-shop/product/(?P<slug>.*)/$", "custom.views.retail_product", name="retail_product"),

    # GENERAL SHOP
    url("^retail-shop/", include("cartridge.shop.urls"), name="retail_shop"),
    url("^wholesale-shop/", include("cartridge.shop.urls"), name="wholesale_shop"),
    url("^basket/$", "custom.views.cart", name="basket"),
    url("^checkout/$", "custom.views.checkout_steps", name="checkout"),
    url("^complete/$", "cartridge.shop.views.complete", name="complete"),

    # OTHER
    url("^subscribed/$", direct_to_template, {'template': 'misc/subscriber_thanks.html'}),
    url("^artists-directory/$", "custom.views.artist_directory", name="artist_directory"),
    url("^build-your-own-kit/add_to_cart/$", "buildyourown.views.add_to_cart", name="pop_add_to_cart"),
    url("^build-your-own-kit/", "buildyourown.views.main", name="build_your_own"),
    url("^product-pop/$", "buildyourown.views.productview", name="product_pop"),

    # AJAX
    url("^get_variation_price/$", "buildyourown.views.get_variation_price", name="get_variation_price"),
    url("^add_to_cart/$", "custom.views.add_to_cart", name="add_to_cart"),


    ("^admin/", include(admin.site.urls)),
    #("^shop/", include("cartridge.shop.urls")),
    url("^account/orders/$", "cartridge.shop.views.order_history", name="shop_order_history"),

    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    # HOMEPAGE AS STATIC TEMPLATE
    # ---------------------------
    # This pattern simply loads the index.html template. It isn't
    # commented out like the others, so it's the default. You only need
    # one homepage pattern, so if you use a different one, comment this
    # one out.

    #url("^$", direct_to_template, {"template": "index.html"}, name="home"),

    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    # ---------------------------------------------
    # This pattern gives us a normal ``Page`` object, so that your
    # homepage can be managed via the page tree in the admin. If you
    # use this pattern, you'll need to create a page in the page tree,
    # and specify its URL (in the Meta Data section) as "home", which
    # is the name used below in the ``{"slug": "home"}`` part. Make
    # sure to uncheck "show in navigation" when you create the page,
    # since the link to the homepage is always hard-coded into all the
    # page menus that display navigation on the site.

    url("^$", "custom.views.home", {"slug": "/"}, name="home"),

    # HOMEPAGE FOR A BLOG-ONLY SITE
    # -----------------------------
    # This pattern points the homepage to the blog post listing page,
    # and is useful for sites that are primarily blogs. If you use this
    # pattern, you'll also need to set BLOG_SLUG = "" in your
    # ``settings.py`` module, and delete the blog page object from the
    # page tree in the admin if it was installed.

    # url("^$", "mezzanine.blog.views.blog_post_list", name="home"),

    # MEZZANINE'S URLS
    # ----------------
    # Note: ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!
    # If you'd like more granular control over the patterns in
    # ``mezzanine.urls``, go right ahead and take the parts you want
    # from it, and use them directly below instead of using
    # ``mezzanine.urls``.
    ("^", include("mezzanine.urls")),

)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler500 = "mezzanine.core.views.server_error"
