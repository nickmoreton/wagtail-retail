from django.apps import apps
from django.db import models
from django.conf import settings
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import Page
from wagtail.coreutils import resolve_model_string


@register_setting(icon="clipboard-list")
class RetailSettings(BaseSiteSetting):
    title = models.CharField(
        "Shop Title",
        max_length=255,
        blank=True,
        null=True,
    )

    panels = [
        FieldPanel("title"),
    ]


class BaseShopConfig:
    shop_model_string = settings.WAGTAIL_RETAIL_SHOP_HOME_PAGE_MODEL
    product_model_string = settings.WAGTAIL_RETAIL_PRODUCT_PAGE_MODEL
    variant_model_string = settings.WAGTAIL_RETAIL_PRODUCT_VARIANT_MODEL


class BaseShopHomePage(BaseShopConfig, Page):
    class Meta:
        abstract = True

    def get_product_pages(self):
        return resolve_model_string(self.product_model_string).objects.live().descendant_of(
            self
        )
    
    def get_context(self, request):
        context = super().get_context(request)
        context["products"] = self.get_product_pages()
        return context


class BaseProductPage(BaseShopConfig, Page):
    class Meta:
        abstract = True

    subpage_types = [
        BaseShopConfig.variant_model_string,
    ]


class BaseProductVariant(BaseShopConfig, models.Model):
    class Meta:
        abstract = True

    def get_subpage_types(self):
        return self.subpage_types
