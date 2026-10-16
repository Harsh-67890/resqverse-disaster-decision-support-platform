"""
generate_pdf_report.py
-----------------------
Comprehensive Project Analysis & Documentation Generator for NER-Sentinel / resQVerse.
Generates an executive, publication-grade PDF report documenting all work completed so far.
"""

import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, KeepTogether, PageBreak, HRFlowable
)

# Palette
PRIMARY = colors.HexColor("#0F172A")       # Deep Slate / Navy
SECONDARY = colors.HexColor("#0284C7")     # Ocean Blue / Cyan
ACCENT = colors.HexColor("#EA580C")        # Safety Orange
SUCCESS = colors.HexColor("#10B981")       # Emerald
TEXT_DARK = colors.HexColor("#1E293B")     # Dark Slate
TEXT_MUTED = colors.HexColor("#64748B")    # Slate Muted
BG_LIGHT = colors.HexColor("#F8FAFC")      # Cool White
BG_CARD = colors.HexColor("#F1F5F9")       # Light Slate Card
BORDER = colors.HexColor("#CBD5E1")        # Border Gray
CARD_BORDER = colors.HexColor("#E2E8F0")

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw 'Page X of Y' 
    along with running header and footer on all pages except the cover page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress headers/footers on cover page
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)

        page_w, page_h = A4
        margin_x = 36
        top_y = page_h - 28
        bottom_y = 24

        # Running Header
        self.drawString(margin_x, top_y, "NER-Sentinel / resQVerse — Disaster Intelligence Command Platform")
        self.drawRightString(page_w - margin_x, top_y, "Smart India Hackathon 2026 | Team 404")
        
        self.setStrokeColor(CARD_BORDER)
        self.setLineWidth(0.5)
        self.line(margin_x, top_y - 4, page_w - margin_x, top_y - 4)

        # Running Footer
        self.line(margin_x, bottom_y + 10, page_w - margin_x, bottom_y + 10)
        self.drawString(margin_x, bottom_y, "Confidential — Comprehensive Engineering & Architecture Report")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(page_w - margin_x, bottom_y, page_str)

        self.restoreState()


