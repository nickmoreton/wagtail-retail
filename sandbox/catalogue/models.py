from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from sandbox.utils.models import BasketSettings


class ProductVariantPage(Page):
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("image"),
    ]

    parent_page_types = ["catalogue.ProductPage"]

    def __str__(self):
        return self.title


class ProductPage(Page):
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("image"),
    ]

    subpage_types = ["catalogue.ProductVariantPage"]

    def __str__(self):
        return self.title
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["variants"] = ProductVariantPage.objects.live().descendant_of(self)
        context["basket_page"] = BasketSettings.for_request(request).basket_page
        return context
