from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import LanguageForm
from .translator import get_translation

# Create your views here.
class MainView(FormView):
    template_name = "api/index.html"
    form_class = LanguageForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        word = form.cleaned_data['word']
        language_source = form.cleaned_data['language_source']
        language_target = form.cleaned_data['language_target']

        context = self.get_context_data(form=form)
        translations, examples = get_translation(language_source, language_target, word)
        context.update({
            'translations': translations,
            'examples': examples
        })

        return self.render_to_response(context)