from django.db import transaction
from rest_framework import serializers

from .models import (
    Application,
    CurrentAddress,
    PermanentAddress,
    EducationalQualification,
    Education,
    Document,
)


# =============================================================
# APPLICATION START
# =============================================================

class ApplicationStartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application

        fields = [
            "id",
            "application_number",
            "status",
            "created_at",
        ]

        read_only_fields = fields


# =============================================================
# CURRENT ADDRESS
# =============================================================

class CurrentAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrentAddress

        fields = [
            "address_line1",
            "address_line2",
            "city",
            "district",
            "state",
            "pincode",
        ]


# =============================================================
# PERMANENT ADDRESS
# =============================================================

class PermanentAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermanentAddress

        fields = [
            "address_line1",
            "address_line2",
            "city",
            "district",
            "state",
            "pincode",
        ]


# =============================================================
# EDUCATIONAL QUALIFICATION
# =============================================================

class EducationalQualificationSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = EducationalQualification

        fields = [
            "id",
            "qualification",
        ]

        read_only_fields = fields


# =============================================================
# EDUCATION
# =============================================================

class EducationSerializer(serializers.ModelSerializer):

    highest_qualification = EducationalQualificationSerializer(
        read_only=True
    )

    class Meta:
        model = Education

        fields = [
            "highest_qualification",
        ]

        read_only_fields = fields


# =============================================================
# DOCUMENT
# =============================================================

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document

        fields = [
            "id",
            "document_type",
            "file",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "uploaded_at",
        ]


# =============================================================
# APPLICATION DETAIL
# =============================================================

