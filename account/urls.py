from django.urls import path
from account import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('email-validation', views.EmailValidationView.as_view(), name='email validation'),
    path('registration/<str:validationCode>', views.AccountRegistrationView.as_view(), name='account registration'),
    path('registration-cont/<str:validationCode>', views.AccountRegistrationContView.as_view(), name='account registration cont'),
    path('member/<str:username>', views.MemberView.as_view(), name='member'),
    path('members', views.MembersView.as_view(), name='members'),
    path('members-admin', views.MembersAdminView.as_view(), name='members admin'),
    path('trainer/<str:username>', views.TrainerView.as_view(), name='trainer'),
    path('token', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh'),
    path('membership', views.MembershipView.as_view(), name='membership'),
    path('membership/change/<int:user>', views.MembershipChangeView.as_view(), name='membership change'),
    path('membership/subscription', views.CheckoutMonthlySubscriptionView.as_view(), name='subscription checkout'),
    path('membership/successful', views.SuccessfulPaymentView.as_view(), name='successful payment'),
    path('membership-types', views.MembershipTypesView.as_view(), name='Membership Types'),
    path('membership/extension/<str:username>', views.SubscriptionExtensionView.as_view(), name='subscription extension'),
]
