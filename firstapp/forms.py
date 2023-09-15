from django import forms
from .models import *
from django.forms import formset_factory,modelformset_factory

class CodeForm(forms.ModelForm):
    class Meta:
        model = Results
        fields = "__all__"
        
        
        def __init__(self,*args,**kwargs):
            super(CodeForm,self).__init__(*args,**kwargs)

CodeFormSet = modelformset_factory(Results,form=CodeForm)