from io import BytesIO
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_transcript_pdf(student, performances):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()

    university_style = ParagraphStyle(
        "UniversityTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "TranscriptSubtitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    elements = []

    # University heading
    elements.append(
        Paragraph("KARATINA UNIVERSITY", university_style)
    )

    elements.append(
        Paragraph("ACADEMIC TRANSCRIPT", subtitle_style)
    )

    # Student details
    student_details = [
        ["Student Name:", str(student)],
        [
            "Registration Number:",
            str(getattr(student, "login_id", "N/A")),
        ],
    ]

    details_table = Table(
        student_details,
        colWidths=[45 * mm, 120 * mm],
    )

    details_table.setStyle(
        TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    elements.append(details_table)
    elements.append(Spacer(1, 15))

    # Performance table
    table_data = [
        [
            "Course Code",
            "Course Name",
            "Academic Year",
            "Marks",
            "Grade",
        ]
    ]

    for performance in performances:
        table_data.append([
            performance.course.code,
            performance.course.name,
            str(performance.academic_year),
            str(performance.total_marks),
            performance.grade,
        ])

    performance_table = Table(
        table_data,
        colWidths=[
            23 * mm,
            65 * mm,
            30 * mm,
            20 * mm,
            17 * mm,
        ],
        repeatRows=1,
    )

    performance_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#17365D"),
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),
            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                "Helvetica",
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8,
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey,
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP",
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                5,
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                5,
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),
        ])
    )

    elements.append(performance_table)
    elements.append(Spacer(1, 25))

    elements.append(
        Paragraph(
            f"Generated on: {date.today().strftime('%d %B %Y')}",
            styles["Normal"],
        )
    )

    document.build(elements)

    buffer.seek(0)

    return buffer