class ApplicationDetailSerializer(
    serializers.ModelSerializer):

    # ---------------------------------------------------------
    # Read-only nested data
    # ---------------------------------------------------------

    current_address = CurrentAddressSerializer(
        read_only=True
    )

    permanent_address = PermanentAddressSerializer(
        read_only=True
    )

    education = EducationSerializer(
        read_only=True
    )

    documents = DocumentSerializer(
        many=True,
        read_only=True
    )

    # ---------------------------------------------------------
    # Flat Current Address Input
    # ---------------------------------------------------------

    current_address_line1 = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    current_address_line2 = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    current_city = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    current_district = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    current_state = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    current_pincode = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    # ---------------------------------------------------------
    # Flat Permanent Address Input
    # ---------------------------------------------------------

    permanent_address_line1 = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    permanent_address_line2 = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    permanent_city = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    permanent_district = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    permanent_state = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    permanent_pincode = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    # ---------------------------------------------------------
    # EDUCATION
    #
    # Angular sends:
    #
    # highest_qualification = 2
    #
    # This is validated against:
    #
    # EducationalQualification.id
    # ---------------------------------------------------------

    highest_qualification = serializers.PrimaryKeyRelatedField(
        queryset=EducationalQualification.objects.all(),
        required=False,
        write_only=True,
    )

    # ---------------------------------------------------------
    # DOCUMENT UPLOADS
    # ---------------------------------------------------------

    qualification = serializers.FileField(
        required=False,
        write_only=True,
    )

    aadhaar = serializers.FileField(
        required=False,
        write_only=True,
    )

    photo = serializers.ImageField(
        required=False,
        write_only=True,
    )

    signature = serializers.ImageField(
        required=False,
        write_only=True,
    )
    
    same_address = serializers.BooleanField(
        required=False,
    )

    # =========================================================
    # META
    # =========================================================

    class Meta:

        model = Application

        fields = [

            # -------------------------------------------------
            # Application
            # -------------------------------------------------

            "id",
            "application_number",
            "status",

            # -------------------------------------------------
            # Student
            # -------------------------------------------------

            "full_name",
            "email",
            "mobile",

            # -------------------------------------------------
            # Parents
            # -------------------------------------------------

            "father_name",
            "father_mobile",
            "mother_name",
            "mother_mobile",

            # -------------------------------------------------
            # Status
            # -------------------------------------------------

            "profile_completed",
            "declaration_accepted",
            "is_active",
            "created_at",
            "updated_at",

            # -------------------------------------------------
            # Addresses - GET
            # -------------------------------------------------

            "current_address",
            "permanent_address",

            # -------------------------------------------------
            # Education - GET
            # -------------------------------------------------

            "education",

            # -------------------------------------------------
            # Documents - GET
            # -------------------------------------------------

            "documents",

            # -------------------------------------------------
            # Current Address Input
            # -------------------------------------------------

            "current_address_line1",
            "current_address_line2",
            "current_city",
            "current_district",
            "current_state",
            "current_pincode",

            # -------------------------------------------------
            # Permanent Address Input
            # -------------------------------------------------

            "permanent_address_line1",
            "permanent_address_line2",
            "permanent_city",
            "permanent_district",
            "permanent_state",
            "permanent_pincode",

            # -------------------------------------------------
            # Address Copy
            # -------------------------------------------------

            "same_address",

            # -------------------------------------------------
            # Education Input
            # -------------------------------------------------

            "highest_qualification",

            # -------------------------------------------------
            # Documents Input
            # -------------------------------------------------

            "qualification",
            "aadhaar",
            "photo",
            "signature",
        ]

        read_only_fields = [
            "id",
            "application_number",
            "status",
            "profile_completed",
            "created_at",
            "updated_at",
        ]

    # =========================================================
    # VALIDATE FILE
    # =========================================================

    def validate_qualification(self, value):

        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError(
                "Highest qualification certificate must be "
                "10 MB or smaller."
            )

        allowed_types = [
            "application/pdf",
        ]

        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Highest qualification certificate must be a PDF."
            )

        return value

    # =========================================================
    # VALIDATE AADHAAR
    # =========================================================

    def validate_aadhaar(self, value):

        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError(
                "Aadhaar document must be 10 MB or smaller."
            )

        allowed_types = [
            "application/pdf",
            "image/jpeg",
            "image/png",
        ]

        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Aadhaar must be a PDF, JPG or PNG file."
            )

        return value

    # =========================================================
    # VALIDATE PHOTO
    # =========================================================

    def validate_photo(self, value):

        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "Photo must be 5 MB or smaller."
            )

        allowed_types = [
            "image/jpeg",
            "image/png",
        ]

        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Photo must be JPG or PNG."
            )

        return value

    # =========================================================
    # VALIDATE SIGNATURE
    # =========================================================

    def validate_signature(self, value):

        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "Signature must be 5 MB or smaller."
            )

        allowed_types = [
            "image/jpeg",
            "image/png",
        ]

        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Signature must be JPG or PNG."
            )

        return value
    
    
    # =========================================================
    # REPRESENTATION
    # =========================================================

    def to_representation(self, instance):
        data = super().to_representation(instance)

        current = getattr(instance, "current_address", None)
        permanent = getattr(instance, "permanent_address", None)

        if not current or not permanent:
            data["same_address"] = False
        else:
            data["same_address"] = (
                current.address_line1 == permanent.address_line1
                and current.address_line2 == permanent.address_line2
                and current.city == permanent.city
                and current.district == permanent.district
                and current.state == permanent.state
                and current.pincode == permanent.pincode
            )

        return data

    # =========================================================
    # UPDATE
    # =========================================================

    @transaction.atomic
    def update(self, instance, validated_data):

        # =====================================================
        # ADDRESS DATA
        # =====================================================

        current_address_data = {
            "address_line1": validated_data.pop(
                "current_address_line1",
                None,
            ),
            "address_line2": validated_data.pop(
                "current_address_line2",
                None,
            ),
            "city": validated_data.pop(
                "current_city",
                None,
            ),
            "district": validated_data.pop(
                "current_district",
                None,
            ),
            "state": validated_data.pop(
                "current_state",
                None,
            ),
            "pincode": validated_data.pop(
                "current_pincode",
                None,
            ),
        }

        permanent_address_data = {
            "address_line1": validated_data.pop(
                "permanent_address_line1",
                None,
            ),
            "address_line2": validated_data.pop(
                "permanent_address_line2",
                None,
            ),
            "city": validated_data.pop(
                "permanent_city",
                None,
            ),
            "district": validated_data.pop(
                "permanent_district",
                None,
            ),
            "state": validated_data.pop(
                "permanent_state",
                None,
            ),
            "pincode": validated_data.pop(
                "permanent_pincode",
                None,
            ),
        }

        same_address = validated_data.pop(
            "same_address",
            None,
        )

        # =====================================================
        # EDUCATION
        # =====================================================

        qualification = validated_data.pop(
            "highest_qualification",
            None,
        )

        # =====================================================
        # DOCUMENTS
        # =====================================================

        qualification_file = validated_data.pop(
            "qualification",
            None,
        )

        aadhaar_file = validated_data.pop(
            "aadhaar",
            None,
        )

        photo_file = validated_data.pop(
            "photo",
            None,
        )

        signature_file = validated_data.pop(
            "signature",
            None,
        )

        # =====================================================
        # UPDATE APPLICATION
        # =====================================================

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value,
            )

        instance.save()

        # =====================================================
        # CURRENT ADDRESS
        # =====================================================

        if any(
            value is not None
            for value in current_address_data.values()
        ):

            current_address, _ = (
                CurrentAddress.objects.get_or_create(
                    application=instance
                )
            )

            for field, value in current_address_data.items():

                if value is not None:

                    setattr(
                        current_address,
                        field,
                        value,
                    )

            current_address.save()

        # =====================================================
        # PERMANENT ADDRESS
        # =====================================================

        if same_address is True:

            current_address, _ = (
                CurrentAddress.objects.get_or_create(
                    application=instance
                )
            )

            PermanentAddress.objects.update_or_create(
                application=instance,
                defaults={
                    "address_line1":
                        current_address.address_line1,

                    "address_line2":
                        current_address.address_line2,

                    "city":
                        current_address.city,

                    "district":
                        current_address.district,

                    "state":
                        current_address.state,

                    "pincode":
                        current_address.pincode,
                },
            )

        elif any(
            value is not None
            for value in permanent_address_data.values()
        ):

            PermanentAddress.objects.update_or_create(
                application=instance,

                defaults={
                    field: value
                    for field, value
                    in permanent_address_data.items()
                    if value is not None
                },
            )

        # =====================================================
        # EDUCATION
        # =====================================================

        if qualification is not None:

            Education.objects.update_or_create(
                application=instance,

                defaults={
                    "highest_qualification": qualification,
                },
            )

        # =====================================================
        # DOCUMENT SAVE HELPER
        # =====================================================

        def save_document(
            document_type,
            uploaded_file,
        ):

            if uploaded_file is None:
                return

            Document.objects.update_or_create(
                application=instance,
                document_type=document_type,

                defaults={
                    "file": uploaded_file,
                },
            )

        # =====================================================
        # SAVE QUALIFICATION DOCUMENT
        # =====================================================

        save_document(
            "qualification",
            qualification_file,
        )

        # =====================================================
        # SAVE AADHAAR
        # =====================================================

        save_document(
            "aadhaar",
            aadhaar_file,
        )

        # =====================================================
        # SAVE PHOTO
        # =====================================================

        save_document(
            "photo",
            photo_file,
        )

        # =====================================================
        # SAVE SIGNATURE
        # =====================================================

        save_document(
            "signature",
            signature_file,
        )

        return instance


