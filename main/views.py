from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages

from .models import User, Rule, News, Comment
from .forms import UserForm, NewsForm, UserUpdateForm, CommentForm, UserAuthenticationForm


def index(request):
    news = News.objects.all()
    if request.path_info == '/by_comments/':
        news = sorted(news, key=lambda entry: entry.comment_set.count(), reverse=True)
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
    print(request.path_info)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your news added')
            return redirect('main:index')
    form = NewsForm(initial={'author': request.user.pk})
    return render(request, 'main/news.html', {'form': form})


@login_required(login_url='main:login')
def delete_news(request, pk):
    news = News.objects.get(id=pk)
    news.delete()
    return redirect('main:personal', pk=request.user.pk)


class EditNews(UpdateView):
    model = News
    template_name = 'main/news.html'
    form_class = NewsForm
    success_url = reverse_lazy('main:add_news')

    def get_context_data(self, **kwargs):
        print(self.request.method)
        context = super().get_context_data()
        return context


def detail(request, pk):
    news = News.objects.get(id=pk)
    comments = []
    comments_lvl1 = Comment.objects.filter(news_id=pk, comment=0)
    for comment_lvl1 in comments_lvl1:
        comments_lvl2 = Comment.objects.filter(comment=comment_lvl1.pk)
        comms_lvl2 = []
        for comment_lvl2 in comments_lvl2:
            comms_lvl3 = []
            _search_comments(comment_lvl2, comms_lvl3)
            comms_lvl2.append({'value': comment_lvl2, 'comms_lvl3': comms_lvl3})
        comments.append({'value': comment_lvl1, 'comms_lvl2': comms_lvl2})
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment added')
            return redirect('main:detail', pk=pk)
    initial = {'news': pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.first_name
    else:
        initial['author'] = 'Anonymous'
    form = CommentForm(initial=initial)
    context = {'news': news, 'form': form, 'comments': comments}
    return render(request, 'main/detail.html', context)


def _search_comments(comment, comms_lvl3):
    entries = Comment.objects.filter(comment=comment.pk)
    if not entries:
        return
    for entry in entries:
        comms_lvl3.append(entry)
        _search_comments(entry, comms_lvl3)




class Login(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserAuthenticationForm()
        return context
