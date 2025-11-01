from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Contact, Donation, FoodRequest, User


class BootstrapFormMixin:
    """Add Bootstrap CSS classes to form widgets."""

    def _init_bootstrap(self) -> None:
        for field in self.fields.values():
            if isinstance(field.widget, (forms.HiddenInput, forms.CheckboxInput)):
                continue
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing_classes + " form-control").strip()


class UserRegisterForm(BootstrapFormMixin, UserCreationForm):
    role = forms.ChoiceField(choices=User.Roles.choices)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "role", "contact_number", "address")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()


class DonationForm(BootstrapFormMixin, forms.ModelForm):
    available_till = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Donation
        fields = ("food_name", "description", "quantity", "address", "available_till")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
        if self.instance and self.instance.pk and self.instance.available_till:
            localized = timezone.localtime(self.instance.available_till)
            self.initial["available_till"] = localized.strftime("%Y-%m-%dT%H:%M")

    def clean_available_till(self):
        available_till = self.cleaned_data["available_till"]
        if available_till <= timezone.now():
            raise forms.ValidationError("Available till must be in the future.")
        return available_till


class FoodRequestForm(forms.ModelForm):
    class Meta:
        model = FoodRequest
        fields: list[str] = []


class ContactForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "email", "message")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
        self.fields["email"].required = True
        self.fields["message"].widget.attrs["rows"] = 4
        self.fields["message"].help_text = "Share details like quantity and pick-up times."
