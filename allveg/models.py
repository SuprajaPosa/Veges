from django.db import models


class Districts(models.Model):
    district_id = models.AutoField(primary_key=True)
    district_name = models.CharField(max_length=30)

    def __str__(self):
        return self.district_name

    
    
class Taluks(models.Model):
    taluk_id = models.AutoField(primary_key=True)
    taluk_name = models.CharField(max_length=50)
    district_id = models.ForeignKey(Districts, on_delete=models.CASCADE)

    def __str__(self):
        return self.taluk_name

class Users(models.Model):
    ROLE_CHOICES = [
        ('Farmer', 'Farmer'),
        ('AgriMember', 'AgriMember'),
        ('Leader', 'Leader'),
        ('Manager', 'Manager'),
        ('GeneralManager', 'GeneralManager')
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ]

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Farmer', null=True, blank=True)
    full_name = models.CharField(max_length=65)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.full_name
    

class Documents(models.Model):
    ENTITY_TYPE_CHOICES = [
        ('Farmer', 'Farmer'),
        ('AgriMember', 'AgriMember'),
        ('Leader', 'Leader'),
        ('Manager', 'Manager'),
        ('GeneralManager', 'GeneralManager'),
    ]
    DOCUMENT_TYPE_CHOICES = [
        ('Identity', 'Identity'),
        ('Address', 'Address'),
        ('Bank', 'Bank'),
        ('Land', 'Land'),
        ('Photo', 'Photo'),
        ('Education', 'Education'),
        ('Other', 'Other'),
        ('Business', 'Business'),
        ('GST', 'GST'),
        ('PanCard', 'PanCard'),
        ('Vehicle_RC_Book', 'Vehicle_RC_Book'),
        ('Vehicle_Insurance', 'Vehicle_Insurance'),
        ('Driving_License', 'Driving_License'),
        ('Bank_Details','Bank_Details')
    ]

    document_id = models.AutoField(primary_key=True)
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES, default="Farmer")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    document_path = models.FileField(upload_to='', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('Users', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Document {self.document_id}"



class BankDetails(models.Model):
    ENTITY_TYPE_CHOICES = [
        ('Farmer', 'Farmer'),
        ('AgriMember', 'AgriMember'),
        ('Leader', 'Leader'),
        ('Manager', 'Manager'),
        ('GeneralManager', 'GeneralManager'),
    ]
    bank_details_id = models.AutoField(primary_key=True)
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES,default='Farmer')  
    bank_account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=50)
    bank_branch = models.CharField(max_length=50, null=True, blank=True)
    ifsc_code = models.CharField(max_length=11)
    upi_id = models.CharField(max_length=50, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,blank=True,related_name='bank_details')

    def __str__(self):
        return f"{self.bank_account_number}"
    
class Buyer(models.Model):
    BUYER_TYPE = [
        ('Street_Vendor',  'Street_Vendor'),
        ('Small_Store',  'Small_Store'),
        ('Big_Store',  'Big_Store'),
        ('Canteen', 'Canteen')
    ]
    buyer_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=65)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=30)
    address = models.CharField(max_length=100)
    buyer_type = models.CharField(max_length=20, choices=BUYER_TYPE, default='Canteen')
    business_name = models.CharField(max_length=100, null=True, blank=True)  # New field for Business Name
    pan_number = models.CharField(max_length=20, null=True, blank=True)  # New field for PAN Number

    business_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='business_documents')
    gst_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='gst_documents')
    pancard_doc_id = models.ForeignKey(Documents,on_delete=models.SET_NULL,null=True,blank=True,related_name='pancard_details')

    
    modified_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='b_bank_details')
    bank_details_id = models.ForeignKey(BankDetails, on_delete=models.SET_NULL, null=True, blank=True, related_name='b_bank_details')

    def __str__(self):
        return self.full_name

class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    driver_owner_full_name = models.CharField(max_length=65)
    driver_full_name = models.CharField(max_length=65)
    vehicle_name = models.CharField(max_length=100, null=True, blank=True)
    model_number = models.CharField(max_length=25)
    vehicle_registration_number = models.CharField(max_length=25)
    vehicle_insurance_number = models.CharField(max_length=15)
    
    # Change to DateField since it's a date
    vehicle_insurance_expiry_date = models.DateField()  
    
    driving_license_number = models.CharField(max_length=30)
    
    # Change to DateField since it's a date
    driving_license_expiry_date = models.DateField()

    # Foreign key relationships for document IDs
    vehicle_rc_book_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='v_vehicle_rc_book')
    vehicle_insurance_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='v_vehicle_insurance')
    driving_license_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='v_driving_license_doc_id')
    identity_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='v_identity_doc_id')
    pancard_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='v_pan_doc_id')
    photo_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='v_photo_id')
    bank_details_id = models.ForeignKey(BankDetails,on_delete=models.SET_NULL,null=True,blank=True,related_name='v_bank_details')

    def __str__(self):
        return f'{self.vehicle_name} - {self.driver_full_name}'



