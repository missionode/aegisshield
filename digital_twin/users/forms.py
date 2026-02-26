from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'full_name', 'location')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-5 py-3.5 rounded-xl border-2 border-slate-100 focus:border-deep-moss/50 focus:ring-4 focus:ring-deep-moss/10 outline-none transition-all text-deep-moss placeholder:text-slate-300 bg-slate-50 font-medium'
            })
