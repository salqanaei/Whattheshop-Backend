from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("cart", views.CartAPIView)
router.register("cartitem", views.CartItemView)
router.register("profile", views.ProfileView)
router.register("review", views.ReviewView)
router.register("product", views.ListAPIView)
router.register("remove", views.CartItemDelete)
router.register("revieworder", views.ReviewOrder)
router.register("address", views.AddressViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('register/', views.UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('checkout/', views.CartStatusCheckout.as_view(), name='checkout'),
    path('revorder/', views.CartStatus.as_view(), name='review'),
    path('return/', views.CartStatusReturn.as_view(), name='review'),
    path('', include(router.urls))
]


if settings.DEBUG:
	urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)