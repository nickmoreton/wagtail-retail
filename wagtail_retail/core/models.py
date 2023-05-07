from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import Page
from wagtail.coreutils import resolve_model_string
from wagtail.images import get_image_model_string
from wagtail.fields import RichTextField

from wagtail_retail.conf import WagtailRetailConf as conf


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


class BaseShopHomePage(Page):
    class Meta:
        abstract = True

    # Only one shop home page allowed
    # override this in your own models.py if you want to allow more than one
    max_count = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = "wagtail_retail/core/pages/shop_home_page.html"

    def get_product_pages(self):
        return (
            resolve_model_string(conf.product)
            .objects.live()
            .descendant_of(self)
            .specific()
        )

    def get_context(self, request):
        context = super().get_context(request)
        context["shop_title"] = self.get_shop_title()
        context["products"] = self.get_product_pages()
        return context

    def get_shop_title(self):
        config = RetailSettings.for_site(self.get_site())
        return config.title


class BaseProductPage(Page):
    class Meta:
        abstract = True

    subpage_types = [
        conf.variant,
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = "wagtail_retail/core/pages/product_page.html"

    main_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    summary = RichTextField(blank=True)
    body = RichTextField(blank=True)

    summary_panels = [
        MultiFieldPanel(
            [
                FieldPanel("main_image"),
                FieldPanel("summary"),
            ],
            heading="Summary",
            help_text="This information will be used in product listings",
        )
    ]

    content_panels = Page.content_panels + summary_panels + [
        FieldPanel("body"),
    ]


class BaseProductVariant(models.Model):
    class Meta:
        abstract = True

    def get_subpage_types(self):
        return self.subpage_types
