from django import template

register = template.Library()


STATUS_BADGE_MAP = {
    "available": "success",
    "claimed": "secondary",
    "expired": "dark",
    "pending": "warning",
    "accepted": "success",
    "rejected": "danger",
}


@register.filter
def status_badge_class(value: str) -> str:
    """Return Bootstrap badge class for status labels."""
    return STATUS_BADGE_MAP.get(value, "secondary")


@register.filter
def add_class(field, css_class: str):
    """Append CSS classes to a form field widget."""
    existing = field.field.widget.attrs.get("class", "")
    combined = f"{existing} {css_class}".strip()
    field.field.widget.attrs["class"] = combined
    return field
