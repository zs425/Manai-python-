from django.contrib import admin
from models import *
from cartridge.shop.forms import *
from cartridge.shop.admin import *
from cartridge.shop.models import Product, ProductImage, ProductVariation
from mezzanine.pages.models import Page
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.utils.encoding import force_unicode
from django.http import HttpResponseRedirect, HttpResponse
#from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin


class WholesaleProductAdminForm(forms.ModelForm):
    """
    Admin form for the WholesaleProduct model.
    """
    __metaclass__ = ProductAdminFormMetaclass

    class Meta:
        model = WholesaleProduct

    def __init__(self, *args, **kwargs):
        """
        Set the choices for each of the fields for product options.
        Also remove the current instance from choices for related and
        upsell products.
        """
        super(WholesaleProductAdminForm, self).__init__(*args, **kwargs)
        for field, options in ProductOption.objects.as_fields().items():
            self.fields[field].choices = make_choices(options)
        instance = kwargs.get("instance")
        if instance:
            queryset = WholesaleProduct.objects.exclude(id=instance.id)
            self.fields["related_products"].queryset = queryset
            self.fields["upsell_products"].queryset = queryset


class RetailProductAdminForm(forms.ModelForm):
    """
    Admin form for the RetailProduct model.
    """
    __metaclass__ = ProductAdminFormMetaclass

    class Meta:
        model = RetailProduct

    def __init__(self, *args, **kwargs):
        """
        Set the choices for each of the fields for product options.
        Also remove the current instance from choices for related and
        upsell products.
        """
        super(RetailProductAdminForm, self).__init__(*args, **kwargs)
        for field, options in ProductOption.objects.as_fields().items():
            self.fields[field].choices = make_choices(options)
        instance = kwargs.get("instance")
        if instance:
            queryset = RetailProduct.objects.exclude(id=instance.id)
            self.fields["related_products"].queryset = queryset
            self.fields["upsell_products"].queryset = queryset


# ACTIONS
# =======
def copy_product_to_wholesale(modeladmin, request, queryset):
  """ Add the selected products to the WholesaleProduct table """
  for product in queryset:
    p = Product.objects.get(id=product.id)
    p.title = p.title + " (Copy)"
    try:
        dup = WholesaleProduct.objects.get(slug=p.slug)
    except ObjectDoesNotExist:
        pass
    else:
        p.slug = p.slug + '-2'
    p.id = None
    p.save()

    from django.db import connection, transaction
    cursor = connection.cursor()

    cursor.execute("INSERT INTO custom_wholesaleproduct (product_ptr_id) values (%s)", [p.id])
    transaction.commit_unless_managed()

    # Looks like the following bit is unnecessary -- we still just end up with p.id!
    cursor.execute("SELECT product_ptr_id FROM custom_wholesaleproduct where product_ptr_id = %s", [p.id])
    row = cursor.fetchone()
    lastid = row[0]

    wholesale_cat = Page.objects.get(slug='wholesale-shop')
    cursor.execute("INSERT INTO shop_product_categories (product_id, category_id) values (%s, %s)", [p.id, wholesale_cat.id])
    transaction.commit_unless_managed()

    pvars = ProductVariation.objects.filter(product_id=product.id)
    for pvar in pvars:

      img = ProductImage.objects.get(id=pvar.image_id)
      img.id = None
      img.product_id = p.id
      img.save()

      pvar.id = None
      pvar.product_id = lastid
      pvar.sku = pvar.sku + '-2'
      pvar.save()


