from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate

from .models import User, Rule, News
from .forms import UserForm, NewsForm


def index(request):
    news = News.objects.all()
    context = {'news': news}
    return render(request, 'main/index.html', context)


class Registration(CreateView):
    model = User
    template_name = 'main/registrar.html'
    form_class = UserForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        response_redirect = super().form_valid(form)
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user:
            login(self.request, user)
        return response_redirect

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rules'] = Rule.objects.all()
        return context


class EditUser(UpdateView):
    model = User
    template_name = 'main/personal.html'
    form_class = UserForm
    success_url = reverse_lazy('main:registrar')


class AddNews(CreateView):
    model = News
    template_name = 'main/news.html'
    form_class = NewsForm
    success_url = reverse_lazy('main:add_news')


class EditNews(UpdateView):
    model = News
    template_name = 'main/news.html'
    form_class = NewsForm
    success_url = reverse_lazy('main:add_news')

