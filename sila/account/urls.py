from tempfile import TemporaryFile
from django.contrib.auth import views
from django.urls import path
from account.views import (
    TeamsListView ,
    TournamentView ,
    SelectUserView ,
    UpdateUserView ,
    TournamentRegisterView ,
    CreateUserView,
    CraeteMatchView,
    MatchManagerView,
    MatchEditView
)

app_name = "account"

urlpatterns = [
    path("", TeamsListView.as_view(), name="profile"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("tours/", TournamentView.as_view(), name="tournament"),
    path("tours/register/<int:pk>", TournamentRegisterView.as_view(), name="tournament_register"),
    path("user-control/", SelectUserView.as_view(), name="user_control"),
    path("user-control/update-user/<int:pk>", UpdateUserView.as_view(), name="user_update"),
    path("register-user/", CreateUserView.as_view(), name="register_user"),
    path("create-match/", CraeteMatchView.as_view(), name="create_match"),
    path("match-manager/", MatchManagerView.as_view(), name="match_manager"),
    path("match-manager/edit/<int:pk>", MatchEditView.as_view(), name="match_editor"),
    
    # path("user-control/update-user/", UpdateUserView.as_view(), name="update_user"),
    # path("logout/", views.LogoutView.as_view(), name="logout"),
    # path(
    #     "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    # ),
    # path(
    #     "password_change/done/",
    #     views.PasswordChangeDoneView.as_view(),
    #     name="password_change_done",
    # ),
    # path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    # path(
    #     "password_reset/done/",
    #     views.PasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "reset/<uidb64>/<token>/",
    #     views.PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "reset/done/",
    #     views.PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
]
