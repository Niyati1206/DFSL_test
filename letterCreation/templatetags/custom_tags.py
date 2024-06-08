# yourapp/templatetags/custom_tags.py
from django import template
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal, InvalidOperation
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal, InvalidOperation

register = template.Library()

@register.simple_tag
def multiply(value1, value2):
    try:
        value1_decimal = Decimal(value1)
        value2_decimal = Decimal(value2)
        result = value1_decimal * value2_decimal
        return result if result.is_finite() else None
    except (InvalidOperation, TypeError):
        return None
    
# /*@register.simple_tag
# def sum_of_products(subproducts, unit_price_attr, quantity_attr):
#     total = 0
#     for subproduct in subproducts:
#         total += getattr(subproduct, str(unit_price_attr)) * getattr(subproduct, str(quantity_attr))
#     return total
    
@register.filter
def sum_of_products(queryset, field_name):
    return sum(getattr(obj, field_name) for obj in queryset)


@register.simple_tag
def multiply_and_add(unit_price, quantity, gst_value):
    try:
        total_price = Decimal(unit_price) * Decimal(quantity) + Decimal(gst_value)
        return total_price
    except (InvalidOperation, TypeError):
        return None
    
@register.filter
def calc(value, arg):
    return value * arg



# @register.filter
# def multiply_and_add_total_basic_price(subproducts_group):
#     total_basic_price = 0
#     for subproduct in subproducts_group:
#         quotationitem = subproduct.quotationitem_set.first()
#         if quotationitem:
#             total_basic_price += quotationitem.unit_price * subproduct.quantity
#     return total_basic_price

@register.filter
def multiply_and_add_total_basic_price(subproducts):
    total_price = 0
    for subproduct in subproducts:
        total_price += subproduct.quotationitem_set.first().unit_price * subproduct.quantity
    return total_price


@register.filter
def total_basic_price(subproducts):
    total_price = sum(subproduct.subproductquotationinfo.unit_price for subproduct in subproducts)
    return total_price if total_price.is_finite() else None

@register.filter
def total_price_inclusive(subproducts):
    total = sum((subproduct.subproductquotationinfo.unit_price * subproduct.quantity) + subproduct.subproductquotationinfo.gst_value for subproduct in subproducts)
    return total if total.is_finite() else None

@register.filter
def group_by_amc_provider(subproducts):
    result = {}
    for subproduct in subproducts:
        provider_name = subproduct.amc_provider
        if provider_name not in result:
            result[provider_name] = []
        result[provider_name].append(subproduct)
    return result.items()


@register.filter
def unique_amc_providers(subproducts):
    unique_providers = set()
    result = []
    for subproduct in subproducts:
        provider_name = subproduct.amc_provider.name
        if provider_name not in unique_providers:
            result.append(provider_name)
            unique_providers.add(provider_name)
    return ' व '.join(result)

@register.filter
def calc(value, arg):
    try:
        value_decimal = Decimal(value)
        arg_decimal = Decimal(arg)
        # Multiply the values
        result = value_decimal * arg_decimal
        # Round the result to the nearest integer
        result_rounded = result.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        return result_rounded
    except (InvalidOperation, TypeError):
        return None


@register.filter
def multiply_and_add(value, arg):
    return value * arg

@register.filter
def calculate_total_price(unit_price, quantity):
    try:
        unit_price_decimal = Decimal(unit_price)
        quantity_decimal = Decimal(quantity)
        total_price = unit_price_decimal * quantity_decimal
        return total_price
    except (InvalidOperation, TypeError):
        return None

@register.filter
def unique_values(queryset, field_name):
    return queryset.values_list(field_name, flat=True).distinct()


@register.filter(name='group_by_amc_provider')
def group_by_amc_provider(subproducts):
    groups = {}
    for subproduct in subproducts:
        amc_provider_name = subproduct.amc_provider.name
        if amc_provider_name not in groups:
            groups[amc_provider_name] = []
        groups[amc_provider_name].append(subproduct)
    return groups.items()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_last(value, arg):
    return value[arg-1] if value else None