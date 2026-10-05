"""Template filters for the collection page."""
from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()

# Written as an escape so this module stays pure ASCII on disk regardless of
# how the file was saved or which editor touched it.
INR_SIGN = "\u20b9"


def _group_indian(digits: str) -> str:
    """Group a digit string the Indian way: 1250000 -> '12,50,000'.

    Django's built-in intcomma applies Western grouping and renders the same
    number as '1,250,000'. On an INR amount for an Indian showroom that is
    simply the wrong number, so the grouping is done by hand: the last three
    digits stand alone, and everything to the left of them is chunked in pairs.
    """
    if len(digits) <= 3:
        return digits

    head, tail = digits[:-3], digits[-3:]

    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)

    return ",".join(parts + [tail])


@register.filter(name="inr")
def inr(value):
    """Render a Decimal as an Indian-rupee price, e.g. 1250000 -> Rs 12,50,000.

    Paise are dropped: a car price quoted to the rupee is the convention, and
    trailing '.00' on every card is noise.
    """
    if value is None or value == "":
        return ""

    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return ""

    rounded = amount.quantize(Decimal("1"))
    sign = "-" if rounded < 0 else ""

    return f"{sign}{INR_SIGN}{_group_indian(str(abs(rounded)))}"
