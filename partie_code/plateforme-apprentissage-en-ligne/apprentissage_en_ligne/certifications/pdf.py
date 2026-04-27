import qrcode # pyright: ignore[reportMissingModuleSource]
import io
from reportlab.lib.pagesizes import A4 # pyright: ignore[reportMissingModuleSource]
from reportlab.lib import colors # pyright: ignore[reportMissingModuleSource]
from reportlab.lib.units import cm # pyright: ignore[reportMissingModuleSource]
from reportlab.pdfgen import canvas # pyright: ignore[reportMissingModuleSource]
from reportlab.lib.styles import getSampleStyleSheet # pyright: ignore[reportMissingModuleSource]
from django.conf import settings


def generate_certificate_pdf(certification):
    buffer     = io.BytesIO()
    p          = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # ── background ──────────────────────────────────────────
    p.setFillColor(colors.HexColor('#F8F9FA'))
    p.rect(0, 0, width, height, fill=1, stroke=0)

    # ── gold border ─────────────────────────────────────────
    p.setStrokeColor(colors.HexColor('#D4AF37'))
    p.setLineWidth(8)
    p.rect(20, 20, width - 40, height - 40, fill=0, stroke=1)

    p.setStrokeColor(colors.HexColor('#D4AF37'))
    p.setLineWidth(2)
    p.rect(30, 30, width - 60, height - 60, fill=0, stroke=1)

    # ── platform name ────────────────────────────────────────
    p.setFillColor(colors.HexColor('#1D9E75'))
    p.setFont('Helvetica-Bold', 28)
    p.drawCentredString(width / 2, height - 100,
                        'Plateforme Apprentissage en Ligne')

    # ── divider ──────────────────────────────────────────────
    p.setStrokeColor(colors.HexColor('#D4AF37'))
    p.setLineWidth(1)
    p.line(80, height - 120, width - 80, height - 120)

    # ── certificate title ────────────────────────────────────
    p.setFillColor(colors.HexColor('#2C3E50'))
    p.setFont('Helvetica-Bold', 22)
    p.drawCentredString(width / 2, height - 170,
                        'CERTIFICAT DE RÉUSSITE')

    # ── this certifies ───────────────────────────────────────
    p.setFont('Helvetica', 14)
    p.setFillColor(colors.HexColor('#555555'))
    p.drawCentredString(width / 2, height - 220,
                        'Ce certificat est décerné à')

    # ── student name ─────────────────────────────────────────
    apprenant = certification.inscription.apprenant.utilisateur
    full_name = f"{apprenant.prenom} {apprenant.nom}".upper()
    p.setFont('Helvetica-Bold', 30)
    p.setFillColor(colors.HexColor('#1D9E75'))
    p.drawCentredString(width / 2, height - 270, full_name)

    # ── divider ──────────────────────────────────────────────
    p.setStrokeColor(colors.HexColor('#D4AF37'))
    p.line(120, height - 290, width - 120, height - 290)

    # ── for completing ───────────────────────────────────────
    p.setFont('Helvetica', 13)
    p.setFillColor(colors.HexColor('#555555'))
    p.drawCentredString(width / 2, height - 330,
                        'pour avoir complété avec succès le cours')

    # ── course name ──────────────────────────────────────────
    cours_titre = certification.inscription.cours.titre
    p.setFont('Helvetica-Bold', 18)
    p.setFillColor(colors.HexColor('#2C3E50'))
    p.drawCentredString(width / 2, height - 370, f'« {cours_titre} »')

    # ── module name ──────────────────────────────────────────
    module_titre = certification.inscription.cours.module.titre
    p.setFont('Helvetica', 13)
    p.setFillColor(colors.HexColor('#777777'))
    p.drawCentredString(width / 2, height - 400,
                        f'Module : {module_titre}')

    # ── date ─────────────────────────────────────────────────
    p.setFont('Helvetica', 12)
    p.setFillColor(colors.HexColor('#555555'))
    date_str = certification.date_emission.strftime('%d %B %Y')
    p.drawCentredString(width / 2, height - 450,
                        f'Délivré le : {date_str}')

    # ── validation code ──────────────────────────────────────
    p.setFont('Helvetica', 10)
    p.setFillColor(colors.HexColor('#999999'))
    p.drawCentredString(width / 2, height - 480,
                        f'Code de validation : {certification.code_validation}')

    # ── QR code ──────────────────────────────────────────────
    verify_url = f"{settings.FRONTEND_URL}/api/certifications/verify/{certification.code_validation}/"
    qr         = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(verify_url)
    qr.make(fit=True)
    qr_img     = qr.make_image(fill_color='black', back_color='white')

    qr_buffer  = io.BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)

    from reportlab.lib.utils import ImageReader # pyright: ignore[reportMissingModuleSource]
    qr_reader  = ImageReader(qr_buffer)
    qr_x       = width / 2 - 60
    qr_y       = height - 620
    p.drawImage(qr_reader, qr_x, qr_y, width=120, height=120)

    p.setFont('Helvetica', 9)
    p.setFillColor(colors.HexColor('#999999'))
    p.drawCentredString(width / 2, height - 630,
                        'Scannez pour vérifier l\'authenticité')

    # ── bottom line ──────────────────────────────────────────
    p.setStrokeColor(colors.HexColor('#D4AF37'))
    p.line(80, 80, width - 80, 80)

    p.setFont('Helvetica', 9)
    p.setFillColor(colors.HexColor('#999999'))
    p.drawCentredString(width / 2, 60,
                        'Plateforme Apprentissage en Ligne — Certificat officiel')

    p.save()
    buffer.seek(0)
    return buffer