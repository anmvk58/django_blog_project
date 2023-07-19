from django.urls import path
from . import  views

urlpatterns = [
    # path bellow deprecated with function in views, which replaced by class inherit View/ListView
    # path('', views.starting_page), name="starting-page"),
    
    path('', views.StartingPageView.as_view(), name="starting-page"),
    path('post', views.AllPostView.as_view(), name="post-page"),
    path('post/<slug:slug>', views.SinglePostView.as_view(), name="post-detail-page")
]