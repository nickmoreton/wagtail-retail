from django.conf import settings
from wagtail.coreutils import resolve_model_string


class WagtailRetailConf:
    shop_home = getattr(settings, "WAGTAIL_RETAIL_SHOP_HOME_PAGE_MODEL", "shop.ShopHomePage")
    product = getattr(settings, "WAGTAIL_RETAIL_PRODUCT_PAGE_MODEL", "shop.ProductPage")
    variant = getattr(settings, "WAGTAIL_RETAIL_PRODUCT_VARIANT_MODEL", "shop.ProductVariantPage")
    
    @property
    def shop_home_model():
        return resolve_model_string(WagtailRetailConf.shop_home)
    
    @property
    def product_model():
        return resolve_model_string(WagtailRetailConf.product)
    
    @property
    def variant_model():
        return resolve_model_string(WagtailRetailConf.variant)
