from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import generics
from account.serializers import MembershipSerializer, MembershipTypeSerializer, MemberSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from account.permissions import IsTrainer
from rest_framework.response import Response
from rest_framework.request import Request
from django.views import View
from datetime import date
from account.models import Member, ValidationSession, Membership, MembershipType, MemberCheckout
from sales.models import Sale
from rest_framework import status
import requests
import smtplib
import ssl
import os

html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Email Verified</title>
    <!-- Google Fonts Link -->
    <link href="https://fonts.googleapis.com/css2?family=Keania+One&display=swap" rel="stylesheet" />
  </head>
  <body style="margin:0; padding:0; background-color:#313030; font-family:'Keania One', sans-serif;">

    <!-- Main Table Wrapper -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#313030; width:100%; height:100%;">
      <tr>
        <td align="center" valign="middle" style="padding:40px 0;">

          <!-- Inner Container -->
          <table cellpadding="0" cellspacing="0" border="0" style="max-width: 400px; background-color:#313030; text-align: center; border-radius: 8px; padding: 20px; width: 100%;">
            <!-- Checkmark Circle -->
            <tr>
              <td align="center" style="padding-bottom: 20px;">
                <div style="width:80px; height:80px; background-color:#76D09C; border-radius:50%; text-align:center; line-height:80px; display:inline-block;">
                  <img src="https://img.icons8.com/ios-filled/50/ffffff/checkmark.png" alt="Checkmark" width="40" height="40" style="vertical-align:middle;" />
                </div>
              </td>
            </tr>

            <!-- Heading -->
            <tr>
              <td style="color:#4CAF50; font-size:2em; font-family:'Keania One', sans-serif; padding-bottom:10px;">
                Email Verified!
              </td>
            </tr>

            <!-- Paragraph -->
            <tr>
              <td style="color:#ffffff; font-size:1.1em; font-family:'Keania One', sans-serif; max-width:320px; padding: 0 10px 20px;">
                Your email address has been successfully verified.
              </td>
            </tr>

            <!-- CTA Button -->
            <tr>
              <td align="center">
                <a href="{link}" style="display:inline-block; padding:10px 20px; background-color:#76D09C; color:#ffffff; text-decoration:none; border-radius:5px; font-size:1em; font-family:'Keania One', sans-serif;">
                  Proceed to registration
                </a>
              </td>
            </tr>
          </table>

        </td>
      </tr>
    </table>
  </body>
