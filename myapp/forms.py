from django import forms


class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8, '8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks'),
    ]
    name = forms.CharField(max_length=100, required=False, label='Student Name')
    length = forms.TypedChoiceField(widget=forms.RadioSelect, choices=LENGTH_CHOICES, coerce=int,
                                    label='Preferred course duration:', required=False, empty_value=0)
    max_price = forms.IntegerField(label='Maximum Price', min_value=0)
