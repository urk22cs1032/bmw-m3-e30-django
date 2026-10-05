"""
URL configuration for config project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from showroom import api_views, views

router = routers.DefaultRouter()
router.register(r"vehicles", api_views.VehicleViewSet)


urlpatterns = [

    # --------------------------------------------------------
    # ADMIN
    # --------------------------------------------------------

    path(
        "admin/",
        admin.site.urls
    ),


    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    path(
        "",
        views.home,
        name="home"
    ),


    # --------------------------------------------------------
    # COLLECTION
    # --------------------------------------------------------

    path(
        "collection/",
        views.collection,
        name="collection"
    ),


    # --------------------------------------------------------
    # VEHICLE DETAIL
    # --------------------------------------------------------

    path(
        "vehicle/<int:pk>/",
        views.vehicle_detail,
        name="vehicle_detail"
    ),


    # --------------------------------------------------------
    # ABOUT
    # --------------------------------------------------------

    path(
        "about/",
        views.about,
        name="about"
    ),


    # --------------------------------------------------------
    # MANAGEMENT
    # --------------------------------------------------------

    path(
        "management/",
        views.management,
        name="management"
    ),


    # --------------------------------------------------------
    # ADD VEHICLE
    # --------------------------------------------------------

    path(
        "management/vehicle/add/",
        views.vehicle_add,
        name="vehicle_add"
    ),


    # --------------------------------------------------------
    # EDIT VEHICLE
    # --------------------------------------------------------

    path(
        "management/vehicle/<int:pk>/edit/",
        views.vehicle_edit,
        name="vehicle_edit"
    ),


    # --------------------------------------------------------
    # DELETE VEHICLE
    # --------------------------------------------------------

    path(
        "management/vehicle/<int:pk>/delete/",
        views.vehicle_delete,
        name="vehicle_delete"
    ),

    # --------------------------------------------------------
    # AUTHENTICATION
    # --------------------------------------------------------

    path(
        "login/",
        views.user_login,
        name="login"
    ),
    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),
    path(
        "register/",
        views.user_register,
        name="register"
    ),

    # --------------------------------------------------------
    # API
    # --------------------------------------------------------
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ------------------------------------------------------------
# MEDIA FILES - DEVELOPMENT
# ------------------------------------------------------------

# MEDIA files configured above via + static(...) for development