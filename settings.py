SITE_URL = 'https://manai.co.uk/'

# HDYH choices

GOOGLE = 'GO'
FACEBOOK = 'FB'
TWITTER = 'TW'
AUTUMN_FAIR = 'AF'
OLYMPIA_BEAUTY_SHOW = 'OB'
GOOGLE_SHOPPING = 'GS'
PAX = 'PX'
EMAIL_MARKETING = 'EM'
WORD_OF_MOUTH = 'WM'
OTHER = 'OT'

# User types
RETAIL_TRADER = 'RT'
GLITTER_TATTOO_ARTIST = 'GT'
BEAUTY_SALON = 'BS'
HENNA_ARTIST = 'HA'
EVENT_PLANNER = 'EP'
SCHOOL = 'SC'
CHARITY = 'CH'
FACE_PAINTER = 'FP'
NAIL_SALON = 'NS'
HAIRDRESSER = 'HD'
MAKEUP_ARTIST = 'MA'
ECOMMERCE_SHOP = 'ES'

HOW_DID_YOU_HEAR_CHOICES = (
    (GOOGLE, 'Google'),
    (FACEBOOK, 'Facebook'),
    (TWITTER, 'Twitter'),
    (AUTUMN_FAIR, 'Autumn Fair'),
    (OLYMPIA_BEAUTY_SHOW, 'Olympia Beauty Show'),
    (GOOGLE_SHOPPING, 'Google Shopping'),
    (PAX, 'The PA Exchange'),
    (EMAIL_MARKETING, 'Email marketing'),
    (WORD_OF_MOUTH, 'Word of Mouth'),
    (OTHER, 'Other (please specify)'),
)

USER_TYPE_CHOICES = (
    (RETAIL_TRADER, 'Retail Trader'),
    (GLITTER_TATTOO_ARTIST, 'Glitter Tattoo Artist (Pro Kit)'),
    (BEAUTY_SALON, 'Beauty Salon / Spa'),
    (HENNA_ARTIST, 'Henna Artist'),
    (EVENT_PLANNER, 'Event Planner'),
    (SCHOOL, 'Charity Fundraiser - School'),
    (CHARITY, 'Charity Fundraiser - Charities'),
    (FACE_PAINTER, 'Face Painter'),
    (NAIL_SALON, 'Nail Salon'),
    (HAIRDRESSER, 'Hair Dresser'),
    (MAKEUP_ARTIST, 'Make Up Artist'),
    (ECOMMERCE_SHOP, 'E-Commerce Shop'),
)

DIRECTORY_USER_TYPES = (
    GLITTER_TATTOO_ARTIST,
    HENNA_ARTIST,
    FACE_PAINTER,
    MAKEUP_ARTIST,
    )

######################
# CARTRIDGE SETTINGS #
######################

# The following settings are already defined in cartridge.conf.defaults
# with default values, but are common enough to be put here, commented
# out, for convenient overriding.

# Sequence of available credit card types for payment.
# SHOP_CARD_TYPES = ("Mastercard", "Visa", "Diners", "Amex")
SHOP_CARD_TYPES = ("Mastercard", "Visa")

# If True, users must create a login for the checkout process.
# SHOP_CHECKOUT_ACCOUNT_REQUIRED = False

# Set an alternative OrderForm class for the checkout process.
SHOP_CHECKOUT_FORM_CLASS = 'custom.forms.OrderForm'

# If True, the checkout process is split into separate
# billing/shipping and payment steps.
# SHOP_CHECKOUT_STEPS_SPLIT = True

# If True, the checkout process has a final confirmation step before
# completion.
# SHOP_CHECKOUT_STEPS_CONFIRMATION = True

# If False, there is no payment step on the checkout process.
# SHOP_PAYMENT_STEP_ENABLED = True

# Controls the formatting of monetary values accord to the locale
# module in the python standard library. If an empty string is
# used, will fall back to the system's locale.
# SHOP_CURRENCY_LOCALE = ""

# Default cost of shipping when no custom shipping is implemented.
# SHOP_DEFAULT_SHIPPING_VALUE = 10

# Dotted package path and class name of the function that
# is called on submit of the billing/shipping checkout step. This
# is where shipping calculation can be performed and set using the
# function ``cartridge.shop.utils.set_shipping``.
# SHOP_HANDLER_BILLING_SHIPPING = \
#                           "cartridge.shop.checkout.default_billship_handler"
SHOP_HANDLER_BILLING_SHIPPING = "custom.checkout.billship_handler"

# Dotted package path and class name of the function that
# is called once an order is successful and all of the order
# object's data has been created. This is where any custom order
# processing should be implemented.
# SHOP_HANDLER_ORDER = "cartridge.shop.checkout.default_order_handler"
SHOP_HANDLER_ORDER = "custom.checkout.order_handler"

# Dotted package path and class name of the function that
# is called on submit of the payment checkout step. This is where
# integration with a payment gateway should be implemented.
SHOP_HANDLER_PAYMENT = "cartridge.shop.payment.paypal.process"


