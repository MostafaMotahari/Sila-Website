from typing import final
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from league.models import Game, Team, Tournament, GameImage, League
from account.models import User, Referee
from account.forms import UpdateUserForm, CreateUserForm, CreateGameForm
from account.mixins import AdminMixin, TopLevelAdminMixin, RefereeMixin

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


class CraeteGameView(LoginRequiredMixin, RefereeMixin, CreateView):
    model = Game
    form_class = CreateGameForm
    template_name = 'account/create_game.html'

    def get_form_kwargs(self):
        kwargs = super(CraeteGameView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        # Create new game
        new_game = Game.objects.create(
            league = League.objects.get(pk=request.POST['league']),
            home_team = Team.objects.get(pk=request.POST['home_team']),
            away_team = Team.objects.get(pk=request.POST['away_team']),
            referee = Referee.objects.get(pk=request.POST['referee']),
            starts_at = request.POST['starts_at'],
        )

        print(request.POST['starts_at'])

        # Get game images and save them to the database
        images = [(tipic_name, img) for tipic_name, img in request.FILES.items()]
        post_items = {tipic_name:value for tipic_name, value in request.POST.items()}


        for tipic_name, img in images:
            if "speed" in tipic_name:
                GameImage.objects.create(
                    game = new_game,
                    image = img,
                    name = post_items[tipic_name + "_name"],
                    type = "speed",
                )

            elif "power" in tipic_name:
                GameImage.objects.create(
                    game = new_game,
                    image = img,
                    name = post_items[tipic_name + "_name"],
                    type = "power",
                )

            elif "info" in tipic_name:
                GameImage.objects.create(
                    game = new_game,
                    image = img,
                    name = post_items[tipic_name + "_name"],
                    type = "info",
                )

            elif "legend" in tipic_name:
                GameImage.objects.create(
                    game = new_game,
                    image = img,
                    name = post_items[tipic_name + "_name"],
                    type = "legend",
                )

            else:
                GameImage.objects.create(
                    game = new_game,
                    image = img,
                    name = post_items[tipic_name + "_name"],
                    type = "search",
                )

        return HttpResponseRedirect(reverse_lazy('account:profile'))