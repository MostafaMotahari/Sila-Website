from typing import final
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from league.models import Team, Tournament
from account.models import User
from account.forms import UpdateUserForm, CreateUserForm
from account.mixins import AdminMixin, TopLevelAdminMixin

# Create your views here.

class TeamsListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'account/index.html'
    context_object_name = 'context'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['teams'] = Team.objects.order_by('-points').all()
        context['teammates'] = User.objects.filter(team=self.request.user.team).all()
        context['teammates_count'] = User.objects.filter(team=self.request.user.team).count()
        context['trophy_count'] = Team.objects.filter(captain=self.request.user).count()
        return context


class TournamentView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'account/tournament.html'
    context_object_name = 'context'


class TournamentRegisterView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'account/tournament_register.html'
    context_object_name = 'context'

    def get(self, request, pk=None, *args, **kwargs):
        tournament = get_object_or_404(Tournament, pk=pk)
        tournament.participants.add(request.user)
        tournament.save()
        return HttpResponseRedirect(reverse_lazy('account:tournament'))


class SelectUserView(LoginRequiredMixin, AdminMixin, ListView):
    model = User
    template_name = 'account/select_user.html'
    context_object_name = 'users'


class UpdateUserView(LoginRequiredMixin, AdminMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'account/select_user.html'

    def get_form_kwargs(self):
        kwargs = super(UpdateUserView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        form = UpdateUserForm(request.POST, instance=user, user=request.user)

        if form.is_valid():

            final_user = form.save(commit=False)
            final_user.save()
            return HttpResponseRedirect(reverse_lazy('account:profile'))

        return HttpResponse('Form is not valid') # Edit this later.


class CreateUserView(LoginRequiredMixin, TopLevelAdminMixin, CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'account/create_user.html'

    # def form_valid(self, form):
    #     user = form.save(commit=False)
    #     user.set_password(form.cleaned_data['password'])
    #     user.save()
    #     return HttpResponseRedirect(reverse_lazy('account:profile'))

    def get_form_kwargs(self):
        kwargs = super(CreateUserView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs