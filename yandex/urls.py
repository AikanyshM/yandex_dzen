from django.contrib import admin
from django.urls import path, include
from main_app import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('post', views.PostViewSet, basename='post')
router.register('comment', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('get-token/', obtain_auth_token),
    path('', include(router.urls)), 
    path('register/', views.UserCreateAPIView.as_view()),
    path('create_admin/', views.AdminCreateAPIView.as_view()),
    
]