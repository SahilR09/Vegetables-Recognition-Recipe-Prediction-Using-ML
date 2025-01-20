from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.SignupPage,name='signup'),
    path('about/', views.about, name='about'),
    path('login/',views.LoginPage,name='login'),
    path('prediction/', views.prediction, name='prediction'),
    path('home/',views.HomePage,name='home'),
    path('logout/',views.LogoutPage,name='logout'),
    path('profile/',views.ProfilePage,name='profile'),
    path('favourites/', views.favourites, name='favourites'),
    path('add_to_favourites/<str:recipe_name>/', views.add_to_favourites, name='add_to_favourites'),
    path('favourites/remove/<int:recipe_id>/', views.remove_from_favourites, name='remove_from_favourites'),

]
