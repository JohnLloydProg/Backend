from rest_framework import serializers
from account.models import Member, Membership, MembershipType


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            'id', 'username', 'first_name', 'last_name', 
            'email', 'birthDate', 'height', 'weight',
            'mobileNumber', 'address', 'gymTrainer', 'sex', 
            'profilePic'
            ]

    def create(self, validated_data):
        member = Member(**validated_data)
        member.save()
        return member


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['startDate', 'member', 'membershipType', 'expirationDate']
        extra_kwargs = {
            'startDate':{'read_only':True},
            'member':{'read_only':True},
            'price':{'read_only':True}
            }


class MembershipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipType
        fields = ['id', 'name', 'price']
