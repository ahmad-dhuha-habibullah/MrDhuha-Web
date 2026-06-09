from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib import colors

OUTPUT = "/mnt/user-data/outputs/Modul_MATLAB_Klimatologi_Oseanografi.pdf"

# Color palette
C_DARK_BLUE   = HexColor("#0D2137")
C_MID_BLUE    = HexColor("#1A4A7A")
C_ACCENT      = HexColor("#2196F3")
C_LIGHT_BLUE  = HexColor("#E3F2FD")
C_TEAL        = HexColor("#00897B")
C_ORANGE      = HexColor("#F57C00")
C_LIGHT_GRAY  = HexColor("#F5F7FA")
C_BORDER_GRAY = HexColor("#CFD8DC")
C_TEXT        = HexColor("#212121")
C_SUBTEXT     = HexColor("#546E7A")
C_CODE_BG     = HexColor("#263238")
C_CODE_TEXT   = HexColor("#A5D6A7")
C_RED         = HexColor("#C62828")
C_GREEN       = HexColor("#2E7D32")

W, H = A4

def make_styles():
    styles = getSampleStyleSheet()

    def add(name, **kw):
        styles.add(ParagraphStyle(name=name, **kw))

    add("Cover_Title",
        fontName="Helvetica-Bold", fontSize=28, textColor=white,
        leading=36, alignment=TA_CENTER, spaceAfter=8)
    add("Cover_Sub",
        fontName="Helvetica", fontSize=14, textColor=HexColor("#B0C4DE"),
        leading=20, alignment=TA_CENTER, spaceAfter=6)
    add("Cover_Module",
        fontName="Helvetica-Bold", fontSize=16, textColor=HexColor("#FFD54F"),
        leading=22, alignment=TA_CENTER, spaceAfter=4)

    add("H1", fontName="Helvetica-Bold", fontSize=18, textColor=C_DARK_BLUE,
        leading=24, spaceBefore=20, spaceAfter=8)
    add("H2", fontName="Helvetica-Bold", fontSize=14, textColor=C_MID_BLUE,
        leading=20, spaceBefore=16, spaceAfter=6)
    add("H3", fontName="Helvetica-Bold", fontSize=12, textColor=C_TEAL,
        leading=18, spaceBefore=12, spaceAfter=4)

    add("Body", fontName="Helvetica", fontSize=10.5, textColor=C_TEXT,
        leading=16, alignment=TA_JUSTIFY, spaceAfter=6)
    add("BodyBold", fontName="Helvetica-Bold", fontSize=10.5, textColor=C_TEXT,
        leading=16, spaceAfter=4)
    add("Bullet", fontName="Helvetica", fontSize=10.5, textColor=C_TEXT,
        leading=16, leftIndent=16, bulletIndent=4, spaceAfter=3)
    add("BulletSub", fontName="Helvetica", fontSize=10, textColor=C_SUBTEXT,
        leading=15, leftIndent=30, bulletIndent=18, spaceAfter=2)

    add("Code", fontName="Courier", fontSize=9.5, textColor=C_CODE_TEXT,
        leading=14, backColor=C_CODE_BG, leftIndent=8, rightIndent=8,
        spaceAfter=2, spaceBefore=2)

    add("Caption", fontName="Helvetica-Oblique", fontSize=9, textColor=C_SUBTEXT,
        leading=13, alignment=TA_CENTER, spaceAfter=4)
    add("Note", fontName="Helvetica-Oblique", fontSize=9.5, textColor=C_SUBTEXT,
        leading=14, spaceAfter=4)
    add("TOC_H1", fontName="Helvetica-Bold", fontSize=11, textColor=C_DARK_BLUE,
        leading=18, spaceBefore=8, spaceAfter=2)
    add("TOC_H2", fontName="Helvetica", fontSize=10, textColor=C_MID_BLUE,
        leading=16, leftIndent=14, spaceAfter=1)
    add("TOC_H3", fontName="Helvetica", fontSize=9.5, textColor=C_SUBTEXT,
        leading=14, leftIndent=28, spaceAfter=1)
    add("ChapterLabel", fontName="Helvetica-Bold", fontSize=11, textColor=C_ACCENT,
        leading=16, spaceAfter=2)
    add("Small", fontName="Helvetica", fontSize=8.5, textColor=C_SUBTEXT,
        leading=12, spaceAfter=2)

    return styles

S = make_styles()

def hr(color=C_BORDER_GRAY, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=6, spaceBefore=4)

def h1(txt): return Paragraph(txt, S["H1"])
def h2(txt): return Paragraph(txt, S["H2"])
def h3(txt): return Paragraph(txt, S["H3"])
def body(txt): return Paragraph(txt, S["Body"])
def bold(txt): return Paragraph(txt, S["BodyBold"])
def bullet(txt, sub=False):
    st = S["BulletSub"] if sub else S["Bullet"]
    return Paragraph(f"• {txt}", st)
def code(txt):
    lines = txt.strip().split("\n")
    elems = []
    for ln in lines:
        elems.append(Paragraph(ln.replace(" ", "&nbsp;"), S["Code"]))
    return elems
def sp(n=6): return Spacer(1, n)
def note(txt): return Paragraph(f"<i>{txt}</i>", S["Note"])

def info_box(title, content_paras, bg=C_LIGHT_BLUE, border=C_ACCENT):
    inner = [[Paragraph(f"<b>{title}</b>", ParagraphStyle(
        "IBT", fontName="Helvetica-Bold", fontSize=10.5, textColor=C_DARK_BLUE, leading=15))]]
    for p in content_paras:
        inner.append([p])
    t = Table(inner, colWidths=[14.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("LINEAFTER", (0,0), (0,-1), 3, border),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [bg]),
    ]))
    return t

def section_banner(txt, color=C_MID_BLUE):
    p = Paragraph(f"<font color='white'><b>{txt}</b></font>",
                  ParagraphStyle("SB", fontName="Helvetica-Bold", fontSize=12,
                                 textColor=white, leading=18, alignment=TA_CENTER))
    t = Table([[p]], colWidths=[14.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), color),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    return t

# ─── PAGE TEMPLATES ──────────────────────────────────────────────────────────
def header_footer(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(C_DARK_BLUE)
    canvas.rect(0, H-28, W, 28, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(1.5*cm, H-19, "SERI BELAJAR MATLAB — Klimatologi & Oseanografi")
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(W-1.5*cm, H-19, doc.title if hasattr(doc, "title") else "")
    # Footer
    canvas.setFillColor(C_LIGHT_GRAY)
    canvas.rect(0, 0, W, 22, fill=1, stroke=0)
    canvas.setFillColor(C_SUBTEXT.clone())
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.5*cm, 7, "© 2025 — Seri Belajar MATLAB untuk Sains Atmosfer dan Kelautan")
    canvas.drawRightString(W-1.5*cm, 7, f"Halaman {doc.page}")
    canvas.restoreState()

def cover_page_template(canvas, doc):
    canvas.saveState()
    # Gradient-style background
    canvas.setFillColor(C_DARK_BLUE)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Accent stripe
    canvas.setFillColor(C_ACCENT)
    canvas.rect(0, H*0.42, W, 4, fill=1, stroke=0)
    canvas.setFillColor(C_TEAL)
    canvas.rect(0, H*0.42-6, W, 3, fill=1, stroke=0)
    canvas.restoreState()

# ─── DOCUMENT ────────────────────────────────────────────────────────────────
doc = BaseDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm,
)

content_frame = Frame(
    doc.leftMargin, doc.bottomMargin + 22,
    W - doc.leftMargin - doc.rightMargin,
    H - doc.topMargin - doc.bottomMargin - 50,
    id="content"
)
cover_frame = Frame(
    1.5*cm, H*0.43 + 10,
    W - 3*cm, H*0.52,
    id="cover"
)

doc.addPageTemplates([
    PageTemplate(id="cover", frames=[cover_frame], onPage=cover_page_template),
    PageTemplate(id="normal", frames=[content_frame], onPage=header_footer),
])

# ─── STORY ───────────────────────────────────────────────────────────────────
story = []

# ═══════════════════════════ COVER ═══════════════════════════════════════════
story.append(Spacer(1, 1.2*cm))
story.append(Paragraph("SERI BELAJAR MATLAB", S["Cover_Sub"]))
story.append(sp(4))
story.append(Paragraph("untuk Sains Atmosfer<br/>dan Kelautan", S["Cover_Title"]))
story.append(sp(16))
story.append(Paragraph("Kurikulum Lengkap 9 Modul", S["Cover_Module"]))
story.append(sp(8))
story.append(Paragraph(
    "Dari Instalasi hingga Analisis Marine Heatwave, ENSO, dan Publikasi Ilmiah",
    S["Cover_Sub"]))
story.append(sp(20))
story.append(Paragraph(
    "Ditujukan untuk Mahasiswa, Peneliti, dan Praktisi<br/>"
    "BMKG • BRIN • Perguruan Tinggi Indonesia",
    ParagraphStyle("CVS2", fontName="Helvetica", fontSize=11,
                   textColor=HexColor("#90CAF9"), leading=18, alignment=TA_CENTER)))
story.append(sp(30))
story.append(Paragraph("2025 | Edisi Pertama", S["Small"]))

story.append(PageBreak())

# ═══════════════════════════ KATA PENGANTAR ══════════════════════════════════
story.append(Paragraph("Kata Pengantar", S["H1"]))
story.append(hr(C_ACCENT, 1.5))
story.append(sp(4))
story.append(body(
    "Modul ini dirancang khusus untuk pemula Indonesia yang ingin belajar MATLAB "
    "dari nol dan menggunakannya secara langsung dalam analisis data iklim dan kelautan. "
    "Tidak ada asumsi pengetahuan pemrograman sebelumnya — semuanya dijelaskan secara "
    "bertahap, dengan contoh nyata dari konteks Indonesia."))
story.append(body(
    "Seri ini mencakup sembilan modul yang berurutan: mulai dari pengenalan antarmuka MATLAB, "
    "membaca data NetCDF, menggunakan Climate Data Toolbox, hingga studi kasus nyata seperti "
    "analisis Marine Heatwave, monitoring ENSO, dan persiapan paper publikasi."))
story.append(body(
    "Setiap modul dilengkapi dengan penjelasan konsep, kode MATLAB yang siap dijalankan, "
    "dan latihan mandiri. Pembaca didorong untuk mengikuti urutan modul karena setiap "
    "modul membangun pemahaman dari modul sebelumnya."))
