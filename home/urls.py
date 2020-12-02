from django.urls import path, include

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required as auth
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
import profile_page.views as profile_page_views
import contact_form.views as contact_form_views


app_name = 'home'
urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('', views.HomeView.as_view(), name='home'),
    # path('listings', views.ListingsView.as_view(), name='listings'),
    path('accounts/', include('allauth.urls')),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path(r'users/<slug>/', profile_page_views.ProfileView.as_view(), name='profile'),
    path(r'edit_profile', auth(profile_page_views.UserProfileEdit.as_view()), name='edit_profile'),
    path(r'edit_zoom_profile', auth(profile_page_views.UserProfileZoomEdit.as_view()), name='edit_zoom_profile'),
    path('profile/editing', profile_page_views.edit_profile, name='editing_profile'),
    path('profile/editing/zoomID', profile_page_views.edit_zoom_profile, name='editing_zoom_profile'),
    path('contact', contact_form_views.contact, name='contact')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)