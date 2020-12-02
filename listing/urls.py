from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'listing'

urlpatterns = [
                  # path('listings', views.ListingsView.as_view(), name='listings'),
                  # path('listings', views.index, name='listings'),
                  path('listings', views.listings_view, name='listings'),
                  path('listings/table', views.listings_table_view, name='table'),
                  path('mylistings', views.users_listings_view, name='mylistings'),
                  path('listings/my', views.ListingsView.as_view(), name='my'),
                  # path('select', views.user_name, name='select'),
                  path('listings/create', views.new_listing_form, name='create'),
                  path('listings/<id>/delete', views.delete_listing, name='delete'),
                  path('listings/<id>/', views.detail_view, name='detail'),
                  path('listings/<id>/join', views.join_group, name='join'),
                  path('listings/<id>/leave', views.leave_group, name='leave'),
                  path('listings/<id>/join/zoom', views.join_zoom, name='zoom'),
                  path('listings/<id>/edit/', views.edit, name='edit'),
                  # path('listings/<id>/edit/', views.listing_update, name='edit'),
                  # path('listings/<id>/edit', views.edit_listing, name='edit'),
                  # path('listings/<int:id>/edit/', views.EditListingView.as_view(), name='edit'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