class LegalCompliance(models.Model):
    ENTITY_TYPE_CHOICES = [
        ('Farmer', 'Farmer'),
        ('AgriMember', 'AgriMember'),
        ('Leader', 'Leader'),
        ('Manager', 'Manager'),
        ('GeneralManager', 'GeneralManager'),
    ]
    
    compliance_id = models.AutoField(primary_key=True)
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES,default='Farmer')
    fpo_details = models.CharField(max_length=255, null=True, blank=True)
    fpo_membership = models.BooleanField(null=True, blank=True)  
    gst_number = models.CharField(max_length=50, null=True, blank=True)
    kcc_number = models.CharField(max_length=55, null=True, blank=True)
    registration_number = models.CharField(max_length=55, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(Users, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Compliance ID: {self.compliance_id}"


class GeneralManagers(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    general_manager_id = models.AutoField(primary_key=True) 
    
    full_name = models.CharField(max_length=50)
    fathers_or_husbands_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    aadhaar_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    
    residential_address = models.CharField(max_length=255)
    designation = models.CharField(max_length=55)
    assigned_city = models.CharField(max_length=55)
    joining_date = models.DateTimeField()
    employee_id = models.CharField(max_length=255, blank=True, null=True)

    identity_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='identity_documents')
    address_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='address_documents')
    bank_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='bank_documents')
    education_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='education_documents')
    photo_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='photo_documents')
    land_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='land_documents')
    legal_compliance_id = models.ForeignKey(LegalCompliance, on_delete=models.SET_NULL, null=True, blank=True, related_name='legal_compliances')
    bank_details_id = models.ForeignKey(BankDetails,on_delete=models.SET_NULL,null=True,blank=True,related_name='bank_details')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='updator')

    def __str__(self):
        return self.full_name
    
class Managers(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    manager_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    fathers_or_husbands_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    aadhaar_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    residential_address = models.TextField(null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    assigned_area = models.CharField(max_length=100, null=True, blank=True)
    supervisor_general_manager_id = models.IntegerField(null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    employee_id = models.CharField(max_length=100, unique=True, null=True, blank=True)

    identity_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='m_identity_documents')
    address_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='m_address_documents')
    bank_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='m_bank_documents')
    education_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='m_education_documents')
    photo_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='m_photo_documents')
    land_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='m_land_documents')
    legal_compliance_id = models.ForeignKey(LegalCompliance, on_delete=models.SET_NULL, null=True, blank=True, related_name='m_legal_compliances')
    bank_details_id = models.ForeignKey(BankDetails,on_delete=models.SET_NULL,null=True,blank=True,related_name='m_bank_details')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(Users,on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name
    
class Leader(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    leader_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    fathers_or_husbands_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    aadhaar_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    residential_address = models.TextField(null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    assigned_area = models.CharField(max_length=100, null=True, blank=True)
    supervisor_general_manager_id = models.IntegerField(null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    employee_id = models.CharField(max_length=100, unique=True, null=True, blank=True)

    identity_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='l_identity_documents')
    address_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='l_address_documents')
    bank_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='l_bank_documents')
    education_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='l_education_documents')
    photo_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='l_photo_documents')
    land_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='l_land_documents')
    legal_compliance_id = models.ForeignKey(LegalCompliance, on_delete=models.SET_NULL, null=True, blank=True, related_name='l_legal_compliances')
    bank_details_id = models.ForeignKey(BankDetails,on_delete=models.SET_NULL,null=True,blank=True,related_name='l_bank_details')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(Users,on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name
    
class AgriMember(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    agri_member_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    fathers_or_husbands_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    aadhaar_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    residential_address = models.TextField(null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    assigned_area = models.CharField(max_length=100, null=True, blank=True)
    supervisor_general_manager_id = models.IntegerField(null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)

    identity_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='ag_identity_documents')
    address_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='ag_address_documents')
    bank_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='ag_bank_documents')
    education_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='ag_education_documents')
    photo_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='ag_photo_documents')
    land_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='ag_land_documents')
    legal_compliance_id = models.ForeignKey(LegalCompliance, on_delete=models.SET_NULL, null=True, blank=True, related_name='ag_legal_compliances')
    bank_details_id = models.ForeignKey(BankDetails,on_delete=models.SET_NULL,null=True,blank=True,related_name='ag_bank_details')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(Users,on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name
    
class Farmer(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    farmer_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    fathers_or_husbands_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    aadhaar_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    residential_address = models.TextField(null=True, blank=True)
    village = models.CharField(max_length=100, null=True, blank=True)
    taluk = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)

    identity_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='f_identity_documents')
    address_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='f_address_documents')
    bank_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='f_bank_documents')
    education_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='f_education_documents')
    photo_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='f_photo_documents')
    land_doc_id = models.ForeignKey(Documents, on_delete=models.SET_NULL, null=True, blank=True, related_name='f_land_documents')
    legal_compliance_id = models.ForeignKey(LegalCompliance, on_delete=models.SET_NULL, null=True, blank=True, related_name='f_legal_compliances')
    bank_details_id = models.ForeignKey(BankDetails,on_delete=models.SET_NULL,null=True,blank=True,related_name='f_bank_details')
    supervisor_agri_member_id = models.ForeignKey(AgriMember, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervisor_agri_member_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(Users,on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name
    