from django import forms
from .models import ServicesList, ServiceCategory


class ServiceForm(forms.ModelForm):
    """
    A form used by the super user to add services to the website, outside of the admin view
    """
    class Meta:
        model = ServicesList
        fields = '__all__'


class ServiceCategoryForm(forms.ModelForm):
    """
    A form used by the super user to add a new category of service to the website,
    outside of the admin view.
    """
    class Meta:
        model = ServiceCategory
        fields = '__all__'
