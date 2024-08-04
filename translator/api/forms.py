from django import forms

LANGUAGES = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish", "Portuguese", "Romanian", "Russian", "Turkish"]
LANGUAGE_CHOICES = [(lang, lang) for lang in LANGUAGES]


class LanguageForm(forms.Form):
    word = forms.CharField(label="Enter the word you want to translate:", max_length=100)
    language_source = forms.ChoiceField(label="Your language", choices=LANGUAGE_CHOICES)
    language_target = forms.ChoiceField(label="Language to translate", choices=LANGUAGE_CHOICES)
