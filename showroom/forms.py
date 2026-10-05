from django import forms

from .models import Vehicle


class CompactClearableFileInput(forms.ClearableFileInput):
    """ClearableFileInput with the two inline labels shortened.

    Django renders this widget as bare text with no element of its own:

        Currently: <a>vehicles/2026/09/sample-evo.png</a>
        <input type=checkbox><label>Clear</label><br>
        Change: <input type=file>

    Because the two labels are text nodes they cannot be styled or hidden from
    CSS, and in a three-column grid the cell is only about 270-300px wide --
    "Currently:" alone spends 60px of it, which is what forced the stored
    filename onto a second line and made the edit form taller than the add form
    by enough to overflow a 768px screen.

    They are class attributes rather than __init__ arguments, so shortening them
    means subclassing, not passing keywords to the constructor. The second one
    is `input_text`, not `change_text` -- Django 5.2 renamed it, and setting
    `change_text` silently does nothing.
    """

    initial_text = "Saved"
    input_text = "New"


class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle

        # Order is the order the fields render in: identity, then customer,
        # then money, then state.
        #
        # Every name here must exist on Vehicle. Naming a field the model does
        # not have is not a validation error -- Django raises FieldError while
        # building the class, which breaks the import of showroom.forms and so
        # breaks EVERY command, including `manage.py check` and `runserver`.
        fields = [
            "bmw_id",
            "model",
            "variant",
            "customer_name",
            "registration_number",
            "price",
            "year",
            "status",
            "image",
        ]

        widgets = {
            "bmw_id": forms.TextInput(
                attrs={
                    "placeholder": "BMW ID",
                    "class": "form-control",
                }
            ),

            "model": forms.TextInput(
                attrs={
                    "placeholder": "Model",
                    "class": "form-control",
                }
            ),

            "variant": forms.TextInput(
                attrs={
                    "placeholder": "Variant",
                    "class": "form-control",
                }
            ),

            "customer_name": forms.TextInput(
                attrs={
                    "placeholder": "Customer Name",
                    "class": "form-control",
                }
            ),

            "registration_number": forms.TextInput(
                attrs={
                    "placeholder": "Registration Number",
                    "class": "form-control",
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "placeholder": "Price",
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "year": forms.NumberInput(
                attrs={
                    "placeholder": "Year",
                    "class": "form-control",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "image": CompactClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
        }