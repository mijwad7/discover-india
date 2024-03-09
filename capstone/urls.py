from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("view_states", views.view_states, name="view_states"),
    path("<str:state>/category/<str:category>", views.state, name="state"),
    path("view_place/<str:place_id>", views.view_place, name="view_place"),
    path("<str:state>/states_categories", views.states_categories, name="states_categories"),
    path("view_categories", views.view_categories, name="view_categories"),
    path("category/<str:category>", views.category, name="category"),
    path("add_place", views.add_place, name="add_place"),
    path("user_place/<int:id>", views.user_place, name="user_place"),
    path('places/mark/<int:place_id>/', views.mark_place_to_visit, name='mark_place_to_visit'),
    path("visit", views.visit, name="visit"),
]