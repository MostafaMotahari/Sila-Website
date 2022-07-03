from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from league.models import Match, Team, Tournament, MatchImage, League
from account.models import User, Referee, Report
from account.forms import UpdateUserForm, CreateUserForm, CreateMatchForm, MatchEditForm, CreateReportForm
from account.mixins import AdminMixin, TopLevelAdminMixin, RefereeMixin, ReporterMixin
from account.utilities import iranDateTime

from datetime import time, datetime

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

    def get_form_kwargs(self):
        kwargs = super(CreateUserView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class CraeteMatchView(LoginRequiredMixin, RefereeMixin, CreateView):
    model = Match
    form_class = CreateMatchForm
    template_name = 'account/create_match.html'

    def get_form_kwargs(self):
        kwargs = super(CraeteMatchView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        # Create new match
        new_match = Match.objects.create(
            league = League.objects.get(pk=request.POST['league']),
            home_team = Team.objects.get(pk=request.POST['home_team']),
            away_team = Team.objects.get(pk=request.POST['away_team']),
            referee = Referee.objects.get(pk=request.POST['referee']),
            starts_at = request.POST['starts_at'],
        )

        print(request.POST['starts_at'])

        # Get match images and save them to the database
        images = [(tipic_name, img) for tipic_name, img in request.FILES.items()]
        post_items = {tipic_name:value for tipic_name, value in request.POST.items()}


        for tipic_name, img in images:
            if "speed" in tipic_name:
                MatchImage.objects.create(
                    match = new_match,
                    image = img,
                    name = post_items[tipic_name + "_name"],
                    type = "speed",
                )

            elif "power" in tipic_name:
                MatchImage.objects.create(
                    match = new_match,
                    image = img,
                    name = post_items[tipic_name + "_name"],
                    type = "power",
                )

            elif "info" in tipic_name:
                MatchImage.objects.create(
                    match = new_match,
                    image = img,
                    name = post_items[tipic_name + "_name"],
                    type = "info",
                )

            elif "legend" in tipic_name:
                MatchImage.objects.create(
                    match = new_match,
                    image = img,
                    name = post_items[tipic_name + "_name"],
                    type = "legend",
                )

            else:
                MatchImage.objects.create(
                    match = new_match,
                    image = img,
                    name = post_items[tipic_name + "_name"],
                    type = "search",
                )

        return HttpResponseRedirect(reverse_lazy('account:profile'))

    
class MatchManagerView(LoginRequiredMixin, RefereeMixin, ListView):
    model = Match
    paginate_by = 10
    template_name = 'account/match_manager.html'
    context_object_name = 'matchs'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        referee = Referee.objects.get(user=self.request.user)
        matchs = Match.objects.filter(referee=referee).order_by('-starts_at')
        matchs_and_status = [
            (
                match, 
                "finished" if iranDateTime(match.starts_at) < iranDateTime(datetime.now()) else "pending"
            ) for match in matchs
        ]

        context['matchs'] = matchs_and_status
        return context


class MatchEditView(LoginRequiredMixin, RefereeMixin, UpdateView):
    model = Match
    form_class = MatchEditForm
    template_name = 'account/match_manager.html'

    def get_form_kwargs(self):
        kwargs = super(MatchEditView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, pk, *args, **kwargs):
        match = get_object_or_404(Match, pk=pk)
        form = MatchEditForm(request.POST, instance=match, user=request.user)

        if form.is_valid():

            final_user = form.save(commit=False)
            final_user.save()
            return HttpResponseRedirect(reverse_lazy('account:profile'))

        return HttpResponse('Form is not valid') # Edit this later.


class CreateReportView(LoginRequiredMixin, ReporterMixin, CreateView):
    model = Report
    form_class = CreateReportForm
    template_name = "account/create_report.html"
    success_url = reverse_lazy("account:profile")


class ReportListView(LoginRequiredMixin, ReporterMixin, ListView):
    model = Report
    paginate_by = 10
    template_name = "account/report_editor.html"
    context_object_name = 'reports'


class UpdateReportView(LoginRequiredMixin, ReporterMixin, UpdateView):
    model = Report
    form_class = CreateReportForm
    template_name = "account/report_editor.html"
    success_url = reverse_lazy("account:profile")