story.append(sp(6))
story.append(info_box("Untuk Siapa Modul Ini?", [
    bullet("Mahasiswa S1/S2/S3 Meteorologi, Oseanografi, Geofisika"),
    bullet("Peneliti muda di BMKG, BRIN, LIPI"),
    bullet("Dosen yang ingin mengajar analisis data iklim dengan MATLAB"),
    bullet("Siapapun yang penasaran dengan pemrograman saintifik"),
]))
story.append(sp(10))
story.append(PageBreak())

# ═══════════════════════════ DAFTAR ISI ══════════════════════════════════════
story.append(Paragraph("Daftar Isi", S["H1"]))
story.append(hr(C_ACCENT, 1.5))
story.append(sp(4))

modules = [
    ("Modul 0", "Pengenalan MATLAB", [
        "0.1 Apa itu MATLAB?",
        "0.2 Kenapa Peneliti Masih Menggunakan MATLAB?",
        "0.3 Kelebihan dan Kekurangan MATLAB",
        "0.4 MATLAB vs Python untuk Klimatologi",
        "0.5 Instalasi MATLAB",
        "0.6 Mengenal Antarmuka MATLAB",
        "0.7 Script Pertama Anda",
        "0.8 Variabel dan Tipe Data",
        "0.9 Matriks dan Vektor",
        "0.10 Membuat Grafik Pertama",
    ]),
    ("Modul 1", "Dasar MATLAB untuk Data Iklim", [
        "1.1 Membaca Data NetCDF",
        "1.2 Memahami Dimensi Data",
        "1.3 Operasi Data 3D dan 4D",
        "1.4 Time Series",
        "1.5 Climatology dan Anomaly",
    ]),
    ("Modul 2", "Climate Data Toolbox", [
        "2.1 Apa itu Climate Data Toolbox?",
        "2.2 Instalasi Climate Data Toolbox",
        "2.3 Fungsi-fungsi Penting",
    ]),
    ("Modul 3", "Visualisasi Data Iklim", [
        "3.1 Plot SST Indonesia",
        "3.2 Plot Curah Hujan",
        "3.3 Plot Angin",
        "3.4 Streamline",
        "3.5 Peta Anomali",
        "3.6 Export Figure Publikasi",
    ]),
    ("Modul 4", "Studi Kasus ERA5", [
        "4.1 Download ERA5",
        "4.2 Membaca ERA5",
        "4.3 Climatology Bulanan",
        "4.4 Anomali",
        "4.5 Trend Linear",
    ]),
    ("Modul 5", "Studi Kasus OISST", [
        "5.1 Membaca OISST",
        "5.2 SST Climatology",
        "5.3 SST Anomaly",
        "5.4 ENSO Monitoring",
    ]),
    ("Modul 6", "Marine Heatwave", [
        "6.1 Konsep Marine Heatwave",
        "6.2 Percentile 90",
        "6.3 Threshold",
        "6.4 Deteksi Event",
        "6.5 Duration",
        "6.6 Intensity",
        "6.7 Mapping",
    ]),
    ("Modul 7", "Tropical Cyclone", [
        "7.1 IBTrACS",
        "7.2 Plot Track",
        "7.3 Density Map",
        "7.4 Composite Analysis",
        "7.5 TC vs Marine Heatwave",
    ]),
    ("Modul 8", "Proyek Nyata", [
        "8.1 Monitoring ENSO",
        "8.2 Monitoring IOD",
        "8.3 Dashboard Cuaca",
        "8.4 Analisis Marine Heatwave Indonesia",
        "8.5 Paper Publikasi dari Nol",
    ]),
]

for mod_num, mod_title, sections in modules:
    story.append(Paragraph(f"<b>{mod_num}</b> — {mod_title}", S["TOC_H1"]))
    for sec in sections:
        story.append(Paragraph(sec, S["TOC_H2"]))
    story.append(sp(4))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# MODUL 0
# ════════════════════════════════════════════════════════════════════════════
story.append(section_banner("MODUL 0 — PENGENALAN MATLAB"))
story.append(sp(10))
story.append(h1("Modul 0: Pengenalan MATLAB untuk Sains Atmosfer dan Kelautan"))
story.append(body(
    "Sebelum membahas data iklim atau toolbox canggih, kita perlu memahami terlebih dahulu "
    "apa itu MATLAB, bagaimana cara kerjanya, dan mengapa ia menjadi pilihan di banyak "
    "laboratorium penelitian di seluruh dunia — termasuk di Indonesia."))

# 0.1
story.append(h2("0.1 Apa itu MATLAB?"))
story.append(body(
    "MATLAB (Matrix Laboratory) adalah lingkungan komputasi numerik dan bahasa pemrograman "
    "yang dikembangkan oleh MathWorks. Pertama kali dirilis pada tahun 1984, MATLAB dirancang "
    "dengan filosofi utama: membuat operasi matriks dan vektor semudah menulis persamaan matematika."))
story.append(body(
    "Nama MATLAB sendiri merupakan singkatan dari <b>MATrix LABoratory</b>, yang mencerminkan "
    "fokus utamanya pada komputasi berbasis matriks. Hal ini menjadikannya sangat cocok untuk "
    "analisis data saintifik, di mana data iklim dan oseanografi selalu berbentuk array multidimensi."))
story.append(info_box("Fakta Menarik tentang MATLAB", [
    bullet("Dikembangkan pertama kali oleh Cleve Moler pada akhir 1970-an"),
    bullet("Versi komersial pertama dirilis tahun 1984 oleh MathWorks"),
    bullet("Saat ini digunakan oleh lebih dari 4 juta pengguna di seluruh dunia"),
    bullet("Tersedia dalam lebih dari 100 toolbox khusus untuk berbagai bidang ilmu"),
    bullet("Digunakan di NASA, CERN, BMKG, dan ribuan universitas riset"),
]))
story.append(sp(6))
story.append(h3("Siapa yang Menggunakan MATLAB di Indonesia?"))
story.append(bullet("BMKG — untuk pemrosesan data observasi dan model cuaca numerik"))
story.append(bullet("BRIN — untuk analisis data iklim dan riset kelautan"))
story.append(bullet("ITB, IPB, UGM, ITS — dalam mata kuliah dan thesis mahasiswa"))
story.append(bullet("LAPAN (kini BRIN) — untuk analisis citra satelit dan data atmosfer"))
story.append(bullet("Perusahaan migas — untuk pemrosesan data geofisika"))

# 0.2
story.append(h2("0.2 Kenapa Banyak Peneliti Masih Menggunakan MATLAB?"))
story.append(body(
    "Di era Python yang semakin populer, wajar jika Anda bertanya: mengapa masih belajar MATLAB? "
    "Jawabannya terletak pada ekosistem yang sudah matang dan sangat teroptimasi untuk sains."))
items_02 = [
    ("Visualisasi Instan", "Satu baris kode sudah menghasilkan grafik berkualitas tinggi. "
     "Tidak perlu import library, tidak perlu konfigurasi backend."),
    ("Matriks sebagai Tipe Data Utama", "Operasi array multidimensi terasa alami dan intuitif, "
     "sangat penting untuk data iklim 3D/4D."),
    ("Toolbox Saintifik Berkualitas", "Climate Data Toolbox, Signal Processing Toolbox, "
     "Statistics Toolbox — semuanya sudah terintegrasi dan diuji secara ketat."),
    ("Dokumentasi Luar Biasa", "Setiap fungsi memiliki dokumentasi lengkap dengan contoh "
     "yang bisa langsung dijalankan."),
    ("Debugging Interaktif", "Lingkungan Command Window memungkinkan eksplorasi data secara "
     "real-time tanpa perlu menulis program lengkap."),
    ("Legacy Kode Riset", "Banyak kode riset di jurnal internasional ditulis dalam MATLAB. "
     "Memahami MATLAB berarti bisa membaca dan mereplikasi hasil penelitian tersebut."),
]
for title, desc in items_02:
    story.append(KeepTogether([
        bold(f"◆ {title}"),
        body(desc),
        sp(4),
    ]))

# 0.3
story.append(h2("0.3 Kelebihan dan Kekurangan MATLAB"))

# Kelebihan table
kelebihan_data = [
    ["Aspek", "Penjelasan"],
    ["Mudah dipelajari", "Sintaks yang bersih dan intuitif untuk pemula"],
    ["Visualisasi sangat kuat", "plot(), imagesc(), surf() langsung menghasilkan grafik bagus"],
    ["Toolbox saintifik", "100+ toolbox resmi yang sudah teruji secara ilmiah"],
    ["Standar riset", "Banyak jurnal dan lab internasional menggunakan MATLAB"],
    ["Debugging mudah", "Workspace interaktif untuk inspeksi variabel real-time"],
    ["Dokumentasi kuat", "help(), doc(), dan portal online yang komprehensif"],
]
t_kelebihan = Table(kelebihan_data, colWidths=[4.5*cm, 10*cm])
t_kelebihan.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), C_GREEN),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9.5),
    ("BACKGROUND", (0,1), (-1,-1), HexColor("#F1F8E9")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, HexColor("#F1F8E9")]),
    ("GRID", (0,0), (-1,-1), 0.5, C_BORDER_GRAY),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(h3("Kelebihan MATLAB"))
story.append(t_kelebihan)
story.append(sp(10))

kekurangan_data = [
    ["Aspek", "Penjelasan"],
    ["Berbayar", "Lisensi komersial bisa sangat mahal; butuh lisensi kampus/institusi"],
    ["Ekosistem lebih kecil", "Komunitas lebih kecil dibanding Python; lebih sedikit paket pihak ketiga"],
    ["Kurang fleksibel", "Tidak ideal untuk aplikasi web, mobile, atau production software"],
    ["Ketergantungan MATLAB", "File .m dan .mat tidak bisa dijalankan tanpa MATLAB (atau Octave)"],
    ["Kecepatan eksekusi", "Lebih lambat dari C/Fortran; bisa jadi kendala untuk data sangat besar"],
]
t_kekurangan = Table(kekurangan_data, colWidths=[4.5*cm, 10*cm])
t_kekurangan.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), C_RED),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9.5),
    ("BACKGROUND", (0,1), (-1,-1), HexColor("#FFF3E0")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, HexColor("#FFF3E0")]),
    ("GRID", (0,0), (-1,-1), 0.5, C_BORDER_GRAY),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(h3("Kekurangan MATLAB"))
story.append(t_kekurangan)

# 0.4
story.append(h2("0.4 MATLAB vs Python untuk Klimatologi"))
story.append(body(
    "Pertanyaan paling sering dari pemula: \"Haruskah saya belajar MATLAB atau Python?\" "
    "Jawabannya bergantung pada konteks dan tujuan Anda. Berikut perbandingan objektif keduanya:"))

