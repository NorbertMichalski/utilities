from django import template
from django.utils.safestring import mark_safe
import json
register = template.Library()

@register.filter(is_safe=True)
def to_json(value):
    return sorted(json.loads(value).items(), key=lambda x: x[1], reverse=True)


@register.filter(is_safe=True)
def lookup(d, key):
    return d[key]


