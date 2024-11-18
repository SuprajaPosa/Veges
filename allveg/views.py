import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Users,Documents,BankDetails,GeneralManagers,LegalCompliance,Districts,Taluks, Managers, Leader, AgriMember, Farmer, Buyer, Vehicle
from .serializers import UserSerializer,DocumentSerializer,BankDetailSerializer,LegalComplianceSerializer,DistrictSerializer,TalukSerializer, ManagerSerializer, LeaderSerializer, AgriMemberSerializer, FarmerSerializer, BuyerSerializer, VehicleSerializer
from .serializers import GeneralManagerSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView


class DistrictAPIView(APIView):
    def get(self, request, district_id=None):
        if district_id:
            try:
                district = Districts.objects.get(district_id=district_id)
                serializer = DistrictSerializer(district)
                return Response(serializer.data)
            except Districts.DoesNotExist:
                return Response({"error": "District not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            districts = Districts.objects.all()
            serializer = DistrictSerializer(districts, many=True)
            return Response(serializer.data)

class TalukDetailView(APIView):

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            # Get a single taluk by primary key (id)
            taluk = get_object_or_404(Taluks, pk=pk)
            serializer = TalukSerializer(taluk)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Get all taluks
            taluks = Taluks.objects.all()
            serializer = TalukSerializer(taluks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class UserList(APIView):
    """
    List all users or create a new user.
    """
    def get(self, request, format=None):
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, user_id):
        try:
            return Users.objects.get(user_id=user_id)
        except Users.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, user_id):
        user = get_object_or_404(Users, pk=user_id)
        # Partially update the user with the data received
        serializer = UserSerializer(user, data=request.data, partial=True)  # Allow partial updates
        print("OK")
        if serializer.is_valid():
            user = serializer.save()  # Save the updated user
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        user = self.get_object(user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DocumentList(APIView):
    def get(self, request):
        documents = Documents.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request):
        print('Data is ==> ', request.data)

        # Parse the incoming data for multiple documents
        documents_data = []

        # Extracting document details from the QueryDict
        index = 0
        while f'documents[{index}][document_type]' in request.data:
            document = {
                'document_type': request.data.get(f'documents[{index}][document_type]'),
                'entity_type': request.data.get(f'documents[{index}][entity_type]'),
                'document_path': request.FILES.get(f'documents[{index}][document_path]')
            }
            documents_data.append(document)
            index += 1

        if not documents_data:
            return Response({"error": "No documents provided."}, status=status.HTTP_400_BAD_REQUEST)

        saved_documents = []

        # Loop through each document and save it
        for document_data in documents_data:
            serializer = DocumentSerializer(data=document_data)
            if serializer.is_valid():
                document_instance = serializer.save()

                # Append necessary fields to the response
                saved_documents.append({
                    'document_id': document_instance.document_id,
                    'entity_type': document_instance.entity_type,
                    'document_type': document_instance.document_type,
                    'document_path': document_instance.document_path.url if document_instance.document_path else None,
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Return the saved documents as a response
        return Response(saved_documents, status=status.HTTP_201_CREATED)


class BankDetailsList(APIView):
    def get(self, request):
        bank_details = BankDetails.objects.all()
        serializer = BankDetailSerializer(bank_details, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BankDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BankDetailsDetail(APIView):
    def get(self, request, pk):
        bank_detail = get_object_or_404(BankDetails, pk=pk)
        serializer = BankDetailSerializer(bank_detail)
        return Response(serializer.data)

    def patch(self, request, pk):
        bank_detail = get_object_or_404(BankDetails, pk=pk)
        serializer = BankDetailSerializer(bank_detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bank_detail = get_object_or_404(BankDetails, pk=pk)
        bank_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuyerList(APIView):
    """
    List all buyers or create a new buyer.
    """
    def get(self, request):
        buyers = Buyer.objects.all()
        serializer = BuyerSerializer(buyers, many=True)
        return Response(serializer.data)

    def post(self, request):
        business_doc_id = None
        gst_doc_id = None
        pancard_doc_id = None

        # Dealing with Bank Details
        bank_details_str = request.data.get('bank_details')
        if not bank_details_str:
            return Response({'error': 'Bank details not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bank_details_data = json.loads(bank_details_str)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid bank details format.'}, status=status.HTTP_400_BAD_REQUEST)

        bank_details_serializer = BankDetailSerializer(data=bank_details_data)
        if bank_details_serializer.is_valid():
            bank_details_object = bank_details_serializer.save()  # Save bank details to the database
        else:
            return Response(bank_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Parse the incoming data for multiple documents
        documents_data = []
        index = 0
        while f'documents[{index}][document_type]' in request.data:
            document = {
                'document_type': request.data.get(f'documents[{index}][document_type]'),
                'document_path': request.FILES.get(f'documents[{index}][document_path]')
            }
            documents_data.append(document)
            index += 1

        if not documents_data:
            return Response({"error": "No documents provided."}, status=status.HTTP_400_BAD_REQUEST)

        saved_documents = []

        # Loop through each document and save it
        for document_data in documents_data:
            serializer = DocumentSerializer(data=document_data)
            if serializer.is_valid():
                document_instance = serializer.save()

                # Append necessary fields to the response
                saved_documents.append({
                    'document_id': document_instance.document_id,
                    'entity_type': document_instance.entity_type,
                    'document_type': document_instance.document_type,
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Dealing with Document Type and IDs for Role Reference
        for document in saved_documents:
            if document['document_type'] == 'Business':
                business_doc_id = document['document_id']
            elif document['document_type'] == 'GST':
                gst_doc_id = document['document_id']
            elif document['document_type'] == 'PanCard':
                pancard_doc_id = document['document_id']

        # Collecting buyer data
        buyer_data = {
            'full_name': request.data.get('full_name'),
            'phone_number': request.data.get('phone_number'),
            'email': request.data.get('email'),
            'address': request.data.get('address'),
            'business_name': request.data.get('business_name'),  # New field
            'pan_number': request.data.get('pan_number'),  # New field
            'bank_details_id': bank_details_object.bank_details_id if bank_details_object else None,
            'business_doc_id': business_doc_id,  # Assign business_id
            'gst_doc_id': gst_doc_id,  # Assign gst_id
            'pancard_doc_id': pancard_doc_id  # Assign pancard_id
        }

        buyer_serializer = BuyerSerializer(data=buyer_data)

        if buyer_serializer.is_valid():
            buyer_serializer.save()
            return Response(buyer_serializer.data, status=status.HTTP_201_CREATED)
        return Response(buyer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BuyerDetail(APIView):
    def get(self, request, pk):
        buyer = get_object_or_404(Buyer, pk=pk)
        serializer = BuyerSerializer(buyer)
        return Response(serializer.data)

    def patch(self, request, pk):
        buyer = get_object_or_404(Buyer, pk=pk)
        serializer = BuyerSerializer(buyer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        buyer = get_object_or_404(Buyer, pk=pk)
        buyer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VehicleList(APIView):
    """
    List all vehicles or create a new buyer.
    """
    def get(self, request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        vehicle_rc_book_doc_id = None
        vehicle_insurance_doc_id = None
        driving_license_doc_id = None
        identity_doc_id = None
        photo_id = None
        pancard_doc_id = None
        bank_doc_id = None

        # Dealing with Bank Details
        bank_details_str = request.data.get('bank_details')
        if not bank_details_str:
            return Response({'error': 'Bank details not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bank_details_data = json.loads(bank_details_str)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid bank details format.'}, status=status.HTTP_400_BAD_REQUEST)

        bank_details_serializer = BankDetailSerializer(data=bank_details_data)
        if bank_details_serializer.is_valid():
            bank_details_object = bank_details_serializer.save()  # Save bank details to the database
        else:
            return Response(bank_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Parse the incoming data for multiple documents
        documents_data = []
        index = 0
        while f'documents[{index}][document_type]' in request.data:
            document = {
                'document_type': request.data.get(f'documents[{index}][document_type]'),
                'document_path': request.FILES.get(f'documents[{index}][document_path]')
            }
            documents_data.append(document)
            index += 1

        if not documents_data:
            return Response({"error": "No documents provided."}, status=status.HTTP_400_BAD_REQUEST)

        saved_documents = []

        # Loop through each document and save it
        for document_data in documents_data:
            serializer = DocumentSerializer(data=document_data)
            if serializer.is_valid():
                document_instance = serializer.save()

                # Append necessary fields to the response
                saved_documents.append({
                    'document_id': document_instance.document_id,
                    'entity_type': document_instance.entity_type,
                    'document_type': document_instance.document_type,
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        print("355 ==> sending the documents daata ", saved_documents)
        # Dealing with Document Type and IDs for Role Reference
        for document in saved_documents:
            if document['document_type'] == 'Vehicle_RC_Book':
                vehicle_rc_book_doc_id = document['document_id']
            elif document['document_type'] == 'Vehicle_Insurance':
                vehicle_insurance_doc_id = document['document_id']
            elif document['document_type'] == 'Driving_License':
                driving_license_doc_id = document['document_id']
            elif document['document_type'] == 'Identity':
                identity_doc_id = document['document_id']
            elif document['document_type'] == 'Photo':
                photo_id = document['document_id']
            elif document['document_type'] == 'PanCard':
                pancard_doc_id = document['document_id']
            elif document['document_type'] == 'Bank_Details':
                bank_doc_id = document['document_id']
        print("===> Data is ", request.data)
        # Collecting buyer data
        vehicle_data = {
            'driver_owner_full_name': request.data.get('driver_owner_full_name'),
            'driver_full_name': request.data.get('driver_full_name'),
            'vehicle_name': request.data.get('vehicle_name'),
            'model_number': request.data.get('model_number'),
            'vehicle_registration_number': request.data.get('vehicle_registration_number'),  # New field
            'vehicle_insurance_number': request.data.get('vehicle_insurance_number'),  # New field
            'vehicle_insurance_expiry_date': request.data.get('vehicle_insurance_expiry_date'),
            'driving_license_number': request.data.get('driving_license_number'),
            'driving_license_expiry_date': request.data.get('driving_license_expiry_date'),
            
            'vehicle_rc_book_doc_id': vehicle_rc_book_doc_id,
            'vehicle_insurance_doc_id': vehicle_insurance_doc_id,
            'driving_license_doc_id': driving_license_doc_id,
            'identity_doc_id': identity_doc_id,  # Assign business_id
            'photo_id': photo_id,  # Assign gst_id
            'pancard_doc_id': pancard_doc_id,  # Assign pancard_id
            'bank_doc_id' : bank_doc_id
        }

        vehicle_serializer = VehicleSerializer(data=vehicle_data)

        if vehicle_serializer.is_valid():
            vehicle_serializer.save()
            return Response(vehicle_serializer.data, status=status.HTTP_201_CREATED)
        return Response(vehicle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VehicleDetail(APIView):
    def get(self, request, pk):
        vehicles = get_object_or_404(Vehicle, pk=pk)
        serializer = VehicleSerializer(vehicles)
        return Response(serializer.data)

    def patch(self, request, pk):
        vehicles = get_object_or_404(Vehicle, pk=pk)
        serializer = VehicleSerializer(vehicles, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vehicles = get_object_or_404(Vehicle, pk=pk)
        vehicles.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

   

class GeneralManagerList(APIView):
    def get(self, request):
        general_managers = GeneralManagers.objects.all()
        serializer = GeneralManagerSerializer(general_managers, many=True)
        return Response(serializer.data)

    def post(self, request):

        identity_doc_id = None
        address_doc_id = None
        bank_doc_id = None
        education_doc_id = None
        photo_id = None
        land_doc_id = None

        # Dealing with Bank Details
        bank_details_str = request.data.get('bank_details')
        if not bank_details_str:
            return Response({'error': 'Bank details not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bank_details_data = json.loads(bank_details_str)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid bank details format.'}, status=status.HTTP_400_BAD_REQUEST)

        bank_details_serializer = BankDetailSerializer(data=bank_details_data)
        if bank_details_serializer.is_valid():
            bank_details_object = bank_details_serializer.save()  # Save bank details to the database
        else:
            return Response(bank_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Parse the incoming data for multiple documents
        documents_data = []
        index = 0
        while f'documents[{index}][document_type]' in request.data:
            document = {
                'document_type': request.data.get(f'documents[{index}][document_type]'),
                'entity_type': request.data.get(f'documents[{index}][entity_type]'),
                'document_path': request.FILES.get(f'documents[{index}][document_path]')
            }
            documents_data.append(document)
            index += 1
        if not documents_data:
            return Response({"error": "No documents provided."}, status=status.HTTP_400_BAD_REQUEST)

        saved_documents = []

        # Loop through each document and save it
        for document_data in documents_data:
            serializer = DocumentSerializer(data=document_data)
            if serializer.is_valid():
                document_instance = serializer.save()

                # Append necessary fields to the response
                saved_documents.append({
                    'document_id': document_instance.document_id,
                    'entity_type': document_instance.entity_type,
                    'document_type': document_instance.document_type,
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # Dealing with the Legal Compliance Data
        legal_compliance_str = request.data.get('legal_compliance')
        legal_compliance_data = {}
        legal_compliance_instance = None
        if legal_compliance_str:
            try:
                legal_compliance_data = json.loads(legal_compliance_str)
            except json.JSONDecodeError:
                return Response({'error': 'Invalid legal compliance format.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if any(value for value in legal_compliance_data.values() if value not in [None, '','null']):  # Exclude None, empty, and string 'null'
                legal_compliance_serializer = LegalComplianceSerializer(data=legal_compliance_data)
                if legal_compliance_serializer.is_valid():
                    legal_compliance_instance = legal_compliance_serializer.save()  # Create the LegalCompliance object
                else:
                    return Response(legal_compliance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        #  Dealing with Document Type and it's IDs for Role Reference
        for document in saved_documents:
            if document['document_type'] == 'Photo':
                photo_id = document['document_id'] 
            elif document['document_type'] == 'Bank':
                bank_doc_id = document['document_id']
            elif document['document_type'] == 'Identity':
                identity_doc_id = document['document_id'] 
            elif document['document_type'] == 'Address':
                address_doc_id = document['document_id']
            elif document['document_type'] == 'Land':
                land_doc_id = document['document_id'] 
            elif document['document_type'] == 'Education':
                education_doc_id = document['document_id']
       
        print("saved documents are ", saved_documents)
        general_manager_data = {
            'full_name' : request.data.get('full_name'),
            'fathers_or_husbands_name' : request.data.get('fathers_or_husbands_name'),
            'email' : request.data.get('email'),
            'date_of_birth' : request.data.get('date_of_birth'),
            'gender':request.data.get('gender'),
            'aadhaar_number' : request.data.get('aadhaar_number'),
            'phone_number' : request.data.get('phone_number'),
            'residential_address' : request.data.get('residential_address'),
            'designation' : request.data.get('designation'),
            'assigned_city' : request.data.get('assigned_city'),
            'joining_date' : request.data.get('joining_date'),
            'employee_id' : request.data.get('employee_id'),

            'identity_doc_id' : identity_doc_id if identity_doc_id else None,
            'address_doc_id' : address_doc_id if address_doc_id else None,
            'bank_doc_id' : bank_doc_id if bank_doc_id else None,
            'photo_id' : photo_id if photo_id else None,
            'education_doc_id' : education_doc_id if education_doc_id else None,
            'land_doc_id' : land_doc_id if land_doc_id else None,

            'legal_compliance_id' : legal_compliance_instance.compliance_id if legal_compliance_instance else None,
            'bank_details_id' : bank_details_object.bank_details_id if bank_details_object else None

        }

        general_manager_serializer = GeneralManagerSerializer(data=general_manager_data)
        print("295 raa mama ", general_manager_serializer)
        if general_manager_serializer.is_valid():
            print("=========== Almost done ===============")
            general_manager_serializer.save()
            print("Done baby ")
            return Response(general_manager_serializer.data, status=status.HTTP_201_CREATED)
        return Response(general_manager_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class GeneralManagerDetail(APIView):
    def get(self, request, pk):
        general_manager = get_object_or_404(GeneralManagers, pk=pk)
        serializer = GeneralManagerSerializer(general_manager)
        return Response(serializer.data)

    def patch(self, request, pk):
        general_manager = get_object_or_404(GeneralManagers, pk=pk)
        serializer = GeneralManagerSerializer(general_manager, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        general_manager = get_object_or_404(GeneralManagers, pk=pk)
        general_manager.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class LegalComplianceAPIView(APIView):
    
    def get(self, request, pk=None):
        """Handle GET requests. If `pk` is provided, fetch a single object. Otherwise, fetch all."""
        if pk:
            legal_compliance = get_object_or_404(LegalCompliance, pk=pk)
            serializer = LegalComplianceSerializer(legal_compliance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            legal_compliance = LegalCompliance.objects.all()
            serializer = LegalComplianceSerializer(legal_compliance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Handle POST request to create a new LegalCompliance entry."""
        serializer = LegalComplianceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Handle PUT request to update an existing LegalCompliance entry."""
        legal_compliance = get_object_or_404(LegalCompliance, pk=pk)
        serializer = LegalComplianceSerializer(legal_compliance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        """Handle PATCH request for partial updates."""
        legal_compliance = get_object_or_404(LegalCompliance, pk=pk)
        serializer = LegalComplianceSerializer(legal_compliance, data=request.data, partial=True)  # Set partial=True
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Handle DELETE request to delete an existing LegalCompliance entry."""
        legal_compliance = get_object_or_404(LegalCompliance, pk=pk)
        legal_compliance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ManagerList(APIView):
    """
    List all managers or create a new manager.
    """
    def get(self, request):
        managers = Managers.objects.all()
        serializer = ManagerSerializer(managers, many=True)
        return Response(serializer.data)

    def post(self, request):
        identity_doc_id = None
        address_doc_id = None
        bank_doc_id = None
        education_doc_id = None
        photo_id = None
        land_doc_id = None

        # Dealing with Bank Details
        bank_details_str = request.data.get('bank_details')
        if not bank_details_str:
            return Response({'error': 'Bank details not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bank_details_data = json.loads(bank_details_str)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid bank details format.'}, status=status.HTTP_400_BAD_REQUEST)

        bank_details_serializer = BankDetailSerializer(data=bank_details_data)
        if bank_details_serializer.is_valid():
            bank_details_object = bank_details_serializer.save()  # Save bank details to the database
        else:
            return Response(bank_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Parse the incoming data for multiple documents
        documents_data = []
        index = 0
        while f'documents[{index}][document_type]' in request.data:
            document = {
                'document_type': request.data.get(f'documents[{index}][document_type]'),
                'entity_type': request.data.get(f'documents[{index}][entity_type]'),
                'document_path': request.FILES.get(f'documents[{index}][document_path]')
            }
            documents_data.append(document)
            index += 1
        if not documents_data:
            return Response({"error": "No documents provided."}, status=status.HTTP_400_BAD_REQUEST)

        saved_documents = []

        # Loop through each document and save it
        for document_data in documents_data:
            serializer = DocumentSerializer(data=document_data)
            if serializer.is_valid():
                document_instance = serializer.save()

                # Append necessary fields to the response
                saved_documents.append({
                    'document_id': document_instance.document_id,
                    'entity_type': document_instance.entity_type,
                    'document_type': document_instance.document_type,
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # Dealing with the Legal Compliance Data
        legal_compliance_str = request.data.get('legal_compliance')
        legal_compliance_data = {}
        legal_compliance_instance = None
        if legal_compliance_str:
            try:
                legal_compliance_data = json.loads(legal_compliance_str)
            except json.JSONDecodeError:
                return Response({'error': 'Invalid legal compliance format.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if any(value for value in legal_compliance_data.values() if value not in [None, '','null']):  # Exclude None, empty, and string 'null'
                legal_compliance_serializer = LegalComplianceSerializer(data=legal_compliance_data)
                if legal_compliance_serializer.is_valid():
                    legal_compliance_instance = legal_compliance_serializer.save()  # Create the LegalCompliance object
                else:
                    return Response(legal_compliance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        #  Dealing with Document Type and it's IDs for Role Reference
        for document in saved_documents:
            if document['document_type'] == 'Photo':
                photo_id = document['document_id'] 
            elif document['document_type'] == 'Bank':
                bank_doc_id = document['document_id']
            elif document['document_type'] == 'Identity':
                identity_doc_id = document['document_id'] 
            elif document['document_type'] == 'Address':
                address_doc_id = document['document_id']
            elif document['document_type'] == 'Land':
                land_doc_id = document['document_id'] 
            elif document['document_type'] == 'Education':
                education_doc_id = document['document_id']
       
        print("saved documents are ", saved_documents)
        manager_data = {
            'full_name' : request.data.get('full_name'),
            'fathers_or_husbands_name' : request.data.get('fathers_or_husbands_name'),
            'email' : request.data.get('email'),
            'date_of_birth' : request.data.get('date_of_birth'),
            'gender':request.data.get('gender'),
            'aadhaar_number' : request.data.get('aadhaar_number'),
            'phone_number' : request.data.get('phone_number'),
            'residential_address' : request.data.get('residential_address'),
            'designation' : request.data.get('designation'),
            'assigned_area' : request.data.get('assigned_area'),
            'supervisor_general_manager_id' : request.data.get('supervisor_general_manager_id'),
            'joining_date' : request.data.get('joining_date'),
            'employee_id' : request.data.get('employee_id'),

            'identity_doc_id' : identity_doc_id if identity_doc_id else None,
            'address_doc_id' : address_doc_id if address_doc_id else None,
            'bank_doc_id' : bank_doc_id if bank_doc_id else None,
            'photo_id' : photo_id if photo_id else None,
            'education_doc_id' : education_doc_id if education_doc_id else None,
            'land_doc_id' : land_doc_id if land_doc_id else None,

            'legal_compliance_id' : legal_compliance_instance.compliance_id if legal_compliance_instance else None,
            'bank_details_id' : bank_details_object.bank_details_id if bank_details_object else None

        }

        manager_serializer = ManagerSerializer(data=manager_data)
        print("295 raa mama ", manager_serializer)
        if manager_serializer.is_valid():
            print("=========== Almost done ===============")
            manager_serializer.save()
            print("Done baby ")
            return Response(manager_serializer.data, status=status.HTTP_201_CREATED)
        return Response(manager_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ManagerDetail(APIView):
    """
    Retrieve, update or delete a manager instance.
    """
    def get_object(self, manager_id):
        try:
            return Managers.objects.get(manager_id=manager_id)
        except Managers.DoesNotExist:
            return None

    def get(self, request, manager_id):
        manager = self.get_object(manager_id)
        if manager is not None:
            serializer = ManagerSerializer(manager)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, manager_id):
        manager = self.get_object(manager_id)
        if manager is not None:
            serializer = ManagerSerializer(manager, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, manager_id):
        manager = self.get_object(manager_id)
        if manager is not None:
            manager.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

class LeaderList(APIView):
    """
    List all leaders or create a new leader.
    """
    def get(self, request):
        leaders = Leader.objects.all()
        serializer = LeaderSerializer(leaders, many=True)
        return Response(serializer.data)

    def post(self, request):
        identity_doc_id = None
        address_doc_id = None
        bank_doc_id = None
        education_doc_id = None
        photo_id = None
        land_doc_id = None

        # Dealing with Bank Details
        bank_details_str = request.data.get('bank_details')
        if not bank_details_str:
            return Response({'error': 'Bank details not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bank_details_data = json.loads(bank_details_str)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid bank details format.'}, status=status.HTTP_400_BAD_REQUEST)

        bank_details_serializer = BankDetailSerializer(data=bank_details_data)
        if bank_details_serializer.is_valid():
            bank_details_object = bank_details_serializer.save()  # Save bank details to the database
        else:
            return Response(bank_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Parse the incoming data for multiple documents
        documents_data = []
        index = 0
        while f'documents[{index}][document_type]' in request.data:
            document = {
                'document_type': request.data.get(f'documents[{index}][document_type]'),
                'entity_type': request.data.get(f'documents[{index}][entity_type]'),
                'document_path': request.FILES.get(f'documents[{index}][document_path]')
            }
            documents_data.append(document)
            index += 1
        if not documents_data:
            return Response({"error": "No documents provided."}, status=status.HTTP_400_BAD_REQUEST)

        saved_documents = []

        # Loop through each document and save it
        for document_data in documents_data:
            serializer = DocumentSerializer(data=document_data)
            if serializer.is_valid():
                document_instance = serializer.save()

                # Append necessary fields to the response
                saved_documents.append({
                    'document_id': document_instance.document_id,
                    'entity_type': document_instance.entity_type,
                    'document_type': document_instance.document_type,
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # Dealing with the Legal Compliance Data
        legal_compliance_str = request.data.get('legal_compliance')
        legal_compliance_data = {}
        legal_compliance_instance = None
        if legal_compliance_str:
            try:
                legal_compliance_data = json.loads(legal_compliance_str)
            except json.JSONDecodeError:
                return Response({'error': 'Invalid legal compliance format.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if any(value for value in legal_compliance_data.values() if value not in [None, '','null']):  # Exclude None, empty, and string 'null'
                legal_compliance_serializer = LegalComplianceSerializer(data=legal_compliance_data)
                if legal_compliance_serializer.is_valid():
                    legal_compliance_instance = legal_compliance_serializer.save()  # Create the LegalCompliance object
                else:
                    return Response(legal_compliance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        #  Dealing with Document Type and it's IDs for Role Reference
        for document in saved_documents:
            if document['document_type'] == 'Photo':
                photo_id = document['document_id'] 
            elif document['document_type'] == 'Bank':
                bank_doc_id = document['document_id']
            elif document['document_type'] == 'Identity':
                identity_doc_id = document['document_id'] 
            elif document['document_type'] == 'Address':
                address_doc_id = document['document_id']
            elif document['document_type'] == 'Land':
                land_doc_id = document['document_id'] 
            elif document['document_type'] == 'Education':
                education_doc_id = document['document_id']
       
        print("saved documents are ", saved_documents)
        leader_data = {
            'full_name' : request.data.get('full_name'),
            'fathers_or_husbands_name' : request.data.get('fathers_or_husbands_name'),
            'email' : request.data.get('email'),
            'date_of_birth' : request.data.get('date_of_birth'),
            'gender':request.data.get('gender'),
            'aadhaar_number' : request.data.get('aadhaar_number'),
            'phone_number' : request.data.get('phone_number'),
            'residential_address' : request.data.get('residential_address'),
            'designation' : request.data.get('designation'),
            'assigned_area' : request.data.get('assigned_area'),
            'supervisor_general_manager_id' : request.data.get('supervisor_general_manager_id'),
            'joining_date' : request.data.get('joining_date'),
            'employee_id' : request.data.get('employee_id'),

            'identity_doc_id' : identity_doc_id if identity_doc_id else None,
            'address_doc_id' : address_doc_id if address_doc_id else None,
            'bank_doc_id' : bank_doc_id if bank_doc_id else None,
            'photo_id' : photo_id if photo_id else None,
            'education_doc_id' : education_doc_id if education_doc_id else None,
            'land_doc_id' : land_doc_id if land_doc_id else None,

            'legal_compliance_id' : legal_compliance_instance.compliance_id if legal_compliance_instance else None,
            'bank_details_id' : bank_details_object.bank_details_id if bank_details_object else None

        }

        leader_serializer = LeaderSerializer(data=leader_data)
        print("295 raa mama ", leader_serializer)
        if leader_serializer.is_valid():
            print("=========== Almost done ===============")
            leader_serializer.save()
            print("Done baby ")
            return Response(leader_serializer.data, status=status.HTTP_201_CREATED)
        return Response(leader_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeaderDetail(APIView):
    """
    Retrieve, update or delete a leader instance.
    """
    def get_object(self, leader_id):
        try:
            return Leader.objects.get(leader_id=leader_id)
        except Leader.DoesNotExist:
            return None

    def get(self, request, leader_id):
        leader = self.get_object(leader_id)
        if leader is not None:
            serializer = LeaderSerializer(leader)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, leader_id):
        leader = self.get_object(leader_id)
        if leader is not None:
            serializer = LeaderSerializer(leader, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, leader_id):
        leader = self.get_object(leader_id)
        if leader is not None:
            leader.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    

class AgriMemberList(APIView):
    """
    List all agri members or create a new agri member.
    """
    def get(self, request):
        agri_members = AgriMember.objects.all()
        serializer = AgriMemberSerializer(agri_members, many=True)
        return Response(serializer.data)

    def post(self, request):
        identity_doc_id = None
        address_doc_id = None
        bank_doc_id = None
        education_doc_id = None
        photo_id = None
        land_doc_id = None

        # Dealing with Bank Details
        bank_details_str = request.data.get('bank_details')
        if not bank_details_str:
            return Response({'error': 'Bank details not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bank_details_data = json.loads(bank_details_str)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid bank details format.'}, status=status.HTTP_400_BAD_REQUEST)

        bank_details_serializer = BankDetailSerializer(data=bank_details_data)
        if bank_details_serializer.is_valid():
            bank_details_object = bank_details_serializer.save()  # Save bank details to the database
        else:
            return Response(bank_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Parse the incoming data for multiple documents
        documents_data = []
        index = 0
        while f'documents[{index}][document_type]' in request.data:
            document = {
                'document_type': request.data.get(f'documents[{index}][document_type]'),
                'entity_type': request.data.get(f'documents[{index}][entity_type]'),
                'document_path': request.FILES.get(f'documents[{index}][document_path]')
            }
            documents_data.append(document)
            index += 1
        if not documents_data:
            return Response({"error": "No documents provided."}, status=status.HTTP_400_BAD_REQUEST)

        saved_documents = []

        # Loop through each document and save it
        for document_data in documents_data:
            serializer = DocumentSerializer(data=document_data)
            if serializer.is_valid():
                document_instance = serializer.save()

                # Append necessary fields to the response
                saved_documents.append({
                    'document_id': document_instance.document_id,
                    'entity_type': document_instance.entity_type,
                    'document_type': document_instance.document_type,
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # Dealing with the Legal Compliance Data
        legal_compliance_str = request.data.get('legal_compliance')
        legal_compliance_data = {}
        legal_compliance_instance = None
        if legal_compliance_str:
            try:
                legal_compliance_data = json.loads(legal_compliance_str)
            except json.JSONDecodeError:
                return Response({'error': 'Invalid legal compliance format.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if any(value for value in legal_compliance_data.values() if value not in [None, '','null']):  # Exclude None, empty, and string 'null'
                legal_compliance_serializer = LegalComplianceSerializer(data=legal_compliance_data)
                if legal_compliance_serializer.is_valid():
                    legal_compliance_instance = legal_compliance_serializer.save()  # Create the LegalCompliance object
                else:
                    return Response(legal_compliance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        #  Dealing with Document Type and it's IDs for Role Reference
        for document in saved_documents:
            if document['document_type'] == 'Photo':
                photo_id = document['document_id'] 
            elif document['document_type'] == 'Bank':
                bank_doc_id = document['document_id']
            elif document['document_type'] == 'Identity':
                identity_doc_id = document['document_id'] 
            elif document['document_type'] == 'Address':
                address_doc_id = document['document_id']
            elif document['document_type'] == 'Land':
                land_doc_id = document['document_id'] 
            elif document['document_type'] == 'Education':
                education_doc_id = document['document_id']
       
        print("saved documents are ", saved_documents)
        agrimember_data = {
            'full_name' : request.data.get('full_name'),
            'fathers_or_husbands_name' : request.data.get('fathers_or_husbands_name'),
            'email' : request.data.get('email'),
            'date_of_birth' : request.data.get('date_of_birth'),
            'gender':request.data.get('gender'),
            'aadhaar_number' : request.data.get('aadhaar_number'),
            'phone_number' : request.data.get('phone_number'),
            'residential_address' : request.data.get('residential_address'),
            'designation' : request.data.get('designation'),
            'assigned_area' : request.data.get('assigned_area'),
            'supervisor_general_manager_id' : request.data.get('supervisor_general_manager_id'),
            'joining_date' : request.data.get('joining_date'),

            'identity_doc_id' : identity_doc_id if identity_doc_id else None,
            'address_doc_id' : address_doc_id if address_doc_id else None,
            'bank_doc_id' : bank_doc_id if bank_doc_id else None,
            'photo_id' : photo_id if photo_id else None,
            'education_doc_id' : education_doc_id if education_doc_id else None,
            'land_doc_id' : land_doc_id if land_doc_id else None,

            'legal_compliance_id' : legal_compliance_instance.compliance_id if legal_compliance_instance else None,
            'bank_details_id' : bank_details_object.bank_details_id if bank_details_object else None

        }

        agrimemeber_serializer = AgriMemberSerializer(data=agrimember_data)
        print("295 raa mama ", agrimemeber_serializer)
        if agrimemeber_serializer.is_valid():
            print("=========== Almost done ===============")
            agrimemeber_serializer.save()
            print("Done baby ")
            return Response(agrimemeber_serializer.data, status=status.HTTP_201_CREATED)
        return Response(agrimemeber_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgriMemberDetail(APIView):
    """
    Retrieve, update or delete an agri member instance.
    """
    def get_object(self, agri_member_id):
        try:
            return AgriMember.objects.get(agri_member_id=agri_member_id)
        except AgriMember.DoesNotExist:
            return None

    def get(self, request, agri_member_id):
        agri_member = self.get_object(agri_member_id)
        if agri_member is not None:
            serializer = AgriMemberSerializer(agri_member)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, agri_member_id):
        agri_member = self.get_object(agri_member_id)
        if agri_member is not None:
            serializer = AgriMemberSerializer(agri_member, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, agri_member_id):
        agri_member = self.get_object(agri_member_id)
        if agri_member is not None:
            agri_member.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


class FarmerList(APIView):
    """
    List all farmers or create a new farmer.
    """
    def get(self, request):
        farmers = Farmer.objects.all()
        serializer = FarmerSerializer(farmers, many=True)
        return Response(serializer.data)

    def post(self, request):
        identity_doc_id = None
        address_doc_id = None
        bank_doc_id = None
        education_doc_id = None
        photo_id = None
        land_doc_id = None

        # Dealing with Bank Details
        bank_details_str = request.data.get('bank_details')
        if not bank_details_str:
            return Response({'error': 'Bank details not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bank_details_data = json.loads(bank_details_str)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid bank details format.'}, status=status.HTTP_400_BAD_REQUEST)

        bank_details_serializer = BankDetailSerializer(data=bank_details_data)
        if bank_details_serializer.is_valid():
            bank_details_object = bank_details_serializer.save()  # Save bank details to the database
        else:
            return Response(bank_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Parse the incoming data for multiple documents
        documents_data = []
        index = 0
        while f'documents[{index}][document_type]' in request.data:
            document = {
                'document_type': request.data.get(f'documents[{index}][document_type]'),
                'entity_type': request.data.get(f'documents[{index}][entity_type]'),
                'document_path': request.FILES.get(f'documents[{index}][document_path]')
            }
            documents_data.append(document)
            index += 1
        if not documents_data:
            return Response({"error": "No documents provided."}, status=status.HTTP_400_BAD_REQUEST)

        saved_documents = []

        # Loop through each document and save it
        for document_data in documents_data:
            serializer = DocumentSerializer(data=document_data)
            if serializer.is_valid():
                document_instance = serializer.save()

                # Append necessary fields to the response
                saved_documents.append({
                    'document_id': document_instance.document_id,
                    'entity_type': document_instance.entity_type,
                    'document_type': document_instance.document_type,
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # Dealing with the Legal Compliance Data
        legal_compliance_str = request.data.get('legal_compliance')
        legal_compliance_data = {}
        legal_compliance_instance = None
        if legal_compliance_str:
            try:
                legal_compliance_data = json.loads(legal_compliance_str)
            except json.JSONDecodeError:
                return Response({'error': 'Invalid legal compliance format.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if any(value for value in legal_compliance_data.values() if value not in [None, '','null']):  # Exclude None, empty, and string 'null'
                legal_compliance_serializer = LegalComplianceSerializer(data=legal_compliance_data)
                if legal_compliance_serializer.is_valid():
                    legal_compliance_instance = legal_compliance_serializer.save()  # Create the LegalCompliance object
                else:
                    return Response(legal_compliance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        #  Dealing with Document Type and it's IDs for Role Reference
        for document in saved_documents:
            if document['document_type'] == 'Photo':
                photo_id = document['document_id'] 
            elif document['document_type'] == 'Bank':
                bank_doc_id = document['document_id']
            elif document['document_type'] == 'Identity':
                identity_doc_id = document['document_id'] 
            elif document['document_type'] == 'Address':
                address_doc_id = document['document_id']
            elif document['document_type'] == 'Land':
                land_doc_id = document['document_id'] 
            elif document['document_type'] == 'Education':
                education_doc_id = document['document_id']

         # Dealing with the Supervisor Agri Member Data
        agri_member_str = request.data.get('supervisor_agri_member')
        supervisor_agri_member_object = None
        if agri_member_str:
            try:
                agri_member_data = json.loads(agri_member_str)
            except json.JSONDecodeError:
                return Response({'error': 'Invalid agri member format.'}, status=status.HTTP_400_BAD_REQUEST)

            agri_member_serializer = AgriMemberSerializer(data=agri_member_data)
            if agri_member_serializer.is_valid():
                supervisor_agri_member_object = agri_member_serializer.save()  # Save the AgriMember object
            else:
                return Response(agri_member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
        print("saved documents are ", saved_documents)
        farmer_data = {
            'full_name' : request.data.get('full_name'),
            'fathers_or_husbands_name' : request.data.get('fathers_or_husbands_name'),
            'email' : request.data.get('email'),
            'date_of_birth' : request.data.get('date_of_birth'),
            'gender':request.data.get('gender'),
            'aadhaar_number' : request.data.get('aadhaar_number'),
            'phone_number' : request.data.get('phone_number'),
            'residential_address' : request.data.get('residential_address'),
            'village' : request.data.get('village'),
            'taluk' : request.data.get('taluk'),
            'district' : request.data.get('district'),
            'state' : request.data.get('state'),

            'identity_doc_id' : identity_doc_id if identity_doc_id else None,
            'address_doc_id' : address_doc_id if address_doc_id else None,
            'bank_doc_id' : bank_doc_id if bank_doc_id else None,
            'photo_id' : photo_id if photo_id else None,
            'education_doc_id' : education_doc_id if education_doc_id else None,
            'land_doc_id' : land_doc_id if land_doc_id else None,

            'legal_compliance_id' : legal_compliance_instance.compliance_id if legal_compliance_instance else None,
            'bank_details_id' : bank_details_object.bank_details_id if bank_details_object else None,
            'supervisor_agri_member_id' :  supervisor_agri_member_object.supervisor_agri_member_id if supervisor_agri_member_object else None

        }

        farmer_serializer = FarmerSerializer(data=farmer_data)
        print("295 raa mama ", farmer_serializer)
        if farmer_serializer.is_valid():
            print("=========== Almost done ===============")
            farmer_serializer.save()
            print("Done baby ")
            return Response(farmer_serializer.data, status=status.HTTP_201_CREATED)
        return Response(farmer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FarmerDetail(APIView):
    """
    Retrieve, update, or delete a farmer instance.
    """
    def get_object(self, farmer_id):
        try:
            return Farmer.objects.get(farmer_id=farmer_id)
        except Farmer.DoesNotExist:
            return None

    def get(self, request, farmer_id):
        farmer = self.get_object(farmer_id)
        if farmer is not None:
            serializer = FarmerSerializer(farmer)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, farmer_id):
        farmer = self.get_object(farmer_id)
        if farmer is not None:
            serializer = FarmerSerializer(farmer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, farmer_id):
        farmer = self.get_object(farmer_id)
        if farmer is not None:
            farmer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view!"})
    

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=205)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)
    


    