# *********************** UNCOMMENT THIS
#SHOP_HANDLER_PAYMENT = "cartridge.shop.payment.paypal.process"
# *********************** UNCOMMENT THIS





# Sequence of value/name pairs for order statuses.
# SHOP_ORDER_STATUS_CHOICES = (
#     (1, "Unprocessed"),
#     (2, "Processed"),
# )

# Sequence of value/name pairs for types of product options,
# eg Size, Colour.
# SHOP_OPTION_TYPE_CHOICES = (
#     (1, "Size"),
#     (2, "Colour"),
# )

######################
# MEZZANINE SETTINGS #
######################

# The following settings are already defined in mezzanine.conf.defaults
# with default values, but are common enough to be put here, commented
# out, for convenient overriding.

# Controls the ordering and grouping of the admin menu.
#
ADMIN_MENU_ORDER = (
     ("Content", ("pages.Page", "blog.BlogPost", "generic.ThreadedComment", ("Media Library", "fb_browse"),)),
     ("Shop", ("custom.RetailProduct", "custom.WholesaleProduct", "shop.ProductOption", "shop.DiscountCode", "shop.Sale", "shop.Order")),
     #("Shop", ("shop.Product", "shop.ProductOption", "shop.DiscountCode", "shop.Sale", "shop.Order")),
     ("Site", ("sites.Site", "redirects.Redirect", "conf.Setting")),
     ("Users", ("auth.User", "auth.Group",)),
)

# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.
#
DASHBOARD_TAGS = (
     ("mezzanine_tags.app_list",),
     ("comment_tags.recent_comments",),
     ("mezzanine_tags.recent_actions",),
)

# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#
# EXTRA_MODEL_FIELDS = (
#     (
#         # Dotted path to field.
#         "mezzanine.blog.models.BlogPost.image",
#         # Dotted path to field class.
#         "somelib.fields.ImageField",
#         # Positional args for field class.
#         ("Image",),
#         # Keyword args for field class.
#         {"blank": True, "upload_to": "blog"},
#     ),
#     # Example of adding a field to *all* of Mezzanine's content types:
#     (
#         "mezzanine.pages.models.Page.another_field",
#         "IntegerField", # 'django.db.models.' is implied if path is omitted.
#         ("Another name",),
#         {"blank": True, "default": 1},
#     ),
# )


# Setting to turn on featured images for blog posts. Defaults to False.
#
# BLOG_USE_FEATURED_IMAGE = True

# If ``True``, users will be automatically redirected to HTTPS
# for the URLs specified by the ``SSL_FORCE_URL_PREFIXES`` setting.
#
# SSL_ENABLED = True

# Host name that the site should always be accessed via that matches
# the SSL certificate.
#
# SSL_FORCE_HOST = "www.example.com"

# Sequence of URL prefixes that will be forced to run over
# SSL when ``SSL_ENABLED`` is ``True``. i.e.
# ('/admin', '/example') would force all URLs beginning with
# /admin or /example to run over SSL. Defaults to:
#
# SSL_FORCE_URL_PREFIXES = ("/admin", "/account", "/shop/checkout",)

# If True, the south application will be automatically added to the
# INSTALLED_APPS setting. This setting is not defined in
# mezzanine.conf.defaults as is the case with the above settings.
USE_SOUTH = True


########################
# MAIN DJANGO SETTINGS #
########################

# People who get code error notifications.
# In the format (('Full Name', 'email@example.com'),
#                ('Full Name', 'anotheremail@example.com'))
ADMINS = (
    ('Alistair Robinson', 'alistair.robinson@gmail.com'),
)
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = "7543957f-c466-449e-8e81-280bfcc7a2751314cad5-0936-4dae-9794-c1c9e317eb328be6f228-c84e-4672-aaf5-528b21aeaf26"

# Tuple of IP addresses, as strings, that:
#   * See debug comments, when DEBUG is true
#   * Receive x-headers
INTERNAL_IPS = ("127.0.0.1",)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

AUTHENTICATION_BACKENDS = ("mezzanine.core.auth_backends.MezzanineBackend",)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.",
        # DB name or path to database file if using sqlite3.
        "NAME": "",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

#################
# USER PROFILES #
#################

AUTH_PROFILE_MODULE = 'custom.CustomerProfile'

ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = (
    "image",
    "description",
)

#########
# PATHS #
#########

import os

# Full filesystem path to the project.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

# Put strings here, like "/home/html/django_templates"
# or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)


################
# APPLICATIONS #
################

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "cartridge.shop",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.pages",
    "mezzanine.galleries",
    "mezzanine.twitter",
    "mezzanine.accounts",
    #"mezzanine.mobile",
    "typogrify",
    #"captcha",
    "custom",
    "buildyourown",
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "mezzanine.conf.context_processors.settings",
)

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    "mezzanine.core.middleware.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "cartridge.shop.middleware.ShopMiddleware",
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
)


# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"


#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}


##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError:
    pass


####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable.
from mezzanine.utils.conf import set_dynamic_settings
set_dynamic_settings(globals())
