from django import template

register = template.Library()


@register.filter
def lookup(obj, field_name):
    try:
        return getattr(obj, field_name)
    except (AttributeError, TypeError):
        try:
            return obj[field_name]
        except (KeyError, TypeError):
            return None


@register.filter
def dict_key(d, key):
    return d.get(key, '')
