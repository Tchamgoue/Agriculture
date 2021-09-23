from django import forms


class CropsRegistration(forms.Form):
    name = forms.CharField(max_length=128, label='Name')
    bionomical_name = forms.CharField(max_length=128, label='Bionomical Name')
    spread = forms.DecimalField(label="Spread(diameter)")
    row_spacing = forms.DecimalField(label="Row Spacing")
    height = forms.DecimalField(label="Height")
    taxon = forms.CharField(label="Taxon")
    sun_requirement_id = forms.ChoiceField(label="Sun Requirements", choices=[('1', 1)])
    growing_degree_days = forms.DecimalField(label="Growing Degree Days")
    sowing_method = forms.CharField(label="Sowing Method", max_length=512)
