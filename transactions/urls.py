from django.urls import path, include

urlpatterns = [
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('v1/', include('bank_account.urls')),
]
