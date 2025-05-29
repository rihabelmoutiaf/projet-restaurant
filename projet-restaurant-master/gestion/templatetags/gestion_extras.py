from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """Get an item from a dictionary by key in templates"""
    return dictionary.get(key)