comp_data = [
    ["Kriteria", "MATLAB", "Python"],
    ["Harga", "Berbayar (ada lisensi kampus)", "Gratis & open source"],
    ["Kemudahan belajar", "Sangat mudah untuk pemula", "Mudah, kurva belajar sedikit lebih panjang"],
    ["Visualisasi", "Sangat kuat, built-in", "Kuat (matplotlib, seaborn, cartopy)"],
    ["Data NetCDF", "ncread, ncinfo built-in", "xarray, netCDF4 (install dulu)"],
    ["Komunitas global", "Sedang", "Sangat besar"],
    ["Machine Learning", "Baik (ML Toolbox)", "Unggul (scikit-learn, TensorFlow)"],
    ["Operasional BMKG", "Digunakan", "Semakin banyak digunakan"],
    ["Riset akademik", "Standar di banyak lab", "Semakin dominan"],
    ["Climate Data Toolbox", "Tersedia resmi", "Tidak ada padanan langsung"],
    ["Legacy kode riset", "Sangat banyak", "Sedang berkembang"],
]
t_comp = Table(comp_data, colWidths=[4*cm, 5.25*cm, 5.25*cm])
t_comp.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), C_DARK_BLUE),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("BACKGROUND", (1,1), (1,-1), HexColor("#E3F2FD")),
    ("BACKGROUND", (2,1), (2,-1), HexColor("#E8F5E9")),
    ("ROWBACKGROUNDS", (0,1), (0,-1), [HexColor("#FAFAFA"), HexColor("#F5F5F5")]),
    ("GRID", (0,0), (-1,-1), 0.5, C_BORDER_GRAY),
    ("LEFTPADDING", (0,0), (-1,-1), 7),
    ("RIGHTPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(t_comp)
story.append(sp(6))
story.append(note(
    "💡 Rekomendasi: Untuk pemula di bidang iklim/oseanografi Indonesia, mulai dari MATLAB "
    "karena kemudahannya. Setelah mahir, menambah Python akan jauh lebih mudah."))

# 0.5
story.append(h2("0.5 Instalasi MATLAB"))
story.append(body(
    "Untuk menggunakan MATLAB, Anda membutuhkan lisensi yang valid. Beberapa opsi yang tersedia:"))
story.append(bullet("<b>Lisensi Kampus/Institusi:</b> Banyak universitas Indonesia (ITB, UI, UGM, ITS, dll) "
    "memiliki perjanjian lisensi dengan MathWorks. Tanyakan ke UPT TIK kampus Anda."))
story.append(bullet("<b>MATLAB Online:</b> Tersedia melalui mathworks.com/products/matlab-online.html — "
    "tidak perlu instalasi, berjalan di browser."))
story.append(bullet("<b>Student License:</b> Tersedia dengan harga terjangkau untuk mahasiswa aktif."))
story.append(bullet("<b>Trial Version:</b> MathWorks menyediakan trial 30 hari gratis."))
story.append(sp(6))

install_steps = [
    ["Langkah", "Aksi"],
    ["1", "Buka mathworks.com dan buat akun MathWorks"],
    ["2", "Pilih 'Get MATLAB' dan masukkan lisensi Anda"],
    ["3", "Download installer sesuai OS (Windows/macOS/Linux)"],
    ["4", "Jalankan installer dan ikuti wizard instalasi"],
    ["5", "Aktivasi menggunakan akun MathWorks saat pertama kali membuka"],
    ["6", "Pilih toolbox yang dibutuhkan (minimal: Statistics, Signal Processing)"],
]
t_install = Table(install_steps, colWidths=[1.5*cm, 13*cm])
t_install.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), C_TEAL),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("BACKGROUND", (0,1), (0,-1), HexColor("#E0F2F1")),
    ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9.5),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, HexColor("#F1FFFE")]),
    ("GRID", (0,0), (-1,-1), 0.5, C_BORDER_GRAY),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("ALIGN", (0,0), (0,-1), "CENTER"),
]))
story.append(t_install)
story.append(sp(6))
story.append(h3("Struktur Folder MATLAB"))
story.append(body(
    "Setelah terinstal, MATLAB biasanya membuat folder <b>MATLAB</b> di direktori Documents Anda. "
    "Gunakan folder ini sebagai tempat menyimpan semua script dan data Anda. Membuat subfolder "
    "untuk setiap proyek adalah kebiasaan yang sangat dianjurkan:"))
story.append(sp(4))
for ln in code("""Documents/
  MATLAB/
    Modul_0_Pengenalan/
    Modul_1_DataIklim/
    Data/
      ERA5/
      OISST/
    Hasil/"""):
    story.append(ln)

# 0.6
story.append(h2("0.6 Mengenal Antarmuka MATLAB"))
story.append(body(
    "Ketika pertama kali membuka MATLAB, Anda akan melihat tampilan yang mungkin terasa asing. "
    "Jangan khawatir — setiap komponen memiliki fungsi yang jelas dan akan terasa intuitif "
    "setelah beberapa jam penggunaan."))

ui_items = [
    ("Command Window", "Ini adalah jantung MATLAB. Di sini Anda bisa mengetik perintah "
     "dan melihat hasilnya secara langsung. Mirip dengan kalkulator super canggih. "
     "Tandanya adalah prompt >> yang menunggu input Anda."),
    ("Workspace", "Panel di kanan atas yang menampilkan semua variabel yang sedang aktif "
     "dalam memori. Anda bisa melihat nama variabel, tipe data, ukuran, dan nilainya. "
     "Sangat berguna untuk memahami data Anda."),
    ("Current Folder", "Panel di kiri yang menampilkan isi folder kerja saat ini. Dari sini "
     "Anda bisa membuka file .m, file data, atau berpindah direktori."),
    ("Editor", "Tempat menulis script dan function yang lebih panjang. Mendukung "
     "syntax highlighting, auto-indent, dan debugging. Buka dengan mengetik 'edit' di "
     "Command Window atau klik New Script."),
    ("Figure Window", "Jendela terpisah yang muncul ketika Anda membuat grafik. "
     "Bisa diperbesar, disimpan, atau diedit interaktif langsung dari tampilan."),
    ("Command History", "Rekam jejak semua perintah yang pernah Anda ketik. "
     "Tekan tombol ↑ di Command Window untuk menelusuri riwayat perintah."),
]
for title, desc in ui_items:
    story.append(KeepTogether([
        bold(f"▸ {title}"),
        body(desc),
        sp(4),
    ]))

# 0.7
story.append(h2("0.7 Script Pertama Anda"))
story.append(body(
    "Mari kita mulai dengan tradisi klasik pemrograman. Ketik baris berikut di Command Window "
    "dan tekan Enter:"))
for ln in code("disp('Halo Dunia')"):
    story.append(ln)
story.append(sp(4))
story.append(body("MATLAB akan menampilkan:"))
for ln in code("Halo Dunia"):
    story.append(ln)
story.append(sp(4))
story.append(body(
    "Selamat! Anda baru saja menjalankan program pertama Anda di MATLAB. Sekarang mari kita "
    "coba beberapa perintah dasar lagi:"))
for ln in code("""% Ini adalah komentar — baris yang dimulai dengan % diabaikan MATLAB
disp('Halo dari MATLAB!')

% Operasi matematika sederhana
2 + 3
10 * 4
sqrt(16)    % Akar kuadrat dari 16

% Menampilkan teks dan angka
fprintf('Nilai pi = %.4f\\n', pi)
fprintf('Akar kuadrat 2 = %.6f\\n', sqrt(2))"""):
    story.append(ln)
story.append(sp(4))
story.append(info_box("Tips: Menekan Tab untuk Autocomplete", [
    body("Saat mengetik nama fungsi di Command Window, tekan Tab untuk melihat saran autocomplete. "
         "Ini sangat berguna untuk menemukan fungsi yang lupa namanya."),
]))

# 0.8
story.append(h2("0.8 Variabel dan Tipe Data"))
story.append(body(
    "Variabel di MATLAB dibuat tanpa deklarasi tipe data terlebih dahulu. MATLAB secara otomatis "
    "menentukan tipe berdasarkan nilai yang Anda masukkan:"))
for ln in code("""% Membuat variabel
suhu = 28.5          % double (angka desimal)
nama = 'Jakarta'     % char (teks/string)
aktif = true         % logical (benar/salah)
tahun = 2024         % double (MATLAB default angka = double)

% Memeriksa tipe data
class(suhu)          % Hasil: 'double'
class(nama)          % Hasil: 'char'
whos                 % Tampilkan semua variabel di Workspace"""):
    story.append(ln)
story.append(sp(6))

tipe_data = [
    ["Tipe Data", "Keterangan", "Contoh"],
    ["double", "Angka desimal (64-bit) — TIPE DEFAULT", "x = 3.14"],
    ["single", "Angka desimal (32-bit) — hemat memori", "x = single(3.14)"],
    ["int32", "Bilangan bulat 32-bit", "x = int32(100)"],
    ["char", "Karakter dan teks (string lama)", "s = 'Jakarta'"],
    ["string", "String modern (sejak R2016b)", 's = "Jakarta"'],
    ["logical", "Nilai benar/salah (true/false)", "flag = true"],
    ["cell", "Array yang bisa menyimpan tipe berbeda", "c = {1, 'a', [1 2]}"],
    ["struct", "Struktur data dengan field bernama", "s.nama = 'Ali'"],
]
t_tipe = Table(tipe_data, colWidths=[3*cm, 7*cm, 4.5*cm])
t_tipe.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), C_MID_BLUE),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, C_LIGHT_GRAY]),
    ("GRID", (0,0), (-1,-1), 0.5, C_BORDER_GRAY),
    ("LEFTPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("FONTNAME", (2,1), (2,-1), "Courier"),
    ("FONTSIZE", (2,1), (2,-1), 9),
]))
story.append(t_tipe)

# 0.9
story.append(h2("0.9 Matriks dan Vektor"))
story.append(body(
    "Ini adalah bagian terpenting dari MATLAB. Ingat: MATLAB = MATrix LABoratory. "
    "Semua data di MATLAB pada dasarnya adalah matriks, bahkan angka tunggal pun dianggap "
    "sebagai matriks 1×1."))
