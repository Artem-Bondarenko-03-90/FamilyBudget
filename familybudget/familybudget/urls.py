"""familybudget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from fb_api.views import APICatViewSet, APIWeekViewSet, api_get_sum_by_category_and_week, \
    api_add_sum_by_category_and_week, api_delete_sum_by_category_and_week, api_statistic_by_category, api_statistic, \
    api_statistic_total, api_total_by_period, APIFamilyViewSet, api_users, \
    api_user_detail, api_sum, api_sum_detail

router = DefaultRouter()
router.register('categories', APICatViewSet)
router.register('weeks', APIWeekViewSet)
router.register('family', APIFamilyViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/sum/', api_sum),
    path('api/v1/sum_detail/<uuid:id>/', api_sum_detail),
    path('api/v1/get_sum_by/category/<uuid:cat_id>/week/<uuid:week_id>/', api_get_sum_by_category_and_week),
    path('api/v1/add_sum_by_category_and_week/', api_add_sum_by_category_and_week),
    path('api/v1/delete_sum_by_category_and_week/', api_delete_sum_by_category_and_week),
    path('api/v1/statistic_sum_by_category/<uuid:cat_id>/', api_statistic_by_category),
    path('api/v1/statistic/', api_statistic),
    path('api/v1/statistic_total/', api_statistic_total),
    path('api/v1/total_by_period/', api_total_by_period),
    path('api/v1/users/', api_users),
    path('api/v1/user_detail/<int:id>/', api_user_detail)
]
