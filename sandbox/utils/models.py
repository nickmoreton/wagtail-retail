from django.db import models

from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import PageChooserPanel


@register_setting
class BasketSettings(BaseSiteSetting):
    basket_page = models.ForeignKey(
        "basket.BasketPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        PageChooserPanel("basket_page", ["basket.BasketPage"]),
    ]
