from django import template
import os

register = template.Library()


@register.simple_tag
def get_env_extras(key):
    os.environ.get(key)
