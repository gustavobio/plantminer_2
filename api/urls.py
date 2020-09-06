from django.urls import path, include
from . import views
from users import views as user_views

urlpatterns = [
    path('suggest/<search_str>/', views.suggestion),
    path('details/<search_str>/', views.details),
    path('details/<search_str>/id/', views.details, kwargs = {'id': True}),
    path('details/<search_str>/suggest/', views.details, kwargs={'suggest': True}),
    path('details/<search_str>/family/', views.details, kwargs={'family': True}),
    path('details/<search_str>/genus/', views.details, kwargs={'genus': True}),
    path('details/<search_str>/specific_epiteth/', views.details, kwargs={'specific_epiteth': True}),
    path('details/<search_str>/scientific_name/', views.details, kwargs={'scientific_name': True}),
    path('details/<search_str>/infra_epiteth/', views.details, kwargs={'infra_epiteth': True}),
    path('details/<search_str>/taxon_rank/', views.details, kwargs={'taxon_rank': True}),
    path('details/<search_str>/authorship/', views.details, kwargs={'authorship': True}),
    path('details/<search_str>/taxon_status/', views.details, kwargs={'taxon_status': True}),
    path('details/<search_str>/name_status/', views.details, kwargs={'name_status': True}),
    path('details/<search_str>/threat_status/', views.details, kwargs={'threat_status': True}),
    path('details/<search_str>/establishment/', views.details, kwargs={'establishment': True}),
    path('details/<search_str>/endemism/', views.details, kwargs={'endemism': True}),
    path('details/<search_str>/life_form/', views.details, kwargs={'life_form': True}),
    path('details/<search_str>/habitat/', views.details, kwargs={'habitat': True}),
    path('details/<search_str>/vegetation_type/', views.details, kwargs={'vegetation_type': True}),
    path('details/<search_str>/occurrence/', views.details, kwargs={'occurrence': True}),
    path('details/<search_str>/domain/', views.details, kwargs={'domain': True}),
    path('expand/<short_name>/', views.expand_name),
    path('synonyms/<search_str>/', views.synonyms),
    path('remove_authors/<taxon>/', views.remove_authors),
    path('profile/', user_views.profile_api),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('shorten/<search_str>/author/', views.shorten, kwargs={'author': True}),
    path('shorten/<search_str>/', views.shorten, kwargs={'author': False}),
    path('plantminer/', views.plantminer, name = 'plantminer'),
    path('user-list/', views.user_list, name = 'user-list'),
]