from django import forms


class NewsletterForm(forms.Form):
    name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={"autocomplete": "off", "tabindex": "-1"}),
    )

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Unable to subscribe with this submission.")
        return value