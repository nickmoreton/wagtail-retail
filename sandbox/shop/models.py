from wagtail.models import Page
from wagtail_retail.core.models import (
    BaseShopHomePage,
    BaseProductPage,
    BaseProductVariant,
)


class ShopHomePage(BaseShopHomePage):
    pass


class ProductPage(BaseProductPage):
    pass


class ProductVariantPage(BaseProductVariant, Page):
    parent_page_types = [ProductPage]
    # subpage_types = []
