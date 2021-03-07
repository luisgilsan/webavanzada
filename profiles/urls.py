from django.urls import path
from . import views
from .views import ProfileListView, ProfileDetailView

profiles_patterns = ([
    path('', ProfileListView.as_view(), name='profiles'),
    path('<username>/', ProfileDetailView.as_view(), name='profile'),
    
],'profiles')