def copy_product_to_retail(modeladmin, request, queryset):
  """ Add the selected products to the RetailProduct table """
  for product in queryset:
    p = Product.objects.get(id=product.id)
    p.title = p.title + " (Copy)"
    try:
        dup = RetailProduct.objects.get(slug=p.slug)
    except ObjectDoesNotExist:
        pass
    else:
        p.slug = p.slug + '-2'
    p.id = None
    p.save()

    from django.db import connection, transaction
    cursor = connection.cursor()

    cursor.execute("INSERT INTO custom_retailproduct (product_ptr_id) values (%s)", [p.id])
    transaction.commit_unless_managed()

    cursor.execute("SELECT product_ptr_id FROM custom_retailproduct where product_ptr_id = %s", [p.id])
    row = cursor.fetchone()
    lastid = row[0]

    retail_cat = Page.objects.get(slug='retail-shop')
    cursor.execute("INSERT INTO shop_product_categories (product_id, category_id) values (%s, %s)", [p.id, retail_cat.id])
    transaction.commit_unless_managed()

    pvars = ProductVariation.objects.filter(product_id=product.id)
    for pvar in pvars:

      img = ProductImage.objects.get(id=pvar.image_id)
      img.id = None
      img.product_id = p.id
      img.save()

      pvar.id = None
      pvar.product_id = lastid
      pvar.sku = pvar.sku + '-2'
      pvar.save()

copy_product_to_wholesale.short_description = "Copy product to wholesale"
copy_product_to_retail.short_description = "Copy product to retail"


def nums_in_stock(obj):
    variations = ProductVariation.objects.filter(product=obj)
    s = ""
    for var in variations:
        s += '<div style="text-align:right;"><small>' + var.sku + '</small>: <strong>' + str(var.num_in_stock) + '</strong><br></div>'
    return s


def prices(obj):
    variations = ProductVariation.objects.filter(product=obj)
    s = ""
    for var in variations:
        s += '<div style="text-align:right;"><small>' + var.sku + '</small>: <strong>&pound;' + str(var.unit_price) + '</strong></div>'
    return s

nums_in_stock.allow_tags = True
prices.allow_tags = True


