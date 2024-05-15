from django.urls import path, include
from . import views
from .admin import admin_site
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'banners', views.BannerViewSet)
router.register(r'school', views.SchoolViewSet)
router.register(r'admissions', views.AdmissionsViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'streams', views.StreamViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'scores', views.ScoreViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'faqs', views.FAQViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'messages', views.MessageViewSet, basename="messages")

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
    path('postfb/', views.test)
]