</html>
"""

# Email Validation View

class EmailValidationView(generics.GenericAPIView):
    context = ssl.create_default_context()

    def post(self, request:Request) -> Response:
        memberEmail = request.data.get('email')
        try:
            member = Member.objects.get(email=memberEmail)
        except Member.DoesNotExist:
            validationSession = ValidationSession(email=memberEmail)
            validationSession.setExpirationDate()
            validationSession.save()

            validationMSG = MIMEMultipart()
            validationMSG['Subject'] = "Email Validation for Tripple J System"
            link = 'https://triple-j-web.onrender.com/registerStart.html?validationCode=' + str(validationSession.validationCode)
            validationMSG.attach(MIMEText(html.format(link=link), 'html'))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=self.context) as smtp:
                smtp.login("johnlloydunida0@gmail.com", "hvwm jkkz gamd nvnn")
                smtp.sendmail("johnlloydunida0@gmail.com", [memberEmail], validationMSG.as_string())

            return Response({'details':"Email sent successfully"}, status=status.HTTP_200_OK)
        return Response({'details':"Email is already registered in the system"}, status=status.HTTP_409_CONFLICT)


class AccountRegistrationView(generics.GenericAPIView):
    permission_classes = []

    def post(self, request:Request, validationCode:str) -> Response:
        try:
            validationSession = ValidationSession.objects.get(validationCode=validationCode)
            if (date.today() > validationSession.expirationDate):
                validationSession.delete()
                return Response('Validation Session Expired!', status=status.HTTP_401_UNAUTHORIZED)
        except ValidationSession.DoesNotExist:
            return Response('Validation Code does not exist!', status=status.HTTP_401_UNAUTHORIZED)

        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        membershipType = request.data.get('membership')

        if (not username or not email or not password or not membershipType):
            return Response('Missing required fields', status=status.HTTP_400_BAD_REQUEST)
        
        try:
            membershipTypeObject = MembershipType(pk=membershipType)
        except MembershipType.DoesNotExist:
            return Response('Membership Type does not exist!', status=status.HTTP_404_NOT_FOUND)

        try:
            member = Member.objects.get(username=username)
            return Response('Username already exists', status=status.HTTP_409_CONFLICT)
        except Member.DoesNotExist:
            member = Member(username=username, email=email)
            member.set_password(password)
            member.save()

            membership = Membership(member=member, membershipType=membershipTypeObject)
            membership.save()

            return Response('Account successfully registered!', status=status.HTTP_201_CREATED)


class AccountRegistrationContView(generics.GenericAPIView):
    permission_classes = []

    def post(self, request:Request, validationCode:str) -> Response:
        try:
            validationSession = ValidationSession.objects.get(validationCode=validationCode)
            if (date.today() > validationSession.expirationDate):
                validationSession.delete()
                return Response('Validation Session Expired!', status=status.HTTP_401_UNAUTHORIZED)
        except ValidationSession.DoesNotExist:
            return Response('Validation Code does not exist!', status=status.HTTP_401_UNAUTHORIZED)
        
        member = Member.objects.get(email=validationSession.email)
        for key, value in request.data.items():
            setattr(member, key, value)
        member.save()

        return Response('Account successfully registered!', status=status.HTTP_202_ACCEPTED)

class MemberView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer
    queryset = Member.objects.all()
    lookup_field = 'username'


class TrainerView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer
    queryset = Member.objects.filter(is_trainer=True)
    lookup_field = 'username'


class MembersView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsTrainer]

    def get(self, request:Request) -> Response:
        try:
            trainer = Member.objects.get(pk=self.request.user)
        except Member.DoesNotExist:
            return Response('Trainer does not exist', status=status.HTTP_404_NOT_FOUND)
        return Response(MemberSerializer(Member.objects.filter(gymTrainer=trainer), many=True).data, status=status.HTTP_200_OK)


class MembersAdminView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = MemberSerializer
    queryset = Member.objects.all()
    
    def get(self, request:Request) -> Response:
        data = []
        for member in Member.objects.all():
            membership = Membership.objects.get(member=member)
            json = {
                    'username': member.username, 'first_name': member.first_name, 'last_name': member.last_name, 'email': member.email,
                    'birthDate': member.birthDate, 'height': member.height, 'weight': member.weight, 'mobileNumber': member.mobileNumber,
                    'address': member.address, 'sex': member.sex,
                    'membership': {'startDate': membership.startDate, 'membershipType':membership.membershipType.name, 'expirationDate': membership.expirationDate}, 'subscription': membership.membershipType.subscription
                }
            if (member.gymTrainer):
                gymTrainer = Member.objects.get(pk=member.gymTrainer)
                json['gymTrainer'] = gymTrainer.username
            if (member.profilePic):
                json['profilePic'] = member.profilePic
            data.append(json)

        return Response(data, status=status.HTTP_200_OK)


class MembershipView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request:Request) -> Response:
        user_id = request.query_params.get('id')
        try:
            if (user_id):
                if (self.request.user.is_superuser):
                    user_id = int(user_id)
                else:
                    return Response('Do not have the authority to use query parameters!', status=status.HTTP_403_FORBIDDEN)
            else:
                user_id = self.request.user
            member = Member.objects.get(pk=user_id)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
        
        
        membership = Membership.objects.get(member=member)
        data = {'id':membership.pk, 'member':member.pk, 'membershipType':membership.membershipType.name, 'startDate':membership.startDate, 'expirationDate':membership.expirationDate, 'subscription':membership.membershipType.subscription}
        return Response(data, status=status.HTTP_200_OK)


class MembershipChangeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request:Request, user:int) -> Response:
        try:
            member = Member.objects.get(pk=user)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
        
        if (request.data.get('changeTo') not in ['Daily', 'Monthly']):
            return Response('Invalid membership type (Daily or Monthly only)', status=status.HTTP_400_BAD_REQUEST)
        return Response('Membership successfully changed', status=status.HTTP_200_OK)


class MembershipTypesView(generics.GenericAPIView):
    permission_classes = []

    def get(self, request:Request) -> Response:
        return Response(MembershipTypeSerializer(MembershipType.objects.all(), many=True).data, status=status.HTTP_200_OK)


class CheckoutMonthlySubscriptionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request:Request) -> Response:
        try:
            member = Member.objects.get(pk=self.request.user)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)

        membership = Membership.objects.get(member=member)
        if (not membership.membershipType.subscription):
            return Response('Membership does not have a subscription', status=status.HTTP_400_BAD_REQUEST)
        
        url = "https://api.paymongo.com/v1/checkout_sessions"

        payload = { "data": { "attributes": {
                    "send_email_receipt": True,
                    "show_description": True,
                    "show_line_items": True,
                    "description": "Monthly subscription to Triple-J Gym.",
                    "line_items": [
                        {
                            "currency": "PHP",
                            "amount": int(membership.membershipType.price * 100),
                            "name": "Monthly Subscription",
                            "quantity": 1
                        }
                    ],
                    "payment_method_types": ["qrph", "gcash"],
                } } }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "authorization": "Basic c2tfdGVzdF9pSkE1cmJlMVJ0Q3BjWmN3TWd6aVVkd3c6",
        }

        response = requests.post(url, json=payload, headers=headers)
        if (response.ok):
            data = response.json().get('data')
            memberCheckout = MemberCheckout(checkoutId=data.get('id'), member=member)
            memberCheckout.save()
            return Response({'details':{'link':data.get('attributes').get('checkout_url')}}, status=status.HTTP_200_OK)
        return Response({'details':'paymongo api request failed'}, status=status.HTTP_417_EXPECTATION_FAILED)


class SuccessfulPaymentView(generics.GenericAPIView):
    permission_classes = []

    def post(self, request:Request) -> Response:
        data = request.data.get('data')
        if (not data):
            return Response("Invalid data received", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            memberCheckout = MemberCheckout.objects.get(checkoutId=data.get('attributes').get('data').get('id'))
        except MemberCheckout.DoesNotExist:
            return Response("Member checkout session does not exist", status=status.HTTP_404_NOT_FOUND)

        membership = Membership.objects.get(member=memberCheckout.member)
        membership.extendExpirationDate()
        membership.save()

        sales = Sale(amount=membership.membershipType.price, description=f"Membership {membership.membershipType.name}", receipt_no=memberCheckout.checkoutId)
        sales.save()

        memberCheckout.delete()
        return Response("You have successfully paid the membership!", status=status.HTTP_200_OK)


class SubscriptionExtensionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request:Request, username:str) -> Response:
        try:
            member = Member.objects.get(username=username)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
        try:
            membership = Membership.objects.get(member=member)
        except Membership.DoesNotExist:
            return Response('Member does not have a membership', status=status.HTTP_404_NOT_FOUND)

        if (membership.membershipType.subscription):
            membership.extendExpirationDate()
            membership.save()
            sale = Sale(amount=membership.membershipType.price, description=f"Membership {membership.membershipType.name}")
            sale.save()
            return Response('Membership successfully extended', status=status.HTTP_200_OK)
        else:
            return Response('Membership is not a subscription type', status=status.HTTP_400_BAD_REQUEST)
