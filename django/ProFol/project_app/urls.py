from django.urls import path, include
from . import views

# for email-smtp
from django.conf.urls import url

urlpatterns = [
    path('', views.index_redirect),
    # path('app/', views.index),
    path('app/login/', views.mng_login),

    path('app/', views.mng_personal),
    path('app/<int:pk>/', views.mng_project),
    path('app/<int:pk>/<str:category_title>/', views.mng_part),

    # portfolio
    path('app/portfolio/', views.user_portfolio),
    path('app/portfolio_detail/<int:pk>/', views.user_portfolio_detail),
    path('app/portfolio/edit_userportfolio_form/', views.edit_userportfolio_form),
    path('app/portfolio/edit_userportfolio/', views.edit_userportfolio),

    # create project, todolist
    path('app/create_project_form/', views.create_project_form),
    path('app/create_project/', views.create_project),
    path('app/<int:pk>/<str:category_title>/create_todo_form/', views.create_todo_form),
    path('app/<int:pk>/<str:category_title>/create_todo/', views.create_todo),
    path('app/<int:pk>/edit_project/edit_project_form/', views.edit_project_form),

    # finish_todo - redirection
    path('app/done/<int:todo_pk>', views.finish_todo),
    path('app/<int:pk>/<str:category_title>/done/<int:todo_pk>', views.finish_todo_part),

    # finish_project
    path('app/project_done/<int:pk>/', views.finish_project),

    # email smtp
    path('app/email_send/<int:pk>/', views.email_send),
    path('app/email_test/<int:pk>/',views.email_test),

    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<from_user>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<from_user_email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<pk>\d{1,5})/$',views.activate, name='activate'),
]
