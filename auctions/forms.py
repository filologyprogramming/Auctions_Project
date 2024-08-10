from django import forms
from .models import Listing, Comment

# Create listing form
class ListingForm(forms.ModelForm):
    class Meta:
        # Access Listing model and take fields which will be included in the form
        model = Listing
        fields = [
            'name', 
            'price', 
            'description',
            'image',
            'condition',
            'category',
            ]
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name_form'}),
            'price': forms.TextInput(attrs={'id': 'price_form'}),
            'description': forms.Textarea(attrs={'id': 'description_form'}),
            'image': forms.FileInput(attrs={'id': 'image_form'}),
            'condition': forms.Select(attrs={'id': 'condition_form'}),
            'category': forms.Select(attrs={'id': 'category_form'})
        }

# Create a comment form
class CommentForm(forms.ModelForm):
    class Meta:
        # Access comment model and take fields which will be included in the form
        model = Comment
        fields = [
            'comment'
        ]
        widgets = {
            'comment': forms.Textarea(attrs={'id': 'comment_form'}),
        }

# Choose a category form:
class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'category'
        ]
