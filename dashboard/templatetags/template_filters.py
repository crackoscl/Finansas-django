from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def format_amount(value):
    try:
        amount_int = int(value)
        return f"${amount_int:,}".replace(',', '.')
    except (ValueError, TypeError):
        return value  # Retorna el valor original si no se puede convertir