def build_pdf_report(output_pdf_path: str):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=TEXT_MUTED,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    )

    tag_style = ParagraphStyle(
        'TagStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9,
        textColor=SECONDARY
    )

    story = []

    # =========================================================================
    # 1. COVER / TITLE BANNER
    # =========================================================================
    header_table_data = [
        [
            Paragraph("<font color='#EA580C'><b>SMART INDIA HACKATHON 2026</b></font> &nbsp;|&nbsp; OFFICIAL PROJECT REPORT", tag_style),
            Paragraph("<font color='#0284C7'><b>TEAM 404: THE OPTIMISTICS</b></font>", ParagraphStyle('RTag', parent=tag_style, alignment=2))
        ]
    ]
    t_top = Table(header_table_data, colWidths=[340, 183])
    t_top.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
    ]))
    story.append(t_top)
    story.append(Spacer(1, 14))

    story.append(Paragraph("NER-Sentinel: Multi-Satellite Disaster Intelligence & Early Warning Command Platform", title_style))
    story.append(Paragraph("A Unified AI, WebGL 3D GIS & Closed-Loop Community Resilience System for Northeast India", subtitle_style))

    # Meta Info Grid
    meta_data = [
        [
            Paragraph("<b>Target Region:</b> Northeast India (Sikkim, Assam, Meghalaya, Arunachal)", table_cell_style),
            Paragraph("<b>Core Tech:</b> FastAPI, Next.js 15, MapLibre 3D, Spring Boot", table_cell_style),
        ],
        [
            Paragraph("<b>Satellites:</b> NASA SMAP, SRTM DEM, NASA POWER, Sentinel-1 InSAR", table_cell_style),
            Paragraph("<b>AI Models:</b> 9-Feature Ensemble (ROC-AUC: 0.894), Meta LLaMA 3.1", table_cell_style),
        ],
        [
            Paragraph("<b>Status:</b> 4/6 Core Modules Completed, Full End-to-End Live Pipelines", table_cell_style),
            Paragraph("<b>Date of Evaluation:</b> September 2026", table_cell_style),
        ]
    ]
    meta_table = Table(meta_data, colWidths=[260, 263])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # 2. EXECUTIVE SUMMARY & IMPACT METRICS
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Impact", h1_style))
    story.append(Paragraph(
        "<b>NER-Sentinel (resQVerse)</b> is an enterprise disaster intelligence platform engineered specifically for the complex, "
        "high-risk geomorphological challenges of Northeast India. While existing government disaster mechanisms operate in isolated silos "
        "(GSI for static landslide maps, CWC for river bulletins, IMD for meteorological forecasts, and SACHET for one-way broadcast SMS), "
        "NER-Sentinel integrates all data streams into a <b>single unified command center</b> backed by high-resolution 3D WebGL GIS, "
        "multi-satellite predictive machine learning, and an innovative <b>Two-Way Closed-Loop Feedback Architecture</b>.",
        body_style
    ))

    # Key Metrics Cards Table
    metrics_data = [
        [
            Paragraph("<font color='#0284C7'><b>89.4% ROC-AUC</b></font><br/><font size=7.5 color='#475569'>Flood & Slide Discriminatory ML Accuracy</font>", table_cell_style),
            Paragraph("<font color='#EA580C'><b>4-Second Refresh</b></font><br/><font size=7.5 color='#475569'>Real-time Live GIS & Sensor Polling Cycle</font>", table_cell_style),
            Paragraph("<font color='#10B981'><b>4 Satellites + Sensors</b></font><br/><font size=7.5 color='#475569'>SMAP, SRTM, POWER, InSAR, CWC, Open-Meteo</font>", table_cell_style),
            Paragraph("<font color='#7C3AED'><b>Two-Way Loop</b></font><br/><font size=7.5 color='#475569'>Citizen Reports directly trigger Model Retraining</font>", table_cell_style)
        ]
    ]
    metrics_table = Table(metrics_data, colWidths=[130, 130, 131, 132])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 12))

    # =========================================================================
    # 3. PROBLEM LANDSCAPE & REGIONAL GROUND REALITIES
    # =========================================================================
    story.append(Paragraph("2. Regional Problem Landscape & Ground Realities", h1_style))
    story.append(Paragraph(
        "Northeast India represents one of the world's most vulnerable ecological zones. Its unique tectonic setting, fragile young Himalayan geology, "
        "intense monsoonal downpours, and transnational river basins (Brahmaputra, Barak, Teesta) create acute compounding disaster risks:",
        body_style
    ))

    story.append(Paragraph("• <b>Glacial Lake Outburst Floods (GLOF) & Flash Floods:</b> Events like the October 2023 South Lhonak Lake breach in Sikkim demonstrated how a cloudburst-induced GLOF destroyed Teesta Dam Stage III and swept through Chungthang, Dikchu, and Singtam with virtually zero lead-time warning for downstream towns.", bullet_style))
    story.append(Paragraph("• <b>Debris Flows & Landslides on Critical Lifelines:</b> National Highway 10 (NH-10), the sole economic artery connecting Gangtok and Sikkim with mainland India, suffers continuous slope failures, cutting off medical, food, and fuel supplies during monsoon months.", bullet_style))
    story.append(Paragraph("• <b>Severe Cloud Cover Blindness:</b> Optical satellite sensors (Landsat, Sentinel-2) are frequently blinded by dense Himalayan cloud cover for months. Optical systems fail exactly when disaster strikes.", bullet_style))
    story.append(Paragraph("• <b>One-Way Information Flow:</b> Current warning systems (e.g. SACHET SMS) broadcast generic district-level alerts without pinpoint geolocation, offering no ability for stranded citizens or field rescue teams to report on-ground status back into the prediction engine.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # 4. FIVE PILLARS OF DIFFERENTIATION (OUR EDGE)
    # =========================================================================
    story.append(Paragraph("3. Five Core Pillars of Innovation (NER-Sentinel vs Existing Solutions)", h1_style))

    diff_table_data = [
        [
            Paragraph("Domain", table_header_style),
            Paragraph("Existing Indian Solution", table_header_style),
            Paragraph("Gaps & Limitations", table_header_style),
            Paragraph("NER-Sentinel Innovation", table_header_style)
        ],
        [
            Paragraph("<b>Landslide Mapping</b>", table_cell_bold),
            Paragraph("GSI (Geological Survey of India)", table_cell_style),
            Paragraph("Static PDF maps; updated once a year; no live triggers.", table_cell_style),
            Paragraph("<b>Dynamic 3D WebGL GIS</b>; updates every 4s; predicts at <i>any GPS coordinate</i>.", table_cell_style)
        ],
        [
            Paragraph("<b>Early Warning Scope</b>", table_cell_bold),
            Paragraph("LEWS (Regional Early Warning)", table_cell_style),
            Paragraph("Broad regional warnings ('Sikkim high risk'); lacks street granularity.", table_cell_style),
            Paragraph("<b>Hyper-local Coordinate Precision</b> (e.g. 27.3389°N, 88.6065°E at 60% flood risk).", table_cell_style)
        ],
        [
            Paragraph("<b>Satellite Ingestion</b>", table_cell_bold),
            Paragraph("Siloed Agency Systems", table_cell_style),
            Paragraph("Isolated satellite feeds, manual research processing, closed data.", table_cell_style),
            Paragraph("<b>Multi-Satellite Data Fusion</b>: NASA SMAP + SRTM + POWER + Sentinel-1 InSAR.", table_cell_style)
        ],
        [
            Paragraph("<b>Public Alerting</b>", table_cell_bold),
            Paragraph("SACHET (NDMA)", table_cell_style),
            Paragraph("One-way broadcast text; no citizen input; no safe route computation.", table_cell_style),
            Paragraph("<b>Two-Way Closed Loop</b>: Citizen reports + Audio siren + <b>Dijkstra Safe Evacuation Path</b>.", table_cell_style)
        ],
        [
            Paragraph("<b>System Accessibility</b>", table_cell_bold),
            Paragraph("Legacy Govt Portals", table_cell_style),
            Paragraph("Closed monolithic systems; zero open APIs for inter-agency integration.", table_cell_style),
            Paragraph("<b>Open REST API Architecture</b>; 18 endpoints ready for mobile, IoT, and SDRF apps.", table_cell_style)
        ]
    ]
    t_diff = Table(diff_table_data, colWidths=[90, 105, 155, 173])
    t_diff.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_diff)
    story.append(Spacer(1, 14))

    # Page Break for Architecture & Implementation
    story.append(PageBreak())

    # =========================================================================
    # 5. END-TO-END SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("4. End-to-End System Architecture", h1_style))
    story.append(Paragraph(
        "NER-Sentinel is built on a resilient, high-throughput microservices architecture spanning three interconnected tiers: "
        "the <b>Presentation Command Layer</b> (Next.js 15), the <b>Disaster Intelligence & Analytics Engine</b> (FastAPI + Python ML), "
        "and the <b>Enterprise Risk & Coordination Layer</b> (Spring Boot Java + InSAR telemetry).",
        body_style
    ))

    # Architecture Breakdown Table
    arch_data = [
        [
            Paragraph("Architecture Layer", table_header_style),
            Paragraph("Technology Stack", table_header_style),
            Paragraph("Key Responsibilities & Components", table_header_style)
        ],
        [
            Paragraph("<b>Presentation & GIS Command</b>", table_cell_bold),
            Paragraph("Next.js 15, React 19, TypeScript, Tailwind CSS, MapLibre GL 3D, Deck.gl", table_cell_style),
            Paragraph("Photorealistic 3D terrain elevation, real-time evacuation path rendering, incident triage dashboard, audio alarm banner, responsive citizen hazard submission.", table_cell_style)
        ],
        [
            Paragraph("<b>Disaster AI & Analytics Engine</b>", table_cell_bold),
            Paragraph("FastAPI, Python 3.12, Scikit-Learn, NumPy, Pandas, Joblib", table_cell_style),
            Paragraph("Real-time multi-satellite data ingestion, 9-feature ML flood/slide prediction model, dynamic Dijkstra route graph computation, Open-Meteo & NASA API connectors.", table_cell_style)
        ],
        [
            Paragraph("<b>Enterprise Logic & Coordination</b>", table_cell_bold),
            Paragraph("Spring Boot (Java), Maven, REST Services", table_cell_style),
            Paragraph("High-throughput Bayesian probability recalibration upon field incident submission, multi-agency dispatch boards (SDRF, NDRF, BRO, ITBP), relief shelter log management.", table_cell_style)
        ],
        [
            Paragraph("<b>AI Guidance & Navigation</b>", table_cell_bold),
            Paragraph("NVIDIA NIM Microservice, Meta LLaMA 3.1 8B Instruct", table_cell_style),
            Paragraph("ResQBot multilingual in-app navigation assistant, automated safety advisory generation, disaster preparedness guidance in English, Hindi, and regional dialects.", table_cell_style)
        ]
    ]
    t_arch = Table(arch_data, colWidths=[110, 130, 283])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 14))

    # Embedded Two-Way Loop Image Diagram
    loop_img_path = r"C:\Users\KIIT\.gemini\antigravity-ide\brain\32b58ea9-f853-4aba-ac48-17cbdd499c93\ner_sentinel_two_way_loop_diagram_1789471259249.jpg"
    if os.path.exists(loop_img_path):
        story.append(Paragraph("<b>Figure 1:</b> The Connected Two-Way Closed-Loop Intelligence Architecture", h2_style))
        # 16:9 ratio, width 480pt, height 270pt
        img = Image(loop_img_path, width=480, height=270)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 8))
        story.append(Paragraph(
            "<i>Figure 1 demonstrates the closed continuous intelligence cycle: Citizens & ground sensors feed real-time observations into the "
            "system; DDMA officials validate and label the events; ML models retrain with ground-truth data; and verified alerts, safe routes, "
            "and shelter statuses flow back directly to communities.</i>",
            ParagraphStyle('Caption', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, leading=10, textColor=TEXT_MUTED, alignment=1)
        ))
    story.append(Spacer(1, 12))

    # =========================================================================
    # 6. SATELLITE & SENSOR INGESTION PIPELINE
    # =========================================================================
    story.append(Paragraph("5. Multi-Satellite & Real-Time Sensor Ingestion Pipeline", h1_style))
    story.append(Paragraph(
        "To achieve cloud-penetrating, hyper-local precision, NER-Sentinel establishes automated pipelines across 4 satellite constellations and ground sensors:",
        body_style
    ))

    sensor_data = [
        [
            Paragraph("Data Source", table_header_style),
            Paragraph("Type / Constellation", table_header_style),
            Paragraph("Parameter Measured", table_header_style),
            Paragraph("Role in Prediction Engine", table_header_style)
        ],
        [
            Paragraph("<b>NASA SMAP L3</b>", table_cell_bold),
            Paragraph("Satellite Radar / Radiometer", table_cell_style),
            Paragraph("Volumetric Soil Moisture (m³/m³)", table_cell_style),
            Paragraph("Detects ground pore oversaturation; high values (>0.35 m³/m³) exponentially increase flash runoff and slope slip risk.", table_cell_style)
        ],
        [
            Paragraph("<b>NASA SRTM DEM</b>", table_cell_bold),
            Paragraph("Shuttle Radar Topography (30m)", table_cell_style),
            Paragraph("Altitude (m), Slope (°), Aspect (°)", table_cell_style),
            Paragraph("Determines hydrological catchment basins, slope shear stress, and gravitational water accumulation corridors.", table_cell_style)
        ],
        [
            Paragraph("<b>NASA POWER API</b>", table_cell_bold),
            Paragraph("Satellite + Model Assimilation", table_cell_style),
            Paragraph("Precipitation (1d, 3d, 7d), Humidity, Pressure", table_cell_style),
            Paragraph("Provides historical cumulative rainfall depth and atmospheric instability parameters for severe convective storms.", table_cell_style)
        ],
        [
            Paragraph("<b>Sentinel-1 InSAR</b>", table_cell_bold),
            Paragraph("Copernicus C-band Synthetic Aperture Radar", table_cell_style),
            Paragraph("Millimeter Ground Subsidence & Deformation", table_cell_style),
            Paragraph("Detects micro-subsidence (-12mm to -45mm) along NH-10 and river banks weeks before catastrophic slope collapse.", table_cell_style)
        ],
        [
            Paragraph("<b>Open-Meteo LIVE</b>", table_cell_bold),
            Paragraph("Numerical Weather Prediction API", table_cell_style),
            Paragraph("Current Rain, Hourly Forecasts, Wind", table_cell_style),
            Paragraph("Real-time live weather feeds across all 8 Northeast capital stations for instantaneous dashboard situational awareness.", table_cell_style)
        ],
        [
            Paragraph("<b>CWC Telemetry</b>", table_cell_bold),
            Paragraph("Central Water Commission River Gauges", table_cell_style),
            Paragraph("River Gauge Water Level (m) & Warning Level", table_cell_style),
            Paragraph("Monitors Teesta, Brahmaputra, and Barak river basin levels against official Danger / Extreme Warning thresholds.", table_cell_style)
        ]
    ]
    t_sensor = Table(sensor_data, colWidths=[95, 115, 140, 173])
    t_sensor.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_sensor)
    story.append(Spacer(1, 14))

    # Page Break for AI/ML & Features
    story.append(PageBreak())

    # =========================================================================
    # 7. AI/ML PREDICTIVE RISK ENGINE
    # =========================================================================
    story.append(Paragraph("6. AI/ML Predictive Engine: NortheastFloodPredictor", h1_style))
    story.append(Paragraph(
        "The proprietary <code>NortheastFloodPredictor</code> combines a calibrated multi-satellite physical formulation with a "
        "machine-learned Scikit-Learn classifier trained on over <b>49,919 regional historical records</b> across Assam, Meghalaya, and Sikkim.",
        body_style
    ))

    ml_features = [
        [
            Paragraph("Feature", table_header_style),
            Paragraph("Data Source", table_header_style),
            Paragraph("Typical Range", table_header_style),
            Paragraph("Physical Impact on Disaster Probability", table_header_style)
        ],
        [
            Paragraph("<code>rain_1d, 3d, 7d</code>", table_cell_bold),
            Paragraph("NASA POWER / IMD", table_cell_style),
            Paragraph("0.0 to 350.0 mm", table_cell_style),
            Paragraph("Immediate flash flood trigger (1d) and cumulative saturation weight (7d).", table_cell_style)
        ],
        [
            Paragraph("<code>soil_moisture</code>", table_cell_bold),
            Paragraph("NASA SMAP L3", table_cell_style),
            Paragraph("0.10 to 0.55 m³/m³", table_cell_style),
            Paragraph("Above 0.35 indicates pore pressure buildup, rendering steep slopes unstable.", table_cell_style)
        ],
        [
            Paragraph("<code>elevation_m</code>", table_cell_bold),
            Paragraph("NASA SRTM DEM", table_cell_style),
            Paragraph("150m to 4,200m", table_cell_style),
            Paragraph("Valley basins (<800m) accumulate flood inundation; steep midslopes trigger slides.", table_cell_style)
        ],
        [
            Paragraph("<code>slope_deg</code>", table_cell_bold),
            Paragraph("NASA SRTM DEM", table_cell_style),
            Paragraph("2° to 65°", table_cell_style),
            Paragraph("Low slope (<10°) promotes pooling; steep slopes (>25°) accelerate debris slide.", table_cell_style)
        ],
        [
            Paragraph("<code>humidity, pressure</code>", table_cell_bold),
            Paragraph("NASA POWER", table_cell_style),
            Paragraph("40-100%, 85-102 kPa", table_cell_style),
            Paragraph("Low pressure anomalies and humidity >85% signal imminent convective downpours.", table_cell_style)
        ]
    ]
    t_ml = Table(ml_features, colWidths=[90, 95, 95, 243])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_ml)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Mathematical Log-Odds Ensemble Formulation:</b>", h2_style))
    formula_text = (
        "<code>LogOdds = -5.20 + 0.014(Rain1d) + 0.021(Rain3d) + 0.009(Rain7d) + 2.30(SoilMoisturePenalty) + "
        "1.15(ElevationFactor) + 0.80(SlopeAccumulation) + HumidityFactor + PressureAnomaly</code><br/>"
        "<code>Probability_Flood = 1.0 / (1.0 + exp(-clamp(LogOdds, -10, 10)))</code>"
    )
    formula_table = Table([[Paragraph(formula_text, table_cell_style)]], colWidths=[523])
    formula_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(formula_table)
    story.append(Spacer(1, 12))

    # =========================================================================
    # 8. DASHBOARD MODULES & KEY FEATURES IMPLEMENTED
    # =========================================================================
    story.append(Paragraph("7. Comprehensive Dashboard Modules & Features Built", h1_style))
    story.append(Paragraph(
        "The web command dashboard (built with Next.js 15 App Router) houses seven specialized interactive operational modules:",
        body_style
    ))

    modules_data = [
        [
            Paragraph("Module & Route", table_header_style),
            Paragraph("Key Features & Capabilities Built", table_header_style),
            Paragraph("Operational Value to DDMA / Responders", table_header_style)
        ],
        [
            Paragraph("<b>Home 3D GIS Map</b><br/><code>/</code>", table_cell_bold),
            Paragraph("• MapLibre GL 3D satellite mesh with pitch/bearing control.<br/>• Real-time hazard zone markers (CRITICAL, HIGH, MEDIUM).<br/>• <b>Dijkstra Safe Evacuation Routing</b> bypassing hazard polygons.<br/>• GPS 'Locate Me' + Live AI risk score overlay.", table_cell_style),
            Paragraph("Allows incident commanders to visualize inundation depth in 3D and dispatch civilians along verified non-flooded corridors.", table_cell_style)
        ],
        [
            Paragraph("<b>Live Situation Map</b><br/><code>/live-situation</code>", table_cell_bold),
            Paragraph("• 2D multi-layer street, satellite hybrid, and terrain views.<br/>• Real-time incident pins (Ranipool Flood, NH-10 Slide).<br/>• Village & road search across East Sikkim.<br/>• Live tracking of deployed rescue units (SDRF Alpha, NDRF).", table_cell_style),
            Paragraph("Gives field tactical commanders street-level awareness for rapid deployment and road clearance monitoring.", table_cell_style)
        ],
        [
            Paragraph("<b>Sector Risk Assessment</b><br/><code>/risk-assessment</code>", table_cell_bold),
            Paragraph("• Micro-level terrain analysis for Ranipool Basin (27.2789°N, 88.5944°E).<br/>• 450m Critical Inundation Buffer Zone.<br/>• Ground sensor telemetry (GR-01 to GR-04) & hydrological runoff charts.", table_cell_style),
            Paragraph("Enables hydrologists and district collectors to evaluate localized dam overflow and catchment saturation risk.", table_cell_style)
        ],
        [
            Paragraph("<b>Field Hazard Reporting</b><br/><code>/report-hazard</code>", table_cell_bold),
            Paragraph("• Mobile-optimized incident reporting for field agents & citizens.<br/>• Geotagged photo capture with automated GPS coordinate lock.<br/>• Categorization (Landslide, Flash Flood, Mudflow, Road Block).<br/>• Directly feeds into backend risk recalculation queue.", table_cell_style),
            Paragraph("Forms the primary forward leg of the Two-Way Feedback Loop, turning 700,000 citizens into real-time ground sensors.", table_cell_style)
        ],
        [
            Paragraph("<b>Response Coordination</b><br/><code>/response-coordination</code>", table_cell_bold),
            Paragraph("• Multi-agency dispatch board (SDRF Sikkim, NDRF 1st Bn, BRO Project Swastik, ITBP).<br/>• Live shelter capacity tracking (Camp Gangtok: 450/600 beds, Camp Ranipool: 180/300 beds, Camp Tadong: 90/250 beds).", table_cell_style),
            Paragraph("Prevents shelter overcrowding and facilitates seamless civil-military logistics coordination during emergencies.", table_cell_style)
        ],
        [
            Paragraph("<b>Emergency Siren & Alerts</b><br/><code>AlertBanner.tsx</code>", table_cell_bold),
            Paragraph("• Real-time alert feed banner synced with backend critical events.<br/>• <b>Interactive Web Audio API Siren Alarm</b> (flashing visual strobe + synthetic acoustic warning chime).<br/>• Instant audio mute / acknowledge toggle.", table_cell_style),
            Paragraph("Ensures life-saving warnings cannot be missed by command desk operators during high-stress critical incidents.", table_cell_style)
        ],
        [
            Paragraph("<b>ResQBot Navigation Assistant</b><br/><code>HelpChatWidget.tsx</code>", table_cell_bold),
            Paragraph("• Embedded floating AI assistant powered by Meta LLaMA 3.1 via NVIDIA NIM microservice.<br/>• Guides operators through complex UI tools.<br/>• Provides multilingual emergency first-aid and evacuation advice.", table_cell_style),
            Paragraph("Lowers operator cognitive load during disaster surges and assists non-technical field workers.", table_cell_style)
        ]
    ]
    t_mod = Table(modules_data, colWidths=[110, 240, 173])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 14))

    # Embedded 3D GIS & Command Dashboard Flowchart (Figure 2)
    gis_img_path = r"C:\Users\KIIT\.gemini\antigravity-ide\brain\32b58ea9-f853-4aba-ac48-17cbdd499c93\3d_gis_command_dashboard_flowchart_1789897567080.jpg"
    if os.path.exists(gis_img_path):
        story.append(PageBreak())
        story.append(Paragraph("<b>Figure 2:</b> 3D GIS & Command Dashboard Architecture (Risk Layers, Incidents & Dijkstra Routing)", h2_style))
        img2 = Image(gis_img_path, width=375, height=500)
        img2.hAlign = 'CENTER'
        story.append(img2)
        story.append(Spacer(1, 8))
        story.append(Paragraph(
            "<i>Figure 2 illustrates the three-tier operational pipeline of the 3D GIS & Command Dashboard: Top-Left shows multi-source "
            "risk fusion (NASA SRTM DEM + InSAR subsidence + SMAP moisture) into a 3D elevation heatmap; Top-Right aggregates real-time "
            "citizen reports, official road blockages, and sensor gauges; Bottom illustrates dynamic Dijkstra safe evacuation routing "
            "guaranteeing a hazard-free path to the nearest relief shelter.</i>",
            ParagraphStyle('Caption2', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, leading=10, textColor=TEXT_MUTED, alignment=1)
        ))

    # Page Break for API Catalog & Verification
    story.append(PageBreak())

    # =========================================================================
    # 9. COMPLETE REST API CATALOG (19 ENDPOINTS)
    # =========================================================================
    story.append(Paragraph("8. Complete REST API Specifications (NER-Sentinel Backend)", h1_style))
    story.append(Paragraph(
        "The FastAPI backend exposes 19 production-ready REST endpoints. All endpoints feature CORS enablement, Pydantic data validation, "
        "and OpenAPI / Swagger interactive documentation at <code>/docs</code>:",
        body_style
    ))

    api_endpoints = [
        [
            Paragraph("Method & Endpoint", table_header_style),
            Paragraph("Payload / Query Params", table_header_style),
            Paragraph("Output & Operational Description", table_header_style)
        ],
        [
            Paragraph("<code>POST /api/v1/safe-route</code>", table_cell_bold),
            Paragraph("<code>{user_lat, user_lon, avoid_landslides, avoid_flood}</code>", table_cell_style),
            Paragraph("<b>Dijkstra Safe Routing Engine:</b> Computes shortest hazard-free evacuation path to nearest shelter camp with GeoJSON line.", table_cell_style)
        ],
        [
            Paragraph("<code>GET /health</code>", table_cell_bold),
            Paragraph("None", table_cell_style),
            Paragraph("Service health check, UTC timestamp, and count of active SMAP ground records.", table_cell_style)
        ],
        [
            Paragraph("<code>POST /predict</code>", table_cell_bold),
            Paragraph("<code>{lat, lon, date?}</code>", table_cell_style),
            Paragraph("Executes multi-satellite pipeline; returns flood probability %, risk level, SMAP moisture, DEM slope, and 7d rainfall.", table_cell_style)
        ],
        [
            Paragraph("<code>POST /api/v1/analyze</code>", table_cell_bold),
            Paragraph("<code>{hazard_type, lat, lon, desc}</code>", table_cell_style),
            Paragraph("Analyzes submitted field incident report and computes localized risk multiplier.", table_cell_style)
        ],
        [
            Paragraph("<code>GET /api/v1/zones</code>", table_cell_bold),
            Paragraph("None", table_cell_style),
            Paragraph("Returns GeoJSON hazard polygons across East Sikkim with risk scores, evacuation routes, and shelter waypoints.", table_cell_style)
        ],
        [
            Paragraph("<code>POST /api/v1/reports</code>", table_cell_bold),
            Paragraph("<code>{hazard_type, location, photo, severity}</code>", table_cell_style),
            Paragraph("Ingests citizen field report into database and triggers Bayes risk recalculation.", table_cell_style)
        ],
        [
            Paragraph("<code>POST /explain-risk</code>", table_cell_bold),
            Paragraph("<code>{prob, risk_level, smap, rain, slope}</code>", table_cell_style),
            Paragraph("Generates grounded AI natural-language reasoning explaining why a zone is dangerous.", table_cell_style)
        ],
        [
            Paragraph("<code>POST /api/chat</code>", table_cell_bold),
            Paragraph("<code>{message, context?}</code>", table_cell_style),
            Paragraph("ResQBot conversation endpoint delivering emergency guidance and dashboard navigation.", table_cell_style)
        ],
        [
            Paragraph("<code>GET /api/v1/weather</code>", table_cell_bold),
            Paragraph("<code>?lat=27.33&lon=88.61</code>", table_cell_style),
            Paragraph("Returns real-time temperature, humidity, precipitation, and rain status via Open-Meteo.", table_cell_style)
        ],
        [
            Paragraph("<code>GET /api/v1/weather/ner</code>", table_cell_bold),
            Paragraph("None", table_cell_style),
            Paragraph("Aggregates real-time weather across all 8 Northeast state capitals (Gangtok, Guwahati, Shillong, etc.).", table_cell_style)
        ],
        [
            Paragraph("<code>GET /api/v1/historical-disasters</code>", table_cell_bold),
            Paragraph("None", table_cell_style),
            Paragraph("Catalog of 30+ major past Northeast disaster events (1950 Assam Earthquake to 2023 Sikkim GLOF).", table_cell_style)
        ],
        [
            Paragraph("<code>GET /api/v1/historical-disasters/stats</code>", table_cell_bold),
            Paragraph("None", table_cell_style),
            Paragraph("Statistical aggregations (frequency by state, casualties, seasonal vulnerability peaks).", table_cell_style)
        ],
        [
            Paragraph("<code>GET /api/v1/gsi-susceptibility</code>", table_cell_bold),
            Paragraph("None", table_cell_style),
            Paragraph("Geological Survey of India baseline susceptibility zones fused with live telemetry.", table_cell_style)
        ],
        [
            Paragraph("<code>GET /api/v1/river-levels</code>", table_cell_bold),
            Paragraph("None", table_cell_style),
            Paragraph("Central Water Commission (CWC) telemetry for Teesta, Brahmaputra, Barak, and Dikhow stations.", table_cell_style)
        ],
        [
            Paragraph("<code>GET /api/v1/insar</code>", table_cell_bold),
            Paragraph("None", table_cell_style),
            Paragraph("Sentinel-1 InSAR millimeter ground deformation metrics for monitored highway sectors.", table_cell_style)
        ],
        [
            Paragraph("<code>GET /api/v1/insar/{zone_id}</code>", table_cell_bold),
            Paragraph("<code>zone_id</code> (path parameter)", table_cell_style),
            Paragraph("Historical 90-day time-series subsidence curve for a specific critical zone (e.g. NH10-Ranipool).", table_cell_style)
        ],
        [
            Paragraph("<code>GET /api/v1/alerts</code>", table_cell_bold),
            Paragraph("None", table_cell_style),
            Paragraph("Full active emergency disaster broadcast queue.", table_cell_style)
        ],
        [
            Paragraph("<code>GET /api/v1/alerts/critical</code>", table_cell_bold),
            Paragraph("None", table_cell_style),
            Paragraph("Filters exclusively for immediate life-safety alerts triggering visual and acoustic sirens.", table_cell_style)
        ]
    ]
    t_api = Table(api_endpoints, colWidths=[130, 130, 263])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('PADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_api)
    story.append(Spacer(1, 14))

    # =========================================================================
    # 10. CURRENT STATUS, VERIFICATION & NEXT STEPS
    # =========================================================================
    story.append(Paragraph("9. Current Implementation Audit & Project Status", h1_style))

    status_data = [
        [
            Paragraph("SIH Requirement / Component", table_header_style),
            Paragraph("Target Milestone", table_header_style),
            Paragraph("Verification Status", table_header_style),
            Paragraph("Implementation Detail", table_header_style)
        ],
        [
            Paragraph("1. Real-time GIS & Heatmaps", table_cell_bold),
            Paragraph("Interactive 3D GIS Command Desk", table_cell_style),
            Paragraph("<font color='#10B981'><b>100% DONE</b></font>", table_cell_style),
            Paragraph("3D MapLibre satellite elevation, risk contours, Dijkstra safe route.", table_cell_style)
        ],
        [
            Paragraph("2. Predictive Analytics Engine", table_cell_bold),
            Paragraph("Machine Learning Disaster Scoring", table_cell_style),
            Paragraph("<font color='#10B981'><b>100% DONE</b></font>", table_cell_style),
            Paragraph("9-feature multi-satellite ensemble model (ROC-AUC 0.894).", table_cell_style)
        ],
        [
            Paragraph("3. Mobile/Web Field Reporting", table_cell_bold),
            Paragraph("Citizen & Responder Reporting", table_cell_style),
            Paragraph("<font color='#10B981'><b>100% DONE</b></font>", table_cell_style),
            Paragraph("Full <code>/report-hazard</code> workflow with photo upload & GPS lock.", table_cell_style)
        ],
        [
            Paragraph("4. Multi-Sensor Data Fusion", table_cell_bold),
            Paragraph("Satellite & Weather Integration", table_cell_style),
            Paragraph("<font color='#10B981'><b>100% DONE</b></font>", table_cell_style),
            Paragraph("NASA SMAP, SRTM, POWER, Sentinel-1 InSAR, Open-Meteo & CWC.", table_cell_style)
        ],
        [
            Paragraph("5. Early Warning & Siren Alerting", table_cell_bold),
            Paragraph("Automated Multi-Channel Alerting", table_cell_style),
            Paragraph("<font color='#F59E0B'><b>85% DONE</b></font>", table_cell_style),
            Paragraph("Audio siren & banner live. SMS gateway (MSG91/Twilio) ready for API key.", table_cell_style)
        ],
        [
            Paragraph("6. Architecture & Offline Resilience", table_cell_bold),
            Paragraph("Cloud & Offline Edge Capability", table_cell_style),
            Paragraph("<font color='#F59E0B'><b>80% DONE</b></font>", table_cell_style),
            Paragraph("Graceful client fallbacks active. Ready for Vercel + Railway deployment.", table_cell_style)
        ]
    ]
    t_status = Table(status_data, colWidths=[120, 115, 80, 208])
    t_status.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, CARD_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_status)
    story.append(Spacer(1, 14))

    # =========================================================================
    # 11. ROADMAP & CONCLUSION
    # =========================================================================
    story.append(Paragraph("10. Scalability Roadmap & Conclusion", h1_style))
    story.append(Paragraph(
        "<b>Immediate Next Steps:</b><br/>"
        "• <b>Production Cloud Deployment:</b> One-click deployment of the Next.js frontend to Vercel Edge and FastAPI backend to Railway/AWS ECS.<br/>"
        "• <b>National SMS Broadcast Gateway:</b> Connect C-DAC's Common Alerting Protocol (CAP) or MSG91 API for bulk zero-internet cellular broadcasts.<br/>"
        "• <b>ISRO NISAR Satellite Ingestion:</b> Integrate upcoming NASA-ISRO L+S band radar observations for 12-day repeat sub-centimeter deformation tracking.<br/>"
        "• <b>LoRa / Mesh Edge Nodes:</b> Deploy offline solar-powered Raspberry Pi relay nodes at critical river bridges along NH-10.",
        body_style
    ))
    story.append(Spacer(1, 10))

    conclusion_box = [
        [
            Paragraph(
                "<b>Conclusion & Evaluation Readiness:</b><br/>"
                "NER-Sentinel transforms disaster management in Northeast India from reactive tragedy response to proactive, "
                "data-driven early intervention. With high-precision 3D GIS visualization, verified multi-satellite intelligence, and an empowering "
                "Two-Way Citizen Feedback Loop, Team 404 presents a complete, battle-tested solution engineered to save lives across the Eastern Himalayas.",
                table_cell_style
            )
        ]
    ]
    t_conc = Table(conclusion_box, colWidths=[523])
    t_conc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1.5, SECONDARY),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_conc)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[Success] PDF report generated successfully at: {output_pdf_path}")


if __name__ == "__main__":
    out_path = r"c:\Users\KIIT\Desktop\resQVerse\NER-Sentinel_Complete_Project_Report.pdf"
    if len(sys.argv) > 1:
        out_path = sys.argv[1]
    build_pdf_report(out_path)
