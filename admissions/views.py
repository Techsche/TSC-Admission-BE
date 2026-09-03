from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ApplicationStartSerializer
from .services import create_application


from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .serializers import *
from .services import create_application

from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema, OpenApiExample



class StartApplicationView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Applications"],
        summary="Start a new admission application",
        description=(
            "Creates a new draft admission application and "
            "generates a unique application number for the current year."
        ),
        request=None,
        responses={
            201: ApplicationStartSerializer,
        },
    )
    def post(self, request):

        application, access_token = create_application()

        serializer = ApplicationStartSerializer(
            application
        )

        return Response(
            {
                "success": True,
                "data": {
                    **serializer.data,
                    "access_token": access_token,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class ApplicationDetailView(APIView):

    permission_classes = [AllowAny]

    # =========================================================
    # GET APPLICATION
    # =========================================================

    @extend_schema(
        tags=["Applications"],
        summary="Get admission application",
        description="Retrieves an existing admission application.",
        responses={
            200: ApplicationDetailSerializer,
            404: None,
        },
    )
    def get(self, request, pk):

        try:
            application = Application.objects.get(pk=pk)

        except Application.DoesNotExist:
            return Response(
                {
                    "detail": "Application not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ApplicationDetailSerializer(
            application
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # =========================================================
    # PATCH APPLICATION
    # =========================================================

    @extend_schema(
        tags=["Applications"],
        summary="Update admission application",
        description=(
            "Updates an existing draft admission application. "
            "Student, parent and education details can be "
            "saved incrementally while the application is in "
            "draft status."
        ),
        request=ApplicationDetailSerializer,
        responses={
            200: ApplicationDetailSerializer,
            400: None,
            404: None,
        },
    )
    def patch(self, request, pk):

        # -----------------------------------------------------
        # Get draft application
        # -----------------------------------------------------

        try:
            application = Application.objects.get(
                pk=pk,
                status="draft",
            )

        except Application.DoesNotExist:
            return Response(
                {
                    "detail": "Draft application not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # -----------------------------------------------------
        # Validate PATCH data
        # -----------------------------------------------------

        serializer = ApplicationDetailSerializer(
            application,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -----------------------------------------------------
        # Save
        #
        # Serializer.update() handles:
        #   - Application fields
        #   - Education record
        # -----------------------------------------------------

        serializer.save()

        # -----------------------------------------------------
        # Return updated application
        # -----------------------------------------------------

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
        
        
class EducationalQualificationListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Educational Qualifications"],
        summary="List all educational qualifications",
        description="Retrieves a list of all available educational qualifications.",
        responses={
            200: EducationalQualificationSerializer(many=True),
        },
    )
    def get(self, request):
        qualifications = EducationalQualification.objects.all()
        serializer = EducationalQualificationSerializer(qualifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class ApplicationDocumentUploadView(APIView):

    permission_classes = [AllowAny]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    @extend_schema(
        tags=["Documents"],
        summary="Upload application document",
        description=(
            "Uploads or replaces a document for an admission "
            "application. Supported document types are "
            "qualification, aadhaar, photo and signature."
        ),
        request=DocumentSerializer,
        responses={
            201: DocumentSerializer,
            400: None,
            404: None,
        },
        examples=[
            OpenApiExample(
                "Photo upload",
                value={
                    "document_type": "photo",
                    "file": "(binary file)",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Aadhaar upload",
                value={
                    "document_type": "aadhaar",
                    "file": "(binary file)",
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request, pk):

        # --------------------------------------------------
        # Find application
        # --------------------------------------------------

        try:
            application = Application.objects.get(
                pk=pk,
                status="draft",
            )
        except Application.DoesNotExist:
            return Response(
                {
                    "detail": "Draft application not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # --------------------------------------------------
        # Validate uploaded data
        # --------------------------------------------------

        serializer = DocumentSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        document_type = serializer.validated_data[
            "document_type"
        ]

        uploaded_file = serializer.validated_data["file"]

        # --------------------------------------------------
        # Replace existing document if present
        # --------------------------------------------------

        document, created = Document.objects.update_or_create(
            application=application,
            document_type=document_type,
            defaults={
                "file": uploaded_file,
            },
        )

        response_serializer = DocumentSerializer(
            document
        )

        return Response(
            response_serializer.data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )
        
        
class ApplicationSubmitView(APIView):

    permission_classes = [AllowAny]

    # =========================================================
    # FINAL SUBMIT APPLICATION
    # =========================================================

    @extend_schema(
        tags=["Applications"],
        summary="Submit admission application",
        description=(
            "Validates the complete draft application and "
            "changes its status from draft to pending."
        ),
        request=None,
        responses={
            200: ApplicationDetailSerializer,
            400: None,
            404: None,
        },
    )
    def post(self, request, pk):

        # -----------------------------------------------------
        # Get draft application
        # -----------------------------------------------------

        try:
            application = Application.objects.get(
                pk=pk,
                status="draft",
            )

        except Application.DoesNotExist:
            return Response(
                {
                    "detail": (
                        "Draft application not found "
                        "or already submitted."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # -----------------------------------------------------
        # Validate complete application
        # -----------------------------------------------------

        serializer = ApplicationSubmitSerializer(
            data={},
            context={
                "application": application,
            },
        )

        if not serializer.is_valid():

            return Response(
                {
                    "detail": "Application cannot be submitted.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # -----------------------------------------------------
        # Submit application
        # -----------------------------------------------------

        application.status = "pending"

        application.profile_completed = True

        application.save(
            update_fields=[
                "status",
                "profile_completed",
                "updated_at",
            ]
        )

        # -----------------------------------------------------
        # Return updated application
        # -----------------------------------------------------

        response_serializer = ApplicationDetailSerializer(
            application
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )