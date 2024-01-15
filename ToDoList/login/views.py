from typing import Any
from django.urls import reverse_lazy   
from .models import Task

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import RedirectView


from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import logout, login





# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'login/loginPage.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')  
    
    
class LogOutView(RedirectView):
    url = reverse_lazy('tasks')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs) 
    
    
class TaskList(LoginRequiredMixin, ListView):
    model=Task
    context_object_name = 'tasks'

    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user).order_by('due')
        context['count'] = context['tasks'].filter(complete=False).count()
        
        searchItem = self.request.GET.get('search-area') or ""
        
        if searchItem:
            context['tasks'] = context['tasks'].filter(title__startswith=searchItem)
        
        context['searchItem'] = searchItem
            
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'object'
    template_name = 'login/task.html'
    

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete', 'reminder', 'due']
    success_url = reverse_lazy('tasks') #redirect the user
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete', 'reminder', 'due']
    success_url = reverse_lazy('tasks') #redirect the user


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks') #redirect the user


class RegisterPage(FormView):
    template_name = 'login/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(request=self.request, user=user)
            
        return super(RegisterPage, self).form_valid(form)
    