for ln in code("""% ── Membuat Vektor ──────────────────────────────────────
v_baris = [1 2 3 4 5]         % Vektor baris (1x5)
v_kolom = [1; 2; 3; 4; 5]     % Vektor kolom (5x1)
v_range = 1:10                 % Vektor 1 sampai 10
v_step  = 0:0.5:5              % Vektor 0 sampai 5, step 0.5
v_linsp = linspace(0, 1, 100)  % 100 titik dari 0 ke 1

% ── Membuat Matriks ──────────────────────────────────────
A = [1 2 3; 4 5 6; 7 8 9]     % Matriks 3x3

% ── Informasi Ukuran ─────────────────────────────────────
size(A)          % [3 3] — baris dan kolom
size(A, 1)       % 3 — jumlah baris
size(A, 2)       % 3 — jumlah kolom
numel(A)         % 9 — total elemen
length(v_baris)  % 5 — dimensi terpanjang

% ── Indexing (Mengakses Elemen) ───────────────────────────
A(2, 3)          % Baris ke-2, kolom ke-3 = 6
A(1, :)          % Seluruh baris ke-1 = [1 2 3]
A(:, 2)          % Seluruh kolom ke-2 = [2; 5; 8]
A(2:3, 1:2)      % Sub-matriks baris 2-3, kolom 1-2

% ── Operasi Matriks ───────────────────────────────────────
B = A * A        % Perkalian matriks
C = A .* A       % Perkalian elemen per elemen (elemenwise)
D = A + 10       % Tambahkan 10 ke semua elemen
E = A > 5        % Logical: elemen mana yang > 5?

% ── Fungsi Berguna ────────────────────────────────────────
zeros(3, 4)      % Matriks 3x4 berisi nol
ones(2, 5)       % Matriks 2x5 berisi satu
eye(4)           % Matriks identitas 4x4
rand(3, 3)       % Matriks 3x3 angka acak [0,1]
nan(2, 6)        % Matriks berisi NaN — berguna untuk missing data"""):
    story.append(ln)
story.append(sp(6))
story.append(info_box("Mengapa Ini Penting untuk Data Iklim?", [
    body("Data iklim selalu berupa array multidimensi. Misalnya, data SST dari OISST berukuran "
         "[1440 × 720 × 365] yang berarti 1440 titik bujur, 720 titik lintang, dan 365 hari. "
         "MATLAB sangat efisien dalam menangani operasi pada array sebesar ini dengan sintaks "
         "yang ringkas dan intuitif."),
]))

# 0.10
story.append(h2("0.10 Membuat Grafik Pertama"))
story.append(body(
    "Salah satu kekuatan terbesar MATLAB adalah kemampuan visualisasinya. Mari kita buat "
    "beberapa grafik sederhana yang relevan dengan data iklim:"))
for ln in code("""% ── Grafik 1: Plot Garis (Time Series Sederhana) ─────────────
bulan = 1:12;
curah_hujan = [180 160 120 90 70 50 45 55 95 130 175 200];

figure(1)
plot(bulan, curah_hujan, 'b-o', 'LineWidth', 2, 'MarkerSize', 6)
xlabel('Bulan')
ylabel('Curah Hujan (mm)')
title('Pola Curah Hujan Bulanan Jakarta')
xticks(1:12)
xticklabels({'Jan','Feb','Mar','Apr','Mei','Jun', ...
             'Jul','Agu','Sep','Okt','Nov','Des'})
grid on
xlim([1 12])

% ── Grafik 2: Plot dengan Multiple Lines ──────────────────
suhu_max = [32 32 33 34 35 35 34 34 34 33 32 31];
suhu_min = [24 24 25 25 26 25 24 24 24 24 24 24];

figure(2)
plot(bulan, suhu_max, 'r-s', 'LineWidth', 2)
hold on
plot(bulan, suhu_min, 'b-s', 'LineWidth', 2)
hold off
legend('Suhu Maksimum', 'Suhu Minimum')
xlabel('Bulan')
ylabel('Suhu (C)')
title('Suhu Bulanan Jakarta')
grid on

% ── Grafik 3: Peta Kontur Sederhana ───────────────────────
[lon, lat] = meshgrid(-10:1:10, -10:1:10);
SST = 28 + 2*sin(lon/5) + cos(lat/3);  % SST buatan

figure(3)
contourf(lon, lat, SST, 20, 'LineColor', 'none')
colorbar
colormap('jet')
xlabel('Longitude')
ylabel('Latitude')
title('Contoh Peta SST (Data Simulasi)')"""):
    story.append(ln)
story.append(sp(6))
story.append(note(
    "Selamat! Anda telah menyelesaikan Modul 0. Anda sekarang memahami dasar-dasar MATLAB "
    "yang cukup untuk mulai bekerja dengan data iklim nyata di modul-modul berikutnya."))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# MODUL 1
# ════════════════════════════════════════════════════════════════════════════
story.append(section_banner("MODUL 1 — DASAR MATLAB UNTUK DATA IKLIM", C_TEAL))
story.append(sp(10))
story.append(h1("Modul 1: Dasar MATLAB untuk Data Iklim"))
story.append(body(
    "Setelah menguasai dasar MATLAB, kita masuk ke dunia data iklim yang nyata. "
    "Format data yang paling umum di bidang ini adalah NetCDF (Network Common Data Form), "
    "sebuah format biner yang dirancang khusus untuk data saintifik multidimensi."))

story.append(h2("1.1 Membaca Data NetCDF"))
story.append(body(
    "NetCDF adalah format standar untuk menyimpan data atmosfer dan kelautan. "
    "File NetCDF memiliki ekstensi .nc dan berisi variabel, dimensi, dan atribut."))
story.append(body("MATLAB memiliki fungsi built-in untuk membaca NetCDF tanpa toolbox tambahan:"))
for ln in code("""% ── Melihat Isi File NetCDF ───────────────────────────────
filename = 'sst_data.nc';

% Melihat informasi file
info = ncinfo(filename)
disp(info.Variables)    % Lihat daftar variabel
disp(info.Dimensions)   % Lihat dimensi

% ── Membaca Variabel Tertentu ─────────────────────────────
sst  = ncread(filename, 'sst');       % Baca variabel SST
lon  = ncread(filename, 'longitude'); % Baca longitude
lat  = ncread(filename, 'latitude');  % Baca latitude
time = ncread(filename, 'time');      % Baca waktu

% Periksa ukuran data
fprintf('Ukuran SST: %d x %d x %d\\n', size(sst))
fprintf('Range lon: %.1f sampai %.1f\\n', min(lon), max(lon))
fprintf('Range lat: %.1f sampai %.1f\\n', min(lat), max(lat))

% ── Membaca Sebagian Data (Efficient) ─────────────────────
% Hanya baca data Indonesia: lon 95-141E, lat 11S-6N
i_lon = find(lon >= 95 & lon <= 141);
i_lat = find(lat >= -11 & lat <= 6);

sst_indo = ncread(filename, 'sst', ...
    [i_lon(1), i_lat(1), 1], ...
    [length(i_lon), length(i_lat), Inf]);"""):
    story.append(ln)

story.append(h2("1.2 Memahami Dimensi Data"))
story.append(body(
    "Data iklim gridded memiliki struktur dimensi yang perlu dipahami. "
    "Format paling umum adalah (lon × lat × time) atau (lon × lat × level × time)."))
for ln in code("""% Contoh: Data ERA5 suhu permukaan
% Ukuran: [480 × 241 × 12] = [lon × lat × bulan]

% Mengakses snapshot tertentu
sst_jan = sst(:, :, 1);    % Bulan Januari
sst_jul = sst(:, :, 7);    % Bulan Juli

% Mean spasial (rata-rata di semua grid point)
sst_mean_jan = mean(sst_jan(:));    % Rata-rata global Januari

% Mean temporal (rata-rata sepanjang waktu)
% squeeze() menghilangkan dimensi tunggal
sst_clim = mean(sst, 3);           % Rata-rata semua bulan
sst_clim_sq = squeeze(mean(sst, 3));  % Hasilnya 2D

% Perbedaan penting: dimensi longitude-first
% Di MATLAB: sst(i_lon, i_lat, i_time)
% Di Python/xarray: sst.sel(time=..., lat=..., lon=...)"""):
    story.append(ln)

story.append(h2("1.3 Operasi Data 3D dan 4D"))
for ln in code("""% ── Data 4D: lon x lat x level x time ───────────────────
% Contoh: angin zonal ERA5 dengan 17 level pressure
% u_wind ukuran: [480 x 241 x 17 x 12]

% Slice pada level 850 hPa (misalnya level ke-5)
u_850 = u_wind(:, :, 5, :);       % 4D, level ke-5
u_850_sq = squeeze(u_wind(:,:,5,:)); % 3D: lon x lat x time

% Rata-rata vertikal (mean di semua level)
u_vmean = mean(u_wind, 3);        % Rata-rata dimensi ke-3 (level)

% Rata-rata temporal
u_tmean = mean(u_wind, 4);        % Rata-rata dimensi ke-4 (time)

% Anomali = data - mean temporal
u_anom = u_wind - repmat(u_tmean, [1 1 1 size(u_wind,4)]);

% Fungsi bsxfun (lebih efisien untuk data besar)
u_anom2 = bsxfun(@minus, u_wind, u_tmean);"""):
    story.append(ln)

story.append(h2("1.4 Time Series"))
for ln in code("""% ── Membuat Time Series dari Data Iklim ─────────────────
% Rata-rata area: SST wilayah Nino3.4 (190-240E, 5S-5N)

% Tentukan batas wilayah
i_lon34 = find(lon >= 190 & lon <= 240);
i_lat34 = find(lat >= -5 & lat <= 5);

% Ekstrak data wilayah
sst_nino34 = sst(i_lon34, i_lat34, :);

% Rata-rata spasial menggunakan mean ganda
nino34_ts = squeeze(mean(mean(sst_nino34, 1), 2));
% atau lebih ringkas:
nino34_ts = squeeze(mean(sst_nino34(:), 1));  % Salah! mean semua dimensi

% Cara benar: reshape dulu
[nlon34, nlat34, nt] = size(sst_nino34);
sst_reshaped = reshape(sst_nino34, nlon34*nlat34, nt);
nino34_ts = mean(sst_reshaped, 1)';   % Transpos jadi kolom

% Buat vektor waktu
t_start = datetime(1982, 1, 1);
t_end   = datetime(2023, 12, 1);
time_vec = t_start:calmonths(1):t_end;

% Plot time series
figure
plot(time_vec, nino34_ts, 'k-', 'LineWidth', 1.5)
yline(0, '--', 'color', [0.5 0.5 0.5])
xlabel('Tahun')
ylabel('SST Anomali (°C)')
title('Indeks Nino3.4')
grid on"""):
    story.append(ln)

