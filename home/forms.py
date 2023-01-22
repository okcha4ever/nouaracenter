from dataclasses import field
from django import forms
from .models import Contact



PARENT_CHOICES =(
    ("1", "ولي أمر"),
    ("2", "تلميذ"),
)



class ContactForm(forms.ModelForm):
    IsParent: forms.ChoiceField(choices = PARENT_CHOICES)
    class Meta:
        model = Contact
        fields = '__all__'
        labels = {
            'Full_Name': '',
            'Email': '',
            'IsParent': '',
            'Content': '',
            }

        widgets = {
            'Full_Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "الإسم الكامل",}),
            'Email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
            'IsParent': forms.Select(attrs={'class': 'form-control form-select'}),
            'Content': forms.Textarea(attrs={"class": "form-control", 'placeholder': 'المحتوى', "rows":5, "cols":20}),
        }
            
        