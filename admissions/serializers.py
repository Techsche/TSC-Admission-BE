from rest_framework import serializers

from .models import *

from PIL import Image

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


class ApplicationDetailSerializer(serializers.ModelSerializer):

    highest_qualification = serializers.PrimaryKeyRelatedField(
        queryset=EducationalQualification.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Application

        fields = [
            "id",
            "application_number",

            "full_name",
            "email",
            "mobile",

            "father_name",
            "father_mobile",
            "mother_name",
            "mother_mobile",

            "highest_qualification",

            "status",
            "profile_completed",
            "declaration_accepted",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "application_number",
            "status",
            "profile_completed",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):

        data = super().to_representation(instance)

        try:
            data["highest_qualification"] = (
                instance.education.highest_qualification_id
            )
        except Education.DoesNotExist:
            data["highest_qualification"] = None

        return data

    def update(self, instance, validated_data):

        highest_qualification = validated_data.pop(
            "highest_qualification",
            serializers.empty,
        )

        # Update Application fields
        instance = super().update(
            instance,
            validated_data,
        )

        # Update Education model
        if highest_qualification is not serializers.empty:

            Education.objects.update_or_create(
                application=instance,
                defaults={
                    "highest_qualification": highest_qualification,
                },
            )

        return instance
        
class EducationalQualificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EducationalQualification
        fields = ['id', 'qualification']    
        
        
        
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

    def validate_file(self, file):
        document_type = self.initial_data.get("document_type")

        if document_type not in {
            "qualification",
            "aadhaar",
            "photo",
            "signature",
        }:
            raise serializers.ValidationError(
                "Invalid document type."
            )

        # --------------------------------------------------
        # File size limits
        # --------------------------------------------------

        max_size = {
            "qualification": 10 * 1024 * 1024,  # 10 MB
            "aadhaar": 10 * 1024 * 1024,        # 10 MB
            "photo": 2 * 1024 * 1024,           # 2 MB
            "signature": 1 * 1024 * 1024,       # 1 MB
        }[document_type]

        if file.size > max_size:
            raise serializers.ValidationError(
                f"File size must not exceed "
                f"{max_size // (1024 * 1024)} MB."
            )

        # --------------------------------------------------
        # Allowed extensions
        # --------------------------------------------------

        allowed_extensions = {
            "qualification": {".pdf", ".jpg", ".jpeg", ".png"},
            "aadhaar": {".pdf", ".jpg", ".jpeg", ".png"},
            "photo": {".jpg", ".jpeg", ".png"},
            "signature": {".jpg", ".jpeg", ".png"},
        }

        filename = file.name.lower()

        if not any(
            filename.endswith(extension)
            for extension in allowed_extensions[document_type]
        ):
            raise serializers.ValidationError(
                "Invalid file type."
            )

        # --------------------------------------------------
        # Image validation
        # --------------------------------------------------

        if document_type in {"photo", "signature"}:

            try:
                image = Image.open(file)
                width, height = image.size

                # Make sure Django/Pillow actually verifies
                # the image contents.
                image.verify()

            except Exception:
                raise serializers.ValidationError(
                    "Invalid or corrupted image file."
                )

            # Reset file pointer after Pillow verification
            file.seek(0)

            if document_type == "photo":

                if not (
                    300 <= width <= 2000
                    and 400 <= height <= 2000
                ):
                    raise serializers.ValidationError(
                        "Photo dimensions must be between "
                        "300x400 and 2000x2000 pixels."
                    )

            elif document_type == "signature":

                if not (
                    400 <= width <= 2000
                    and 150 <= height <= 1000
                ):
                    raise serializers.ValidationError(
                        "Signature dimensions must be between "
                        "400x150 and 2000x1000 pixels."
                    )

        return file

    def validate_document_type(self, value):

        valid_types = {
            "qualification",
            "aadhaar",
            "photo",
            "signature",
        }

        if value not in valid_types:
            raise serializers.ValidationError(
                "Invalid document type."
            )

        return value
    
    
    
class ApplicationSubmitSerializer(serializers.Serializer):
    """
    Serializer used to validate an application before final submission.
    """

    def validate(self, attrs):
        application = self.context["application"]

        errors = {}

        # =====================================================
        # APPLICATION DETAILS
        # =====================================================

        required_fields = {
            "full_name": "Full name",
            "email": "Email",
            "mobile": "Mobile",
            "father_name": "Father name",
            "father_mobile": "Father mobile",
            "mother_name": "Mother name",
            "mother_mobile": "Mother mobile",
        }

        for field, label in required_fields.items():
            value = getattr(application, field, None)

            if not value or not str(value).strip():
                errors[field] = f"{label} is required."

        # =====================================================
        # EDUCATION
        # =====================================================

        try:
            education = application.education

            if not education.highest_qualification:
                errors["highest_qualification"] = (
                    "Highest qualification is required."
                )

        except Education.DoesNotExist:
            errors["highest_qualification"] = (
                "Highest qualification is required."
            )

        # =====================================================
        # DOCUMENTS
        # =====================================================

        required_documents = {
            "qualification": (
                "Highest qualification certificate"
            ),
            "aadhaar": "Aadhaar",
            "photo": "Photo",
            "signature": "Signature",
        }

        documents = {
            document.document_type: document
            for document in application.documents.all()
        }

        for document_type, label in required_documents.items():

            if document_type not in documents:
                errors[document_type] = (
                    f"{label} is required."
                )

        # =====================================================
        # DECLARATION
        # =====================================================

        if not application.declaration_accepted:
            errors["declaration_accepted"] = (
                "Declaration must be accepted before submission."
            )

        # =====================================================
        # RETURN VALIDATION ERRORS
        # =====================================================

        if errors:
            raise serializers.ValidationError(errors)

        return attrs