story.append(h2("1.5 Climatology dan Anomaly"))
story.append(body(
    "Dua konsep fundamental dalam analisis iklim adalah <b>climatology</b> (rata-rata iklim) "
    "dan <b>anomaly</b> (penyimpangan dari rata-rata). Ini adalah dasar dari hampir semua "
    "analisis iklim."))
for ln in code("""% ── Menghitung Climatology Bulanan ───────────────────────
% Asumsikan data berukuran [nlon x nlat x ntime]
% dengan ntime = jumlah bulan total (misal 492 = 41 tahun)

ntime = size(sst, 3);
nyears = ntime / 12;

% Reshape menjadi [nlon x nlat x 12 x nyears]
sst_4d = reshape(sst, size(sst,1), size(sst,2), 12, nyears);

% Climatology: rata-rata sepanjang dimensi tahun (ke-4)
sst_clim = mean(sst_4d, 4);  % Ukuran: [nlon x nlat x 12]

% ── Menghitung Anomali ────────────────────────────────────
% Ulangi climatology sebanyak nyears kali
sst_clim_rep = repmat(sst_clim, [1, 1, 1, nyears]);
% Reshape kembali ke 3D
sst_clim_3d = reshape(sst_clim_rep, size(sst));
% Hitung anomali
sst_anom = sst - sst_clim_3d;

% ── Verifikasi ────────────────────────────────────────────
fprintf('Range anomali: %.2f sampai %.2f C\\n', ...
    min(sst_anom(:)), max(sst_anom(:)))
fprintf('Mean anomali global: %.4f C (seharusnya mendekati 0)\\n', ...
    nanmean(sst_anom(:)))"""):
    story.append(ln)

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# MODUL 2
# ════════════════════════════════════════════════════════════════════════════
story.append(section_banner("MODUL 2 — CLIMATE DATA TOOLBOX", C_ORANGE))
story.append(sp(10))
story.append(h1("Modul 2: Climate Data Toolbox"))

story.append(h2("2.1 Apa itu Climate Data Toolbox?"))
story.append(body(
    "Climate Data Toolbox (CDT) adalah koleksi fungsi MATLAB yang dikembangkan oleh "
    "<b>Chad A. Greene</b> dari Jet Propulsion Laboratory (JPL), NASA. Greene adalah "
    "peneliti geosains yang juga dikenal sebagai kontributor aktif komunitas MATLAB."))
story.append(body(
    "CDT dirilis sebagai open-source dan tersedia gratis melalui GitHub dan MATLAB File Exchange. "
    "Toolbox ini berisi lebih dari 100 fungsi yang dirancang khusus untuk analisis dan "
    "visualisasi data iklim, cuaca, dan oseanografi."))
story.append(info_box("Mengapa CDT Luar Biasa?", [
    bullet("Fungsi yang intuitif dan terdokumentasi dengan sangat baik"),
    bullet("Terintegrasi dengan colormap cmocean yang dirancang untuk data saintifik"),
    bullet("Mendukung analisis trend, anomali, dan climatology secara efisien"),
    bullet("Fungsi grid seperti cdtarea dan regrid sangat berguna untuk data global"),
    bullet("Gratis dan open-source — berbeda dengan banyak toolbox MATLAB lainnya"),
    bullet("Dipercaya dan digunakan dalam publikasi jurnal internasional"),
]))

story.append(h2("2.2 Instalasi Climate Data Toolbox"))
for ln in code("""% Cara 1: Dari MATLAB Add-On Explorer (Cara Termudah)
% Home > Add-Ons > Get Add-Ons
% Cari "Climate Data Toolbox"
% Klik Install

% Cara 2: Dari GitHub
% git clone https://github.com/chadagreene/CDT.git
% Kemudian di MATLAB:
addpath(genpath('/path/to/CDT'))
savepath  % Simpan path agar permanen

% Verifikasi instalasi
cdt  % Akan menampilkan daftar fungsi CDT yang tersedia"""):
    story.append(ln)

story.append(h2("2.3 Fungsi-fungsi Penting CDT"))

functions_cdt = [
    ("imagescn", "Menampilkan gambar/peta dengan penanganan NaN yang benar. "
     "Alternatif imagesc yang lebih baik untuk data dengan nilai kosong."),
    ("cmocean", "Koleksi colormap perceptually-uniform untuk data saintifik. "
     "Termasuk colormap untuk SST, kedalaman laut, anomali, dan banyak lagi."),
    ("trend", "Menghitung trend linear pada data time series. Mendukung data "
     "3D sehingga bisa menghitung trend di setiap grid point sekaligus."),
    ("anomaly", "Menghitung anomali bulanan atau musiman secara otomatis. "
     "Menggantikan perhitungan manual climatology dan pengurangan."),
    ("climatology", "Menghitung rata-rata iklim untuk setiap bulan atau musim. "
     "Sangat berguna untuk membuat climatological mean dari data panjang."),
    ("cdtarea", "Menghitung luas area setiap sel grid dalam km persegi. "
     "Penting untuk rata-rata area-weighted yang akurat secara geografis."),
    ("regrid", "Menginterpolasi data dari satu grid ke grid lain. "
     "Berguna ketika menggabungkan dataset dengan resolusi berbeda."),
]

for fname, desc in functions_cdt:
    story.append(KeepTogether([
        bold(f"◆ {fname}"),
        body(desc),
        sp(3),
    ]))

story.append(sp(8))
story.append(body("Contoh penggunaan fungsi CDT:"))
for ln in code("""% ── cmocean ──────────────────────────────────────────────
figure
contourf(lon, lat, sst(:,:,1), 20, 'LineColor','none')
cmocean('thermal')   % Colormap termal yang bagus untuk SST
colorbar
title('SST dengan cmocean thermal')

% ── imagescn ─────────────────────────────────────────────
figure
imagescn(lon, lat, sst_anom(:,:,1)')  % NaN ditampilkan transparan
cmocean('balance', 'pivot', 0)        % Colormap diverging, pivot di 0
colorbar
title('SST Anomali dengan imagescn')

% ── trend ─────────────────────────────────────────────────
% Hitung trend SST di setiap grid point
% Input: data [nlon x nlat x ntime], time vector
[tr, p] = trend(sst, 1);  % trend per satuan waktu
% tr: ukuran [nlon x nlat]
% p: p-value untuk signifikansi statistik

% Tampilkan hanya trend yang signifikan (p < 0.05)
tr_sig = tr;
tr_sig(p > 0.05) = NaN;

% ── anomaly ──────────────────────────────────────────────
sst_anom = anomaly(sst, 'monthly');   % Anomali bulanan otomatis

% ── climatology ──────────────────────────────────────────
sst_clim = climatology(sst, time, 'monthly');  % Climatology bulanan"""):
    story.append(ln)

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# MODUL 3
# ════════════════════════════════════════════════════════════════════════════
story.append(section_banner("MODUL 3 — VISUALISASI DATA IKLIM", C_MID_BLUE))
story.append(sp(10))
story.append(h1("Modul 3: Visualisasi Data Iklim"))

story.append(h2("3.1 Plot SST Indonesia"))
for ln in code("""% Setup peta Indonesia
figure('Position', [100 100 1200 600])

% Plot SST
imagescn(lon_indo, lat_indo, sst_indo')
cmocean('thermal')
caxis([26 32])
colorbar('FontSize', 12)

% Tambahkan garis pantai
hold on
% borders('Indonesia', 'k', 'LineWidth', 1.5)  % dari CDT atau Mapping Toolbox
load coastlines
plot(coastlon, coastlat, 'k', 'LineWidth', 1)

% Formatting
xlabel('Longitude (°E)', 'FontSize', 12)
ylabel('Latitude (°N)', 'FontSize', 12)
title('SST Indonesia — Januari 2023', 'FontSize', 14, 'FontWeight', 'bold')
set(gca, 'XLim', [95 141], 'YLim', [-11 6])
set(gca, 'FontSize', 11)

% Export
exportgraphics(gcf, 'SST_Indonesia_Jan2023.png', 'Resolution', 300)"""):
    story.append(ln)

story.append(h2("3.2 Plot Curah Hujan"))
for ln in code("""% Curah Hujan dengan colormap yang tepat
figure
imagescn(lon, lat, precip(:,:,1)')
cmocean('rain')      % Colormap khusus curah hujan dari CDT
caxis([0 20])        % mm/hari
colorbar
title('Curah Hujan Harian (mm/hari)')

% Alternatif: contourf dengan lebih banyak kontrol
figure
levels = [1 2 5 10 15 20 30 50];
contourf(lon, lat, precip(:,:,1)', levels, 'LineColor', 'none')
cmocean('rain')
colorbar('Ticks', levels)"""):
    story.append(ln)

story.append(h2("3.3 Plot Angin dan Streamline"))
for ln in code("""% ── Quiver Plot (Panah Angin) ────────────────────────────
figure
% Subsample setiap 5 grid point agar tidak terlalu padat
step = 5;
lon_q = lon(1:step:end);
lat_q = lat(1:step:end);
u_q   = u850(1:step:end, 1:step:end);
v_q   = v850(1:step:end, 1:step:end);

quiver(lon_q, lat_q, u_q', v_q', 1.5, 'k')
title('Angin 850 hPa')
xlabel('Longitude'); ylabel('Latitude')
axis equal; grid on

% ── Streamline ────────────────────────────────────────────
figure
[meshlon, meshlat] = meshgrid(lon, lat);
streamslice(meshlon, meshlat, u850', v850', 2)
title('Streamline Angin 850 hPa')
xlabel('Longitude'); ylabel('Latitude')

% ── Wind Speed ────────────────────────────────────────────
ws = sqrt(u850.^2 + v850.^2);   % Kecepatan angin
figure
imagescn(lon, lat, ws')
cmocean('speed')
colorbar
hold on
quiver(lon_q, lat_q, u_q', v_q', 'w', 'AutoScaleFactor', 1.5)
title('Kecepatan dan Arah Angin 850 hPa')"""):
    story.append(ln)

