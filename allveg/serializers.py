from rest_framework import serializers
from .models import *

class TalukSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taluks
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Districts
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'  # This will include all fields in the Users model
        extra_kwargs = {
            'username': {'required': False},  # Optional
            'password': {'required': False},  # Optional
            'role': {'required': False},      # Optional
            'created_by': {'required': False},  # Optional
            'status': {'required': False},    # Optional
        }

    def create(self, validated_data):
        user = Users(**validated_data)  # Create the user object with validated data
        user.save()  # Save to the database
        return user
    
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'


class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = '__all__' 

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__' 

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class LegalComplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalCompliance
        fields = '__all__'

class GeneralManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralManagers
        fields = '__all__' 

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Managers
        fields = '__all__' 

class LeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leader
        fields = '__all__'

class AgriMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgriMember
        fields = '__all__'  

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__' 