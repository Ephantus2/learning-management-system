from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from assessment.models import Performance
from .pdf_utils import generate_transcript_pdf
from django.core.cache import cache

class TranscriptDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role != "STUDENT":
            raise PermissionDenied(
                "Only students can download their transcripts."
            )
        data = cache.get("transcript")

        if data is None:

            performances = Performance.objects.filter(
                student=user
            ).select_related("course", "academic_year")

            academic_year = request.query_params.get("academic_year")

            if academic_year:
                performances = performances.filter(
                    academic_year__name=academic_year
                )

            performances = performances.order_by(
                "academic_year",
                "course__code",
            )

            pdf_buffer = generate_transcript_pdf(
                student=user,
                performances=performances
            )

            data = pdf_buffer

            cache.set("transcript", data, timeout=300)

        return FileResponse(
            data,
            as_attachment=True,
            filename="academic_transcript.pdf",
            content_type="application/pdf"
        )