from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("top_habits", views.top_habit, name="top_habit"),
    path("add_comment/<int:profile_id>/", views.add_comment, name="add_comment"),
    path("add_habit", views.add_habit, name="add_habit"),
    path("delete_habit/", views.delete_habit, name="delete_habit"),
    path("update_log/", views.update_log, name="update_log"),
    path("dashboard/<int:id>", views.dashboard, name="dashboard"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]