class WholesaleProductAdmin(DisplayableAdmin):

    class Media:
        js = ("cartridge/js/admin/product_variations.js","/static/js/admin/wholesale_categories.js")
        css = {"all": ("cartridge/css/admin/product.css",)}

    list_display = ("admin_thumb", "my_edit_link", "status", "ref", prices, nums_in_stock, "admin_link", )
    list_display_links = ("admin_thumb", )
    list_editable = ("status",)
    list_filter = ("status", "categories")
    filter_horizontal = ("categories", "related_products", "upsell_products")
    search_fields = ("title", "content", "categories__title", "variations__sku")
    inlines = (ProductImageAdmin, ProductVariationAdmin)
    form = WholesaleProductAdminForm
    fieldsets = product_fieldsets

    actions = [copy_product_to_retail]


    def my_edit_link(self, obj):
        return '<a href="%s" class="edit-link">%s</a>' % (obj.id, obj.title)
    my_edit_link.allow_tags = True


    def save_model(self, request, obj, form, change):
        """
        Store the product object for creating variations in save_formset.
        """
        super(WholesaleProductAdmin, self).save_model(request, obj, form, change)
        self._product = obj


    def save_formset(self, request, form, formset, change):
        """

        Here be dragons. We want to perform these steps sequentially:

        - Save variations formset
        - Run the required variation manager methods:
          (create_from_options, manage_empty, etc)
        - Save the images formset

        The variations formset needs to be saved first for the manager
        methods to have access to the correct variations. The images
        formset needs to be run last, because if images are deleted
        that are selected for variations, the variations formset will
        raise errors when saving due to invalid image selections. This
        gets addressed in the set_default_images method.

        An additional problem is the actual ordering of the inlines,
        which are in the reverse order for achieving the above. To
        address this, we store the images formset as an attribute, and
        then call save on it after the other required steps have
        occurred.

        """

        # Store the images formset for later saving, otherwise save the
        # formset.
        if formset.model == ProductImage:
            self._images_formset = formset
        else:
            super(WholesaleProductAdmin, self).save_formset(request, form, formset,
                                                   change)

        # Run each of the variation manager methods if we're saving
        # the variations formset.
        if formset.model == ProductVariation:

            # Build up selected options for new variations.
            options = dict([(f, request.POST.getlist(f)) for f in option_fields
                             if request.POST.getlist(f)])
            # Create a list of image IDs that have been marked to delete.
            deleted_images = [request.POST.get(f.replace("-DELETE", "-id"))
                              for f in request.POST if f.startswith("images-")
                              and f.endswith("-DELETE")]

            # Create new variations for selected options.
            self._product.variations.create_from_options(options)
            # Create a default variation if there are nonw.
            self._product.variations.manage_empty()
            # Copy duplicate fields (``Priced`` fields) from the default
            # variation to the prodyct.
            self._product.copy_default_variation()
            # Remove any images deleted just now from variations they're
            # assigned to, and set an image for any variations without one.
            self._product.variations.set_default_images(deleted_images)

            # Save the images formset stored previously.
            super(WholesaleProductAdmin, self).save_formset(request, form,
                                                 self._images_formset, change)

            # Run again to allow for no images existing previously, with
            # new images added which can be used as defaults for variations.
            self._product.variations.set_default_images(deleted_images)


    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        opts = obj._meta

        # Handle proxy models automatically created by .only() or .defer().
        # Refs #14529
        verbose_name = opts.verbose_name
        module_name = opts.module_name
        if obj._deferred:
            opts_ = opts.proxy_for_model._meta
            verbose_name = opts_.verbose_name
            module_name = opts_.module_name

        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {'name': force_unicode(verbose_name), 'obj': force_unicode(obj)}
        if "_continue" in request.POST:
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if "_popup" in request.REQUEST:
                return HttpResponseRedirect(request.path + "?_popup=1")
            else:
                return HttpResponseRedirect(request.path)
        elif "_saveasnew" in request.POST:
            msg = _('The %(name)s "%(obj)s" was added successfully. You may edit it again below.') % {'name': force_unicode(verbose_name), 'obj': obj}
            self.message_user(request, msg)
            return HttpResponseRedirect(reverse('admin:%s_%s_change' %
                                        (opts.app_label, module_name),
                                        args=(pk_value,),
                                        current_app=self.admin_site.name))
        elif "_addanother" in request.POST:
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(verbose_name)))
            return HttpResponseRedirect(reverse('admin:%s_%s_add' %
                                        (opts.app_label, module_name),
                                        current_app=self.admin_site.name))
        else:
            self.message_user(request, msg)
            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            if self.has_change_permission(request, None):
                q = request.GET.get('q', '')
                post_url = reverse('admin:%s_%s_changelist' %
                                   (opts.app_label, module_name),
                                   current_app=self.admin_site.name) + '?q=' + q
            else:
                post_url = reverse('admin:index',
                                   current_app=self.admin_site.name)
            return HttpResponseRedirect(post_url)



