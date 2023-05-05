from django.db import models
from django.shortcuts import HttpResponseRedirect
from wagtail.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from sandbox.catalogue.models import ProductVariantPage


class Basket(models.Model):
    variant = models.ForeignKey(
        "catalogue.ProductVariantPage", on_delete=models.CASCADE, related_name="baskets"
    )
    quantity = models.PositiveIntegerField(default=1)
    session = models.CharField(max_length=255, null=True, blank=True)


class BasketPage(RoutablePageMixin, Page):

    max_count = 1

    @path("", name="basket")
    def index(self, request, *args, **kwargs):
        ctx = {}
        ctx["basket"] = Basket.objects.filter(session=request.session.session_key)
        ctx["basket_page"] = self
        ctx["has_items"] = ctx["basket"].exists()

        return self.render(request, *args, context_overrides=ctx)

    @path("add/<int:id>/", name="basket-add")
    def add(self, request, *args, **kwargs):
        variant = ProductVariantPage.objects.get(id=kwargs["id"])
        basket, created = Basket.objects.get_or_create(
            variant=variant, session=request.session.session_key
        )
        if not created:
            basket.quantity += 1
            basket.save()

        return HttpResponseRedirect(self.url)
    
    @path("remove/<int:id>/", name="basket-remove")
    def remove(self, request, *args, **kwargs):
        item = Basket.objects.get(id=kwargs["id"], session=request.session.session_key)
        item.delete()

        return HttpResponseRedirect(self.url)
    
    @path("increment/<int:id>/", name="basket-increment")
    def update(self, request, *args, **kwargs):
        item = Basket.objects.get(id=kwargs["id"], session=request.session.session_key)
        item.quantity += 1
        item.save()

        return HttpResponseRedirect(self.url)
    
    @path("decrement/<int:id>/", name="basket-decrement")
    def decrement(self, request, *args, **kwargs):
        item = Basket.objects.get(id=kwargs["id"], session=request.session.session_key)
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
        else:
            item.save()

        return HttpResponseRedirect(self.url)
