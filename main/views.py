from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import User, Rule, News, Comment
from .forms import UserForm, NewsForm, UserUpdateForm, CommentForm


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
            messages.add_message(self.request, messages.SUCCESS, f'Hello, {user.first_name}!')
        return response_redirect

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rules'] = Rule.objects.all()
        return context


class EditUser(UpdateView, LoginRequiredMixin):
    model = User
    template_name = 'main/personal.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        response_redirect = super().form_valid(form)
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, 'Your data updated')
        return response_redirect

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_news = News.objects.filter(author_id=self.request.user.pk)
        context['news'] = user_news
        return context


@login_required(login_url='main:login')
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your news added')
            return redirect('main:index')
    form = NewsForm(initial={'author': request.user.pk})
    return render(request, 'main/news.html', {'form': form})


class EditNews(UpdateView):
    model = News
    template_name = 'main/news.html'
    form_class = NewsForm
    success_url = reverse_lazy('main:add_news')


def detail(request, pk):
    news = News.objects.get(id=pk)
    return render(request, 'main/detail.html', {'news': news})


