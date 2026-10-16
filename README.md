# 🛰️ resQVerse (NER-Sentinel) — AI-Powered Geospatial Disaster Decision Support Platform

An end-to-end, multi-tier disaster early warning, risk intelligence, and unified emergency response system designed to mitigate floods, landslides, and climate hazards across high-vulnerability regions.

---

## 👥 Team & Contribution Breakdown

> **Project Origin:** Developed as a comprehensive 6-member collaborative engineering initiative solving the Smart India Hackathon (SIH) Disaster Management problem statement.

| Member / Role | Core Modules & Responsibilities |
| :--- | :--- |
| **Harshvardhan Singh**<br>`@Lucifer-67890`<br>*(Co-Ideator & Web Dashboard / LLM Lead)* | • **Central Government Web Command Portal (`NER-Sentinel-GovDashboard`):** Architected and built the full-stack Next.js 15, TypeScript, and TailwindCSS command dashboard featuring live incident logging, 2D/3D geospatial terrain mapping, and multi-agency response dispatch.<br>• **LLM Assistant Microservice (`NER-Sentinel/nvidia_help_chatbot.py`):** Developed and integrated an AI-driven conversational guidance system powered by NVIDIA NIM for first responders and disaster coordinators.<br>• **Cross-Platform REST API Pipeline:** Designed unified data schemas and RESTful route handlers to ingest citizen hazard reports and broadcast alerts in real-time. |
| **Collaborator Team (5 Members)** | • **Satellite & Hydrological Risk Engine (`NER-Sentinel-RiskEngine`):** Synthetic Aperture Radar (InSAR Sentinel-1) differential interferometry and flood forecasting models.<br>• **Field Mobile Application (`NER-Sentinel-Android`):** Native Android/Kotlin client for crowdsourced citizen reporting and offline-first hazard telemetry. |

---

## 🚀 System Architecture

```text
resQVerse / NER-Sentinel Architecture:

┌─────────────────────────────────────────────────────────────┐
│             CITIZEN / FIRST RESPONDER LAYER                 │
│         Android App (Kotlin) & Crowdsourced Alerts          │
└──────────────────────────────┬──────────────────────────────┘
                               │ REST / JSON Ingestion
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  CENTRAL BACKEND & SERVICES                 │
│  FastAPI / Flask Microservices + NVIDIA NIM LLM Chatbot     │
│       Data Inventory • Geospatial Preprocessing API         │
└──────────────────────────────┬──────────────────────────────┘
                               │ Real-Time WebSocket / SSE
                               ▼
┌─────────────────────────────────────────────────────────────┐
│          GOVERNMENT COMMAND DASHBOARD (WEB PORTAL)          │
│   Next.js 15 • TypeScript • TailwindCSS • Interactive GIS   │
│   Live Incidents • Sector Maps • Emergency Coordination     │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features Owned & Implemented

### 1. 🖥️ Government Web Command Portal (`NER-Sentinel-GovDashboard`)
- **Next.js 15 & React 19:** High-performance responsive dashboard for state disaster management authorities (SDMA / NDRF).
- **Interactive Geospatial Visualization:** Real-time 2D and 3D elevation maps displaying hazard perimeters, affected infrastructure, and flood water levels.
- **Incident Dispatch & Coordination:** Categorized incident management (Urgent, Moderate, Low) with automated routing to response teams.
- **Automated Situation Reports:** Live summary generator converting field telemetry into downloadable PDF intelligence reports.

### 2. 🤖 First Responder LLM Chatbot (`nvidia_help_chatbot.py`)
- **NVIDIA NIM LLM Microservice:** Conversational intelligence engine running on a dedicated port for zero-latency operations.
- **Disaster Advisory & Navigation:** Real-time contextual assistance guiding responders to nearest shelters, relief camps, and safe evacuation corridors.
- **Zero-Dependency Resilience:** Embedded fallback server ensuring continuous availability during network disruptions.

### 3. 🔌 Robust REST API Pipeline
- **Strict Data Contracts:** Typed JSON schemas for incoming hazard reports, sensor telemetry, and broadcast alerts.
- **Cross-Service Interoperability:** Seamless data bridge connecting the Python ML/LLM services to the Next.js frontend.

---

## 🛠️ Technology Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Web Dashboard** | Next.js 15, TypeScript, TailwindCSS, Lucide Icons, Leaflet / Mapbox GL |
| **Backend & APIs** | Python 3.10+, FastAPI, Flask, RESTful Endpoints, JSON Serialization |
| **AI / LLM Microservice** | NVIDIA NIM API, Prompt Engineering, Contextual Q&A |
| **Data & Geoprocessing** | GeoJSON, InSAR Radar (Sentinel-1), Pandas, NumPy |
| **Mobile Client (Team)** | Android SDK, Kotlin, Jetpack Compose |
| **DevOps & Version Control** | Git, GitHub, VS Code |

---

## 📁 Repository Structure

```text
resQVerse/
├── NER-Sentinel-GovDashboard/   # [Core] Next.js 15 Web Command Dashboard
│   ├── app/                     # App router pages (dashboard, alerts, maps, reports)
│   ├── components/              # LiveRiskMap, InSARMonitor, TopNavbar, Sidebar
│   └── public/                  # Map assets, 3D tiles, and styling
├── NER-Sentinel/                # [Core] Backend Services & LLM Chatbot
│   ├── nvidia_help_chatbot.py   # NVIDIA NIM LLM emergency navigation microservice
│   ├── llm_app.py               # Disaster situation prediction & analysis service
│   ├── northeast_flood_predictor.py # Machine learning hazard classification
│   └── data_inventory/          # Data schemas and telemetry records
├── NER-Sentinel-RiskEngine/     # Hydrological risk calculation models
├── NER-Sentinel-Android/        # Mobile field application source code (Kotlin)
├── generate_pdf_report.py       # Automated situation report compiler
└── README.md                    # System documentation & team breakdown
```

---

## ⚡ Getting Started Locally

### 1. Web Dashboard Setup (`NER-Sentinel-GovDashboard`)
```bash
cd NER-Sentinel-GovDashboard/web-dashboard
npm install
npm run dev
```
Access the Command Portal at: **`http://localhost:3000`**

### 2. LLM Help Chatbot Microservice (`NER-Sentinel`)
```bash
cd NER-Sentinel
python nvidia_help_chatbot.py
```
The Chatbot Service will be live at: **`http://localhost:5001`**

---

## 👤 Author & Contributor

- **Harshvardhan Singh** — Full-Stack Web & LLM Lead
- **GitHub:** [@Lucifer-67890](https://github.com/Lucifer-67890)
- **Email:** singhharshvardhan148@gmail.com
