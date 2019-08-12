from django import forms


class TilForm(forms.Form):
    subject = forms.CharField(label='Title', max_length=160)
    content = forms.CharField(label='What did I learn today?',
                              widget=forms.Textarea, max_length=800)
    # four tags separated by a comma
    tags = forms.CharField(label='Tags (comma separated, maximum: 4)',
                           required=False,
                           max_length=43)
    public = forms.BooleanField(label='Public', required=False)
