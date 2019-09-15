from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("cart", views.CartAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('product-list/', views.ListAPIView.as_view(), name='list'),
    path('product-detail/<int:product_id>/', views.DetailAPIView.as_view(), name='detail'),
    path('register/', views.UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='register'),
    path('', include(router.urls))
]


if settings.DEBUG:
	urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)