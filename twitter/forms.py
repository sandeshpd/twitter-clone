from django import forms
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from .models import Tweet, Profile, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# Upload Profile Picture
class ProfilePicForm(forms.ModelForm):
    profile_picture = forms.ImageField(label = 'Profile Picture')
    profile_bio = forms.CharField(label = 'Profile Bio',
                                  required = False,
                                  widget=forms.widgets.Textarea(
                                      attrs={
                                          'placeholder': 'Enter your bio to show who you are to your friends.',
                                          'class': 'form-control',
                                      }
                                  ))
    website_link = forms.CharField(label = 'Your Website URL',
                                   required = False,
                                   widget=forms.widgets.TextInput(
                                      attrs={
                                          'placeholder': 'Link to your personal website',
                                          'class': 'form-control',
                                      }
                                  ))
    facebook_link = forms.CharField(label = 'Facebook',
                                    required = False,
                                   widget=forms.widgets.TextInput(
                                      attrs={
                                          'placeholder': 'Your Facebook Profile Link',
                                          'class': 'form-control',
                                      }
                                  ))
    instagram_link = forms.CharField(label = 'Instagram',
                                     required = False,
                                   widget=forms.widgets.TextInput(
                                      attrs={
                                          'placeholder': 'Your Instagram Profile Link',
                                          'class': 'form-control',
                                      }
                                  ))
    linkedin_link = forms.CharField(label = 'LinkedIn',
                                    required=False,
                                    widget=forms.widgets.TextInput(
                                    attrs={
                                        'placeholder': 'Your LinkedIn Profile Link',
                                        'class': 'form-control',
                                    }
                                ))

    class Meta:
        model = Profile
        fields = ('profile_picture', 'profile_bio', 'website_link', 'facebook_link', 'instagram_link', 'linkedin_link',)

# User Tweeting form
class TweetForm(forms.ModelForm):
    # tb__pfp = forms.ImageField(label='PFP',)
    body = forms.CharField(required=True,
                           widget=forms.widgets.TextInput(
                               attrs={
                                   'placeholder': 'What is happening?!',
                                   'class': 'tweetbox__input',
                                   # 'style': 'box-sizing: border-box; padding: 0; padding-top: 2px; padding-left: 2px; text-align: left; width: 50em; height: 5em; vertical-align: top;'
                                   'style': 'flex: 1; margin-top: 10px; margin-left: 10px; border: none; outline: 1px solid #ddd; width: 50em; height: 5em; ',
                               }
                           ),
                           label='',
                        )
    class Meta:
        model = Tweet
        exclude = ('user','likes','bookmarks','comment_count',)

class CommentForm(forms.ModelForm):
    body = forms.CharField(required=True,
                              widget=forms.widgets.Textarea(
                                  attrs={
                                      'placeholder':'Post your reply...',
                                      'class':'form-control',
                                      'style':'height: 150px; border-color: #484848;',
                                  }
                              ),
                              label=''
                            )
    class Meta:
        model = Comment
        fields = ['body',]

    def save(self,commit = True):
        instance = super(CommentForm, self).save(commit = False)
        if commit:
            instance.save()
        self.cleaned_data['body'] = ''
        return instance

# User Signup form
# FIXME: User entered data do not get stored in DB and SignUp page keeps redirecting to itself
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update(
            {
                'class': 'md-text-field__input',
                'id': 'first_name',
            }
        )

        self.fields['last_name'].widget.attrs.update(
            {
                'class': 'md-text-field__input',
                'id': 'last_name',
            }
        )

        self.fields['username'].widget.attrs.update(
            {
                'class': 'md-text-field__input',
                'id': 'username',
            }
        )

        self.fields['email'].widget.attrs.update(
            {
                'class': 'md-text-field__input',
                'id': 'email',
            }
        )

        self.fields['password1'].widget.attrs.update(
            {
                'class': 'md-text-field__input',
                'id': 'password1',
            }
        )

        self.fields['password2'].widget.attrs.update(
            {
                'class': 'md-text-field__input',
                'id': 'password2',
            }
        )


# User Update Form
class UpdateUserForm(UserChangeForm):
    email = forms.EmailField(label='Email', 
                             widget=forms.TextInput(
                                 attrs={
                                     'class':'form-control',
                                     'placeholder':'Your Valid Email Address',
                                 }))
    first_name = forms.CharField(label='First Name',
                                 max_length=50,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class':'form-control',
                                         'placeholder':'Your First Name',
                                     }))
    last_name = forms.CharField(label='Last Name',
                                 max_length=60,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class':'form-control',
                                         'placeholder':'Your Last Name',
                                     }))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
    
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Your User Name'
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password'].label = ''
        self.fields['password'].help_text = '<p>If you want to change the password, <a href="{}">click here</a>.</p>'.format(reverse_lazy('change_password'))