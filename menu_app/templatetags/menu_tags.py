from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from ..models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    menu_items = MenuItem.objects.filter(name=menu_name)

    current_path = request.path
    active_items = set()


    def check_active(item):
        if item.url == current_path:
            active_items.add(item.url)
            return True
        if item.children.exists():
            for child in item.children.all():
                if check_active(child):
                    active_items.add(item.url)
                    return True
        return False

    for item in menu_items:
        check_active(item)

    return mark_safe(build_menu(menu_items, active_items))


def build_menu(items, active_items, parent=None):
    menu_html = ''
    for item in items.filter(parent=parent):
        is_active = item.url in active_items
        menu_html += f'<li class="{"active" if is_active else ""}">'
        menu_html += f'<a href="{item.get_absolute_url()}">{item.title}</a>'
        if item.children.exists():
            menu_html += '<ul>' + build_menu(items, active_items, item) + '</ul>'
        menu_html += '</li>'

    return menu_html
