"""
URL configuration for ALLVEGPRO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from allveg.views import UserList, UserDetail,DocumentList,BankDetailsList,BankDetailsDetail,LegalComplianceAPIView,DistrictAPIView,TalukDetailView
from allveg.views import GeneralManagerList,GeneralManagerDetail, ManagerList, ManagerDetail, LeaderList, LeaderDetail, AgriMemberList, AgriMemberDetail, FarmerList, FarmerDetail, BuyerList, BuyerDetail, VehicleList, VehicleDetail, ProtectedView, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', UserList.as_view(), name='user-list'),
    path('api/users/<int:user_id>/', UserDetail.as_view(), name='user-detail'),

    path('api/documents/', DocumentList.as_view(), name='document-list-create'),

    path('api/bank-details/', BankDetailsList.as_view(), name='bank-details-list'),
    path('api/bank-details/<int:pk>/', BankDetailsDetail.as_view(), name='bank-details-detail'),

    path('api/general-managers/', GeneralManagerList.as_view(), name='general-managers-list'),
    path('api/general-managers/<int:pk>/', GeneralManagerDetail.as_view(), name='general-managers-detail'),

    path('api/legal-compliance/', LegalComplianceAPIView.as_view(), name='legal-compliance-list-create'),
    path('api/legal-compliance/<int:pk>/', LegalComplianceAPIView.as_view(), name='legal-compliance-detail'),


    path('api/districts/', DistrictAPIView.as_view(), name='district-list-create'),
    path('api/districts/<int:district_id>/', DistrictAPIView.as_view(), name='district-detail-update'),

    path('api/taluks/', TalukDetailView.as_view(), name='taluk-list'),  
    path('api/taluks/<int:pk>/', TalukDetailView.as_view(), name='taluk-detail'), 

    path('api/managers/', ManagerList.as_view(), name='manager-list'),
    path('api/managers/<int:manager_id>/', ManagerDetail.as_view(), name='manager-detail'),

    path('api/leaders/', LeaderList.as_view(), name='leader-list'),
    path('api/leaders/<int:leader_id>/', LeaderDetail.as_view(), name='leader-detail'),

     path('api/agri-members/', AgriMemberList.as_view(), name='agri-member-list'),
    path('api/agri-members/<int:agri_member_id>/', AgriMemberDetail.as_view(), name='agri-member-detail'),

    path('api/farmers/', FarmerList.as_view(), name='farmer-list'),
    path('api/farmers/<int:farmer_id>/', FarmerDetail.as_view(), name='farmer-detail'),
 
    path('api/buyers/', BuyerList.as_view(), name='buyer-list'),
    path('api/buyers/<int:buyer_id>/', BuyerDetail.as_view(), name='buyer-detail'),

    path('api/vehicles/', VehicleList.as_view(), name='vehicle-list'),
    path('api/vehicles/<int:vehicle_id>/', VehicleDetail.as_view(), name='vehicle-detail'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # To obtain token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # To refresh token

    path('api/protected/', ProtectedView.as_view(), name='protected_view'),

    path('logout/', LogoutView.as_view(), name='logout'),


] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)