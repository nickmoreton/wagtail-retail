from django import template
from wagtail_retail.core.models import RetailSettings

register = template.Library()


@register.inclusion_tag('wagtail_retail/core/tags/shop_title_tag.html', takes_context=True)
def shop_title(context):
    request = context['request']
    title = RetailSettings.for_request(request).title
    return {
        'title': title,
    }