class RetailProductAdmin(DisplayableAdmin):

    class Media:
        js = ("cartridge/js/admin/product_variations.js","/static/js/admin/retail_categories.js")
        css = {"all": ("cartridge/css/admin/product.css",)}

    list_display = ("admin_thumb", "my_edit_link", "status", "ref", prices, nums_in_stock, "admin_link")
    list_display_links = ("admin_thumb", )
    list_editable = ("status",)
    list_filter = ("status", "categories")
    filter_horizontal = ("categories", "related_products", "upsell_products")
    search_fields = ("title", "content", "categories__title",
                     "variations__sku")
    inlines = (ProductImageAdmin, ProductVariationAdmin)
    form = RetailProductAdminForm
    fieldsets = product_fieldsets

    actions = [copy_product_to_wholesale]

    def my_edit_link(self, obj):
        return '<a href="%s" class="edit-link">%s</a>' % (obj.id, obj.title)
    my_edit_link.allow_tags = True


    def save_model(self, request, obj, form, change):
        """
        Store the product object for creating variations in save_formset.
        """
        super(RetailProductAdmin, self).save_model(request, obj, form, change)
        self._product = obj

    def save_formset(self, request, form, formset, change):
        """

        Here be dragons. We want to perform these steps sequentially:

        - Save variations formset
        - Run the required variation manager methods:
          (create_from_options, manage_empty, etc)
        - Save the images formset

        The variations formset needs to be saved first for the manager
        methods to have access to the correct variations. The images
        formset needs to be run last, because if images are deleted
        that are selected for variations, the variations formset will
        raise errors when saving due to invalid image selections. This
        gets addressed in the set_default_images method.

        An additional problem is the actual ordering of the inlines,
        which are in the reverse order for achieving the above. To
        address this, we store the images formset as an attribute, and
        then call save on it after the other required steps have
        occurred.

        """

        # Store the images formset for later saving, otherwise save the
        # formset.
        if formset.model == ProductImage:
            self._images_formset = formset
        else:
            super(RetailProductAdmin, self).save_formset(request, form, formset,
                                                   change)

        # Run each of the variation manager methods if we're saving
        # the variations formset.
        if formset.model == ProductVariation:

            # Build up selected options for new variations.
            options = dict([(f, request.POST.getlist(f)) for f in option_fields
                             if request.POST.getlist(f)])
            # Create a list of image IDs that have been marked to delete.
            deleted_images = [request.POST.get(f.replace("-DELETE", "-id"))
                              for f in request.POST if f.startswith("images-")
                              and f.endswith("-DELETE")]

            # Create new variations for selected options.
            self._product.variations.create_from_options(options)
            # Create a default variation if there are nonw.
            self._product.variations.manage_empty()
            # Copy duplicate fields (``Priced`` fields) from the default
            # variation to the prodyct.
            self._product.copy_default_variation()
            # Remove any images deleted just now from variations they're
            # assigned to, and set an image for any variations without one.
            self._product.variations.set_default_images(deleted_images)

            # Save the images formset stored previously.
            super(RetailProductAdmin, self).save_formset(request, form,
                                                 self._images_formset, change)

            # Run again to allow for no images existing previously, with
            # new images added which can be used as defaults for variations.
            self._product.variations.set_default_images(deleted_images)


    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        opts = obj._meta

        # Handle proxy models automatically created by .only() or .defer().
        # Refs #14529
        verbose_name = opts.verbose_name
        module_name = opts.module_name
        if obj._deferred:
            opts_ = opts.proxy_for_model._meta
            verbose_name = opts_.verbose_name
            module_name = opts_.module_name

        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {'name': force_unicode(verbose_name), 'obj': force_unicode(obj)}
        if "_continue" in request.POST:
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if "_popup" in request.REQUEST:
                return HttpResponseRedirect(request.path + "?_popup=1")
            else:
                return HttpResponseRedirect(request.path)
        elif "_saveasnew" in request.POST:
            msg = _('The %(name)s "%(obj)s" was added successfully. You may edit it again below.') % {'name': force_unicode(verbose_name), 'obj': obj}
            self.message_user(request, msg)
            return HttpResponseRedirect(reverse('admin:%s_%s_change' %
                                        (opts.app_label, module_name),
                                        args=(pk_value,),
                                        current_app=self.admin_site.name))
        elif "_addanother" in request.POST:
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(verbose_name)))
            return HttpResponseRedirect(reverse('admin:%s_%s_add' %
                                        (opts.app_label, module_name),
                                        current_app=self.admin_site.name))
        else:
            self.message_user(request, msg)
            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            if self.has_change_permission(request, None):
                post_url = reverse('admin:index',
                                   current_app=self.admin_site.name)
                try:
                    q = request.get_full_path().split("?")[1]
                    post_url = reverse('admin:%s_%s_changelist' %
                                   (opts.app_label, module_name),
                                   current_app=self.admin_site.name) + '?' + q
                except:
                    pass
            return HttpResponseRedirect(post_url)




admin.site.register(WholesaleProduct, WholesaleProductAdmin)
admin.site.register(RetailProduct, RetailProductAdmin)
admin.site.unregister(Product)