story.append(h2("3.4 Peta Anomali dan Export Publikasi"))
for ln in code("""% ── Peta Anomali dengan Signifikansi ─────────────────────
figure('Position', [50 50 1000 500], 'Color', 'w')

% Plot anomali SST
imagescn(lon, lat, sst_anom(:,:,t0)')
cmocean('balance', 'pivot', 0)
caxis([-2 2])
cb = colorbar;
cb.Label.String = 'SST Anomali (°C)';
cb.FontSize = 11;

% Hatching untuk area tidak signifikan
hold on
h = pcolor(lon, lat, double(~sig_mask)');
h.FaceAlpha = 0.3;
h.EdgeColor = 'none';
h.FaceColor = [0.7 0.7 0.7];

% Garis pantai
load coastlines
plot(coastlon, coastlat, 'k', 'LineWidth', 0.8)

% Label dan formatting
xlabel('Longitude (°E)', 'FontSize', 12)
ylabel('Latitude (°N)', 'FontSize', 12)
title('SST Anomali — Desember 2023 (El Nino)', 'FontSize', 13)
set(gca, 'XLim', [30 180], 'YLim', [-30 30], 'FontSize', 11)

% ── Export Kualitas Publikasi ─────────────────────────────
% Format untuk jurnal (300 DPI, PDF vektor)
exportgraphics(gcf, 'fig1_sst_anomali.pdf', 'ContentType', 'vector')
exportgraphics(gcf, 'fig1_sst_anomali.png', 'Resolution', 300)
% Untuk EPS (beberapa jurnal masih minta ini)
print('-depsc', '-r300', 'fig1_sst_anomali.eps')"""):
    story.append(ln)

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# MODUL 4 & 5
# ════════════════════════════════════════════════════════════════════════════
story.append(section_banner("MODUL 4 — STUDI KASUS ERA5", C_DARK_BLUE))
story.append(sp(10))
story.append(h1("Modul 4: Studi Kasus ERA5"))
story.append(body(
    "ERA5 adalah reanalisis atmosfer global terbaru dari ECMWF (European Centre for "
    "Medium-Range Weather Forecasts). Dengan resolusi 0.25° dan data dari 1940 hingga kini, "
    "ERA5 adalah dataset yang paling banyak digunakan dalam penelitian iklim modern."))

story.append(h2("4.1 Download ERA5"))
story.append(body(
    "ERA5 tersedia gratis melalui Copernicus Climate Data Store (CDS). Anda membutuhkan akun "
    "di cds.climate.copernicus.eu dan menginstal cdsapi (Python) atau menggunakan web interface."))
story.append(info_box("Variabel ERA5 yang Sering Digunakan", [
    bullet("2m temperature (t2m) — suhu udara 2 meter dari permukaan"),
    bullet("Sea Surface Temperature (sst) — suhu permukaan laut"),
    bullet("Total Precipitation (tp) — curah hujan total"),
    bullet("10m U/V wind components (u10, v10) — angin permukaan"),
    bullet("Mean sea level pressure (msl) — tekanan muka laut"),
    bullet("Specific humidity (q) — kelembaban spesifik"),
]))

story.append(h2("4.2–4.5 Membaca, Climatology, Anomali, dan Trend ERA5"))
for ln in code("""% ── 4.2 Membaca ERA5 ─────────────────────────────────────
fname = 'ERA5_SST_monthly_1982_2023.nc';
lon  = ncread(fname, 'longitude');   % 0 sampai 360 atau -180 sampai 180
lat  = ncread(fname, 'latitude');    % 90 sampai -90 (perhatikan urutan!)
time = ncread(fname, 'time');        % Jam sejak epoch
sst  = ncread(fname, 'sst');
sst  = sst - 273.15;   % Konversi dari Kelvin ke Celsius

% Konversi waktu ERA5 ke datetime MATLAB
time_dt = datetime(1900,1,1) + hours(time);
fprintf('Data dari: %s sampai %s\\n', datestr(time_dt(1)), datestr(time_dt(end)))

% ── 4.3 Climatology Bulanan ERA5 ─────────────────────────
ntime = length(time_dt);
nyears = ntime / 12;
sst_4d = reshape(sst, size(sst,1), size(sst,2), 12, nyears);
sst_clim = mean(sst_4d, 4, 'omitnan');   % Klimatologi bulanan [lon x lat x 12]

% Plot klimatologi DJF
djf = mean(sst_clim(:,:,[12 1 2]), 3);    % Desember-Januari-Februari
figure
imagescn(lon, lat, djf')
cmocean('thermal'); caxis([0 30]); colorbar
title('SST Klimatologi DJF (ERA5 1982-2023)')

% ── 4.4 Anomali ERA5 ─────────────────────────────────────
sst_clim_rep = repmat(sst_clim, [1, 1, 1, nyears]);
sst_clim_3d  = reshape(sst_clim_rep, size(sst));
sst_anom = sst - sst_clim_3d;

% ── 4.5 Trend Linear ERA5 ─────────────────────────────────
% Menggunakan fungsi trend dari CDT
[tr, ~, p] = trend(sst, 12);   % trend per tahun (x12 karena data bulanan)
% Satuan: °C/tahun

figure
imagescn(lon, lat, tr')
cmocean('balance', 'pivot', 0)
caxis([-0.05 0.05])
colorbar('Label', '°C/tahun')
title('Trend SST ERA5 (1982-2023, °C/tahun)')

% Mask area tidak signifikan
tr_masked = tr;
tr_masked(p > 0.05) = NaN;
figure
imagescn(lon, lat, tr_masked')
cmocean('balance', 'pivot', 0)
title('Trend SST Signifikan (p < 0.05)')"""):
    story.append(ln)

story.append(PageBreak())

# MODUL 5
story.append(section_banner("MODUL 5 — STUDI KASUS OISST", C_TEAL))
story.append(sp(10))
story.append(h1("Modul 5: Studi Kasus OISST"))
story.append(body(
    "NOAA OISST (Optimum Interpolation Sea Surface Temperature) adalah dataset SST harian "
    "dengan resolusi 0.25°, tersedia dari September 1981 hingga sekarang. Dataset ini "
    "sangat populer untuk analisis variabilitas SST, terutama untuk studi ENSO dan "
    "Marine Heatwave karena resolusi temporalnya yang tinggi."))

story.append(h2("5.1–5.4 OISST: Dari Pembacaan hingga ENSO"))
for ln in code("""% ── 5.1 Membaca OISST ────────────────────────────────────
% OISST tersedia sebagai file netCDF harian atau bulanan
% Download dari: https://www.ncei.noaa.gov/products/optimum-interpolation-sst

fname_oisst = 'sst.mnmean.nc';
lon_oi = ncread(fname_oisst, 'lon');   % 0.125 sampai 359.875, step 0.25
lat_oi = ncread(fname_oisst, 'lat');   % -89.875 sampai 89.875
time_oi = ncread(fname_oisst, 'time'); % Hari sejak 1800-01-01
sst_oi  = ncread(fname_oisst, 'sst');  % °C, sudah dalam Celsius
% Nilai fill: sst > 35 atau < -5 biasanya adalah land/ice mask
sst_oi(sst_oi > 35) = NaN;

time_oi_dt = datetime(1800,1,1) + days(time_oi);

% ── 5.2 SST Climatology (1991-2020) ──────────────────────
% Pilih periode referensi WMO 1991-2020
i_ref = time_oi_dt.Year >= 1991 & time_oi_dt.Year <= 2020;
sst_ref = sst_oi(:,:, i_ref);
nref = sum(i_ref);  % = 360 bulan

sst_ref_4d = reshape(sst_ref, size(sst_ref,1), size(sst_ref,2), 12, nref/12);
sst_clim_oi = mean(sst_ref_4d, 4, 'omitnan');

% ── 5.3 SST Anomaly (SSTA) ───────────────────────────────
ntime_oi = size(sst_oi, 3);
nyears_oi = floor(ntime_oi / 12);
months_all = repmat(1:12, 1, nyears_oi);

sst_anom_oi = nan(size(sst_oi));
for m = 1:12
    idx = (months_all == m);
    sst_anom_oi(:,:,idx) = bsxfun(@minus, sst_oi(:,:,idx), sst_clim_oi(:,:,m));
end

% ── 5.4 ENSO Monitoring (Nino3.4 Index) ──────────────────
% Wilayah Nino3.4: 190-240°E, 5°S-5°N
i_lon34 = find(lon_oi >= 190 & lon_oi <= 240);
i_lat34 = find(lat_oi >= -5 & lat_oi <= 5);

sst_n34 = sst_anom_oi(i_lon34, i_lat34, :);
[nl, nlt, nt] = size(sst_n34);
nino34 = squeeze(mean(reshape(sst_n34, nl*nlt, 1, nt), 1));

% Plot dengan shading El Nino / La Nina
figure('Position', [50 50 1200 400])
area(time_oi_dt, max(nino34, 0), 'FaceColor', [0.8 0.2 0.2], 'FaceAlpha', 0.6)
hold on
area(time_oi_dt, min(nino34, 0), 'FaceColor', [0.2 0.4 0.8], 'FaceAlpha', 0.6)
plot(time_oi_dt, nino34, 'k', 'LineWidth', 1)
yline(0.5, '--r'); yline(-0.5, '--b')
xlabel('Tahun'); ylabel('SST Anomali (°C)')
title('Indeks Nino3.4 (OISST) — ENSO Monitor')
legend('El Nino', 'La Nina'); grid on"""):
    story.append(ln)

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# MODUL 6
# ════════════════════════════════════════════════════════════════════════════
story.append(section_banner("MODUL 6 — MARINE HEATWAVE", C_RED))
story.append(sp(10))
story.append(h1("Modul 6: Marine Heatwave"))

story.append(h2("6.1 Konsep Marine Heatwave"))
story.append(body(
    "Marine Heatwave (MHW) adalah periode berkepanjangan di mana suhu permukaan laut "
    "berada di atas threshold tertentu. Definisi formal menurut Hobday et al. (2016) adalah: "
    "<b>periode di mana SST harian melebihi persentil ke-90 selama minimal 5 hari berturut-turut</b>, "
    "dengan dua event yang terpisah kurang dari 2 hari dianggap sebagai satu event."))
story.append(body(
    "MHW memiliki dampak besar pada ekosistem laut, termasuk pemutihan terumbu karang, "
    "kematian massal organisme laut, dan gangguan rantai makanan. Indonesia, dengan "
    "terumbu karang terkaya di dunia, sangat rentan terhadap MHW."))
story.append(info_box("Definisi Resmi Marine Heatwave (Hobday et al., 2016)", [
    bullet("SST harian > Persentil ke-90 dari baseline (biasanya 1982-2011 atau 1991-2020)"),
    bullet("Durasi minimal: 5 hari berturut-turut"),
    bullet("Gap < 2 hari antara dua event = digabung menjadi satu event"),
    bullet("Intensitas diukur sebagai selisih SST dari threshold pada setiap hari event"),
]))

