from django.contrib import admin
from django.urls import path, include

# ✅ For media files
from django.conf.urls.static import static
from django.conf import settings

# ↑ settings.py를 잘 이용하자.

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/houses/", include("houses.urls")),
    path("api/v1/experiences/", include("experiences.urls")),
    path("api/v1/amenities/", include("amenities.urls")),
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/bookings/", include("bookings.urls")),
    path("api/v1/reviews/", include("reviews.urls")),
    path("api/v1/medias/", include("medias.urls")),
    path("api/v1/wishlists/", include("wishlists.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