# =============================================================
# APPLICATION SUBMIT
# =============================================================

class ApplicationSubmitSerializer(
    serializers.Serializer
):

    def validate(self, attrs):

        application = self.context["application"]

        errors = {}

        # =====================================================
        # STUDENT
        # =====================================================

        if not application.full_name.strip():

            errors["full_name"] = (
                "Full name is required."
            )

        if not application.email.strip():

            errors["email"] = (
                "Email is required."
            )

        if not application.mobile.strip():

            errors["mobile"] = (
                "Mobile number is required."
            )

        # =====================================================
        # PARENTS
        # =====================================================

        if not application.father_name.strip():

            errors["father_name"] = (
                "Father name is required."
            )

        if not application.father_mobile.strip():

            errors["father_mobile"] = (
                "Father mobile is required."
            )

        if not application.mother_name.strip():

            errors["mother_name"] = (
                "Mother name is required."
            )

        if not application.mother_mobile.strip():

            errors["mother_mobile"] = (
                "Mother mobile is required."
            )

        # =====================================================
        # CURRENT ADDRESS
        # =====================================================

        try:

            current_address = (
                application.current_address
            )

        except CurrentAddress.DoesNotExist:

            current_address = None

        if current_address is None:

            errors["current_address"] = (
                "Current address is required."
            )

        else:

            if not current_address.address_line1.strip():

                errors["current_address_line1"] = (
                    "Current address is required."
                )

            if not current_address.city.strip():

                errors["current_city"] = (
                    "Current city is required."
                )

            if not current_address.district.strip():

                errors["current_district"] = (
                    "Current district is required."
                )

            if not current_address.state.strip():

                errors["current_state"] = (
                    "Current state is required."
                )

            if not current_address.pincode.strip():

                errors["current_pincode"] = (
                    "Current pincode is required."
                )

        # =====================================================
        # PERMANENT ADDRESS
        # =====================================================

        try:

            permanent_address = (
                application.permanent_address
            )

        except PermanentAddress.DoesNotExist:

            permanent_address = None

        if permanent_address is None:

            errors["permanent_address"] = (
                "Permanent address is required."
            )

        else:

            if not permanent_address.address_line1.strip():

                errors["permanent_address_line1"] = (
                    "Permanent address is required."
                )

            if not permanent_address.city.strip():

                errors["permanent_city"] = (
                    "Permanent city is required."
                )

            if not permanent_address.district.strip():

                errors["permanent_district"] = (
                    "Permanent district is required."
                )

            if not permanent_address.state.strip():

                errors["permanent_state"] = (
                    "Permanent state is required."
                )

            if not permanent_address.pincode.strip():

                errors["permanent_pincode"] = (
                    "Permanent pincode is required."
                )

        # =====================================================
        # EDUCATION
        # =====================================================

        try:

            education = application.education

        except Education.DoesNotExist:

            education = None

        if education is None:

            errors["highest_qualification"] = (
                "Highest qualification is required."
            )

        elif education.highest_qualification_id is None:

            errors["highest_qualification"] = (
                "Highest qualification is required."
            )

        # =====================================================
        # DOCUMENTS
        # =====================================================

        required_documents = [
            "qualification",
            "aadhaar",
            "photo",
            "signature",
        ]

        existing_documents = set(
            application.documents.values_list(
                "document_type",
                flat=True,
            )
        )

        for document_type in required_documents:

            if document_type not in existing_documents:

                errors[document_type] = (
                    f"{document_type.capitalize()} "
                    "document is required."
                )

        # =====================================================
        # DECLARATION
        # =====================================================

        if not application.declaration_accepted:

            errors["declaration_accepted"] = (
                "Declaration must be accepted."
            )

        # =====================================================
        # RETURN ERRORS
        # =====================================================

        if errors:

            raise serializers.ValidationError(
                errors
            )

        return attrs