story.append(h2("6.2–6.7 Deteksi dan Analisis MHW"))
for ln in code("""% ── 6.2 Hitung Persentil ke-90 ───────────────────────────
% Untuk satu titik grid (misal lon=115E, lat=8S)
i_lon_pt = find(lon_oi >= 115, 1);
i_lat_pt = find(lat_oi >= -8, 1);

sst_pt = squeeze(sst_oi(i_lon_pt, i_lat_pt, :));   % Time series 1D

% Hitung persentil ke-90 menggunakan baseline 1982-2011
i_base = year(time_oi_dt) >= 1982 & year(time_oi_dt) <= 2011;
sst_base = sst_pt(i_base);

% ── 6.3 Threshold Persentil 90 ───────────────────────────
% Penting: hitung persentil per hari-of-year (bukan global)
% untuk menangkap siklus musiman
doy = day(time_oi_dt, 'dayofyear');
threshold = nan(365, 1);
window = 11;   % ±11 hari window

for d = 1:365
    % Kumpulkan hari dalam window dari baseline
    win_days = mod((d-window-1):(d+window-1), 365) + 1;
    idx_win = ismember(doy(i_base), win_days);
    threshold(d) = prctile(sst_base(idx_win), 90);
end

% Haluskan threshold dengan moving average
threshold_smooth = movmean(threshold, 31, 'Endpoints', 'fill');

% ── 6.4 Deteksi Event MHW ────────────────────────────────
% Bangun threshold time series lengkap
thresh_ts = threshold_smooth(doy);    % Sesuaikan ke time series panjang
exceed = sst_pt > thresh_ts;          % Logical: hari mana yang exceeded?

% Cari event: minimal 5 hari berturut-turut
min_dur = 5;
max_gap = 2;
events = struct('start', {}, 'end', {}, 'duration', {}, ...
                'intensity_mean', {}, 'intensity_max', {});

in_event = false;
gap_count = 0;
e_start = 0;

for t = 1:length(exceed)
    if exceed(t)
        if ~in_event
            e_start = t;
            in_event = true;
        end
        gap_count = 0;
    else
        if in_event
            gap_count = gap_count + 1;
            if gap_count > max_gap
                dur = t - e_start - gap_count;
                if dur >= min_dur
                    n = length(events) + 1;
                    events(n).start = time_oi_dt(e_start);
                    events(n).end   = time_oi_dt(t-gap_count-1);
                    events(n).duration = dur;
                    anom_e = sst_pt(e_start:t-gap_count-1) - thresh_ts(e_start:t-gap_count-1);
                    events(n).intensity_mean = mean(anom_e(anom_e>0));
                    events(n).intensity_max  = max(anom_e);
                end
                in_event = false;
                gap_count = 0;
            end
        end
    end
end

fprintf('Jumlah MHW terdeteksi: %d event\\n', length(events))

% ── 6.5–6.6 Durasi dan Intensitas ────────────────────────
dur_all = [events.duration];
int_all = [events.intensity_mean];
fprintf('Durasi rata-rata: %.1f hari\\n', mean(dur_all))
fprintf('Intensitas rata-rata: %.2f C\\n', mean(int_all))
fprintf('Event terpanjang: %d hari\\n', max(dur_all))
fprintf('Intensitas maksimum: %.2f C\\n', max(int_all))

% Plot distribusi
figure
histogram(dur_all, 'BinWidth', 5, 'FaceColor', '#E74C3C')
xlabel('Durasi (hari)'); ylabel('Jumlah Event')
title('Distribusi Durasi Marine Heatwave')"""):
    story.append(ln)

story.append(PageBreak())

# MODUL 7
story.append(section_banner("MODUL 7 — TROPICAL CYCLONE", HexColor("#4A148C")))
story.append(sp(10))
story.append(h1("Modul 7: Tropical Cyclone"))

story.append(h2("7.1 IBTrACS — Database Siklon Tropis Global"))
story.append(body(
    "IBTrACS (International Best Track Archive for Climate Stewardship) adalah database "
    "resmi WMO yang mengkompilasi data jalur siklon tropis dari seluruh dunia sejak 1842. "
    "Data tersedia dalam format NetCDF dan CSV dari ncei.noaa.gov/products/international-best-track-archive."))

for ln in code("""% ── 7.1 Membaca IBTrACS ──────────────────────────────────
fname_tc = 'IBTrACS.WP.v04r00.nc';   % Wilayah Western Pacific

% Variabel utama
lon_tc  = ncread(fname_tc, 'lon');       % [storm x time]
lat_tc  = ncread(fname_tc, 'lat');
wind_tc = ncread(fname_tc, 'wmo_wind'); % Kecepatan angin maksimum (knot)
pres_tc = ncread(fname_tc, 'wmo_pres'); % Tekanan minimum (hPa)
year_tc = ncread(fname_tc, 'season');   % Tahun
name_tc = ncread(fname_tc, 'name');     % Nama siklon

fprintf('Jumlah total storm: %d\\n', size(lon_tc, 1))

% ── 7.2 Plot Track Siklon ─────────────────────────────────
% Filter: hanya tahun 2000-2023, wilayah Indonesia (95-141E, 30S-20N)
years = squeeze(year_tc);
i_storms = find(years >= 2000 & years <= 2023);

figure('Position', [50 50 1200 700])
hold on

for i = i_storms'
    lo = lon_tc(i, :);
    la = lat_tc(i, :);
    ws = wind_tc(i, :);
    
    valid = ~isnan(lo) & ~isnan(la);
    if sum(valid) < 2; continue; end
    
    % Warna berdasarkan intensitas
    max_ws = nanmax(ws);
    if max_ws >= 130
        clr = [0.6 0 0];        % Super typhoon: merah tua
    elseif max_ws >= 96
        clr = [0.9 0.2 0.2];    % Typhoon: merah
    elseif max_ws >= 64
        clr = [1 0.6 0];        % Severe TS: oranye
    else
        clr = [0.3 0.5 1];      % TS: biru
    end
    
    plot(lo(valid), la(valid), '-', 'Color', clr, 'LineWidth', 0.8)
end

load coastlines
plot(coastlon, coastlat, 'k', 'LineWidth', 0.5)
xlabel('Longitude'); ylabel('Latitude')
title('Track Siklon Tropis Western Pacific 2000-2023')
xlim([90 180]); ylim([-15 35])
grid on"""):
    story.append(ln)

story.append(h2("7.3 Density Map Siklon"))
for ln in code("""% Density map menggunakan histogram 2D
res = 2;   % Resolusi 2 derajat
lon_bins = 90:res:180;
lat_bins = -15:res:35;

density = zeros(length(lon_bins)-1, length(lat_bins)-1);

for i = i_storms'
    lo = lon_tc(i, :);
    la = lat_tc(i, :);
    valid = ~isnan(lo) & ~isnan(la);
    
    for t = find(valid)
        [~, il] = histc(lo(t), lon_bins);
        [~, ila] = histc(la(t), lat_bins);
        if il > 0 && ila > 0
            density(il, ila) = density(il, ila) + 1;
        end
    end
end

% Normalisasi ke track density per tahun per degree^2
density_norm = density / (2023-2000+1) / res^2;

figure
imagescn(lon_bins(1:end-1)+res/2, lat_bins(1:end-1)+res/2, density_norm')
cmocean('matter')
colorbar('Label', 'Track density (per tahun per deg^2)')
title('Track Density Siklon Tropis (2000-2023)')"""):
    story.append(ln)

story.append(PageBreak())

# MODUL 8
story.append(section_banner("MODUL 8 — PROYEK NYATA", C_TEAL))
story.append(sp(10))
story.append(h1("Modul 8: Proyek Nyata"))
story.append(body(
    "Modul terakhir ini mengintegrasikan semua yang telah dipelajari ke dalam proyek-proyek "
    "nyata yang relevan untuk penelitian dan operasional di Indonesia."))

story.append(h2("8.1 Monitoring ENSO"))
for ln in code("""%% ENSO_Monitor.m — Script Monitoring ENSO Komprehensif
% ─────────────────────────────────────────────────────────
% Langkah 1: Load data OISST
fname = 'sst.mnmean.nc';
lon  = ncread(fname, 'lon');
lat  = ncread(fname, 'lat');
time = ncread(fname, 'time');
sst  = ncread(fname, 'sst');
time_dt = datetime(1800,1,1) + days(time);

% Langkah 2: Hitung Nino3.4
i_lon = find(lon >= 190 & lon <= 240);
i_lat = find(lat >= -5 & lat <= 5);

sst_n34 = sst(i_lon, i_lat, :);
nino34_raw = squeeze(mean(reshape(sst_n34, [], size(sst_n34,3)), 1));

% Baseline 1991-2020
i_base = year(time_dt) >= 1991 & year(time_dt) <= 2020;
clim_monthly = nan(12, 1);
for m = 1:12
    idx = i_base & month(time_dt) == m;
    clim_monthly(m) = mean(nino34_raw(idx));
end
clim_full = clim_monthly(month(time_dt));
nino34 = nino34_raw - clim_full;

% 3-month running mean
nino34_3m = movmean(nino34, 3);

% Kategori ENSO
el_nino  = nino34_3m >= 0.5;
la_nina  = nino34_3m <= -0.5;
neutral  = ~el_nino & ~la_nina;

% Dashboard plot
figure('Position', [50 50 1400 500], 'Color', 'w')
area(time_dt, max(nino34_3m, 0), 'FaceColor', '#C62828', 'FaceAlpha', 0.7)
hold on
area(time_dt, min(nino34_3m, 0), 'FaceColor', '#1565C0', 'FaceAlpha', 0.7)
plot(time_dt, nino34_3m, 'k', 'LineWidth', 1.2)
yline(0.5, '--', 'El Nino', 'Color', '#C62828', 'FontSize', 10)
yline(-0.5, '--', 'La Nina', 'Color', '#1565C0', 'FontSize', 10)
yline(0, 'k-', 'LineWidth', 0.5)
xlabel('Tahun', 'FontSize', 12)
ylabel('Indeks Nino3.4 (°C)', 'FontSize', 12)
title('ENSO Monitor — Indeks Nino3.4 (3-bulan running mean)', 'FontSize', 14)
set(gca, 'FontSize', 11)
grid on; box on"""):
    story.append(ln)

story.append(h2("8.2 Monitoring IOD"))
for ln in code("""%% IOD_Monitor.m — Indian Ocean Dipole
% IOD = SST anomali Samudera Hindia Barat (WIO) minus Timur (EIO)
% Dipole Mode Index (DMI) = SSTA_WIO - SSTA_EIO

% Wilayah WIO: 50-70E, 10S-10N
% Wilayah EIO: 90-110E, 10S-0N

i_wio_lo = find(lon >= 50 & lon <= 70);
i_wio_la = find(lat >= -10 & lat <= 10);
i_eio_lo = find(lon >= 90 & lon <= 110);
i_eio_la = find(lat >= -10 & lat <= 0);

sst_wio = sst(i_wio_lo, i_wio_la, :);
sst_eio = sst(i_eio_lo, i_eio_la, :);

[nw1, nw2, nt] = size(sst_wio);
[ne1, ne2, ~]  = size(sst_eio);

wio_ts = squeeze(mean(reshape(sst_wio, nw1*nw2, nt), 1))';
eio_ts = squeeze(mean(reshape(sst_eio, ne1*ne2, nt), 1))';

% Hitung anomali dari baseline
wio_anom = detrend(wio_ts - mean(wio_ts(i_base)));
eio_anom = detrend(eio_ts - mean(eio_ts(i_base)));

% DMI = WIO - EIO
dmi = wio_anom - eio_anom;
dmi_3m = movmean(dmi, 3);

% Plot
figure('Position', [50 50 1400 450], 'Color', 'w')
area(time_dt, max(dmi_3m, 0), 'FaceColor', '#E65100', 'FaceAlpha', 0.7)
hold on
area(time_dt, min(dmi_3m, 0), 'FaceColor', '#1A237E', 'FaceAlpha', 0.7)
yline(0.4, '--r'); yline(-0.4, '--b')
xlabel('Tahun'); ylabel('DMI (°C)')
title('IOD Monitor — Dipole Mode Index')
grid on"""):
    story.append(ln)

story.append(h2("8.4 Analisis Marine Heatwave Indonesia"))
for ln in code("""%% MHW_Indonesia.m — Peta Frekuensi MHW Perairan Indonesia
% ─────────────────────────────────────────────────────────
% Hitung frekuensi MHW per grid point untuk seluruh Indonesia

% Subset Indonesia
i_lo = find(lon >= 95 & lon <= 141);
i_la = find(lat >= -15 & lat <= 10);

lon_id = lon(i_lo);
lat_id = lat(i_la);
sst_id = sst(i_lo, i_la, :);

[nlo, nla, nt] = size(sst_id);
mhw_freq = nan(nlo, nla);    % Frekuensi event per tahun
mhw_dur  = nan(nlo, nla);    % Durasi rata-rata (hari)

fprintf('Menghitung MHW untuk %d x %d grid points...\\n', nlo, nla)

for il = 1:nlo
    for ila = 1:nla
        sst_pt = squeeze(sst_id(il, ila, :));
        if all(isnan(sst_pt)); continue; end
        
        % Hitung threshold persentil 90
        thresh = prctile(sst_pt(i_base), 90);
        
        % Deteksi event sederhana
        exceed = sst_pt > thresh;
        events = bwconncomp(exceed);  % Image processing toolbox
        
        durations = cellfun(@length, events.PixelIdxList);
        valid_ev  = durations >= 5;
        
        n_years = (time_dt(end) - time_dt(1)).Days / 365.25;
        mhw_freq(il, ila) = sum(valid_ev) / n_years;
        if any(valid_ev)
            mhw_dur(il, ila) = mean(durations(valid_ev));
        end
    end
end

% Plot frekuensi MHW
figure('Position', [50 50 1200 600])
imagescn(lon_id, lat_id, mhw_freq')
cmocean('matter')
caxis([0 3])
cb = colorbar;
cb.Label.String = 'Frekuensi MHW (event/tahun)';
hold on
load coastlines
plot(coastlon, coastlat, 'k', 'LineWidth', 0.8)
set(gca, 'XLim', [95 141], 'YLim', [-15 10])
xlabel('Longitude (°E)'); ylabel('Latitude (°N)')
title('Frekuensi Marine Heatwave Perairan Indonesia (1982-2023)')"""):
    story.append(ln)

story.append(h2("8.5 Dari Analisis ke Paper Publikasi"))
story.append(body(
    "Setelah menghasilkan analisis dan visualisasi yang baik, langkah berikutnya adalah "
    "menulis paper ilmiah. Berikut panduan singkat untuk mempersiapkan output MATLAB "
    "untuk publikasi:"))

pub_tips = [
    ("Kualitas Gambar", 
     "Export semua figure dengan resolusi minimal 300 DPI untuk jurnal. "
     "Gunakan format PDF atau EPS untuk gambar vektor. "
     "Command: exportgraphics(gcf, 'fig1.pdf', 'ContentType', 'vector')"),
    ("Konsistensi Warna",
     "Gunakan colormap yang sama untuk variabel yang sama di semua figure. "
     "Hindari colormap 'jet' — gunakan cmocean yang perceptually uniform. "
     "Pastikan gambar bisa dibaca oleh orang dengan color blindness."),
    ("Caption dan Label",
     "Semua sumbu harus berlabel dengan satuan. Semua gambar harus memiliki caption "
     "yang lengkap. Ukuran font minimal 10pt untuk teks dalam gambar."),
    ("Reprodusibilitas",
     "Simpan semua script yang menghasilkan setiap figure. Beri komentar yang jelas "
     "pada setiap bagian kode. Upload data dan kode ke Zenodo atau GitHub "
     "saat paper terbit untuk open science."),
    ("Statistik",
     "Selalu tampilkan signifikansi statistik (p-value) untuk trend dan korelasi. "
     "Gunakan bootstrap atau Monte Carlo untuk confidence interval jika diperlukan. "
     "Nyatakan periode baseline yang digunakan untuk anomali dan climatology."),
]
for title, desc in pub_tips:
    story.append(KeepTogether([
        bold(f"◆ {title}"),
        body(desc),
        sp(5),
    ]))

story.append(sp(8))
for ln in code("""% Template Script untuk Figure Kualitas Jurnal
function export_fig_journal(fig_handle, filename, fig_title)
    % Set font size konsisten
    set(findall(fig_handle, 'Type', 'axes'), 'FontSize', 11, ...
        'FontName', 'Helvetica')
    set(findall(fig_handle, 'Type', 'text'), 'FontSize', 11)
    
    % Set ukuran figure (misal untuk double column: 19cm x 9cm)
    fig_handle.Units = 'centimeters';
    fig_handle.Position = [1 1 19 9];
    
    % Export PDF vektor
    exportgraphics(fig_handle, [filename '.pdf'], ...
        'ContentType', 'vector', 'BackgroundColor', 'white')
    
    % Export PNG 300 DPI
    exportgraphics(fig_handle, [filename '.png'], 'Resolution', 300)
    
    fprintf('Figure "%s" berhasil disimpan!\\n', fig_title)
end"""):
    story.append(ln)

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# PENUTUP
# ════════════════════════════════════════════════════════════════════════════
story.append(section_banner("PENUTUP DAN REFERENSI", C_DARK_BLUE))
story.append(sp(10))
story.append(h1("Penutup"))
story.append(body(
    "Selamat! Anda telah menyelesaikan seluruh kurikulum Seri Belajar MATLAB untuk "
    "Sains Atmosfer dan Kelautan. Dari memahami antarmuka MATLAB di Modul 0, hingga "
    "menganalisis Marine Heatwave dan mempersiapkan paper publikasi di Modul 8, "
    "perjalanan ini mencakup keterampilan yang diperlukan oleh seorang peneliti "
    "iklim dan oseanografi modern."))
story.append(body(
    "Ingat bahwa pemrograman adalah keterampilan yang diasah melalui praktik. "
    "Jangan takut untuk mencoba, membuat kesalahan, dan mencari solusi. "
    "Komunitas MATLAB dan ilmu iklim Indonesia terus berkembang, dan kontribusi "
    "Anda sangat berharga."))

story.append(h2("Referensi Utama"))
refs = [
    "Greene, C.A., et al. (2019). The Climate Data Toolbox for MATLAB. "
     "Geochemistry, Geophysics, Geosystems, 20(7), 3774-3781.",
    "Hobday, A.J., et al. (2016). A hierarchical approach to defining marine heatwaves. "
     "Progress in Oceanography, 141, 227-238.",
    "Rayner, N.A., et al. (2003). Global analyses of sea surface temperature, sea ice, "
     "and night marine air temperature since the late nineteenth century. "
     "Journal of Geophysical Research, 108(D14), 4407.",
    "Hersbach, H., et al. (2020). The ERA5 global reanalysis. "
     "Quarterly Journal of the Royal Meteorological Society, 146(730), 1999-2049.",
    "Knapp, K.R., et al. (2010). The International Best Track Archive for Climate Stewardship "
     "(IBTrACS). Bulletin of the American Meteorological Society, 91(3), 363-376.",
    "MathWorks (2024). MATLAB Documentation. https://www.mathworks.com/help/matlab/",
    "Huang, B., et al. (2017). NOAA Optimum Interpolation (OI) SST V2 High Resolution Dataset. "
     "NOAA National Centers for Environmental Information.",
]
for i, ref in enumerate(refs, 1):
    story.append(Paragraph(f"[{i}] {ref}", 
        ParagraphStyle("Ref", fontName="Helvetica", fontSize=9.5, textColor=C_TEXT,
                       leading=14, leftIndent=20, firstLineIndent=-20, spaceAfter=5)))

story.append(sp(10))
story.append(h2("Sumber Belajar Tambahan"))
story.append(bullet("MATLAB Official Documentation: mathworks.com/help/matlab/"))
story.append(bullet("Climate Data Toolbox: github.com/chadagreene/CDT"))
story.append(bullet("cmocean colormap: matplotlib.org/cmocean/"))
story.append(bullet("ERA5: cds.climate.copernicus.eu"))
story.append(bullet("OISST: ncei.noaa.gov/products/optimum-interpolation-sst"))
story.append(bullet("IBTrACS: ncei.noaa.gov/products/international-best-track-archive"))
story.append(bullet("Copernicus Climate Change Service: climate.copernicus.eu"))

story.append(sp(10))
story.append(hr(C_ACCENT, 2))
story.append(sp(6))
story.append(Paragraph(
    "Seri Belajar MATLAB untuk Klimatologi dan Oseanografi<br/>"
    "Edisi Pertama — 2025<br/>"
    "Dikembangkan untuk komunitas sains atmosfer dan kelautan Indonesia",
    ParagraphStyle("Footer", fontName="Helvetica-Oblique", fontSize=9.5,
                   textColor=C_SUBTEXT, leading=16, alignment=TA_CENTER)))

# ─── BUILD ────────────────────────────────────────────────────────────────
doc.title = "Modul 0"
doc.build(story, onFirstPage=cover_page_template, onLaterPages=header_footer)
print(f"PDF berhasil dibuat: {OUTPUT}")
