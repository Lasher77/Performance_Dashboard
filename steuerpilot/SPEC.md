# SteuerPilot – MVP-Konzept & Entwicklungsbriefing

## 1. Produktvision

**SteuerPilot** ist eine Web-App (PWA), die Privatpersonen durch ihre Steuererklärung führt. Der Mandant erfasst seine Daten in einer geführten, verständlichen Oberfläche. Die App übernimmt Berechnung, Belegauswertung und Aufbereitung. Ein Steuerberater prüft und gibt die Erklärung frei.

**Zielgruppe MVP:** Mandanten einer Steuerberaterkanzlei (initial eine Kanzlei, perspektivisch Multi-Tenant SaaS für mehrere Kanzleien).

**Kernprinzip:** Mandant erfasst → App verarbeitet → Steuerberater kontrolliert & gibt frei.

---

## 2. Stakeholder & Rollen

| Rolle | Beschreibung |
|-------|-------------|
| **Mandant** | Privatperson, die ihre Steuererklärung über die App einreicht |
| **Steuerberater** | Zugelassener Steuerberater, der prüft, korrigiert und freigibt |
| **Admin** | Kanzleiinhaber, verwaltet Einstellungen, Mandanten, Abrechnungen |

---

## 3. Steuerszenarien (MVP-Scope)

### Phase 1 – Kernszenarien
1. **Angestellte (Einkünfte aus nichtselbständiger Arbeit)**
   - Lohnsteuerbescheinigung
   - Werbungskosten (Fahrtkosten, Arbeitszimmer, Arbeitsmittel, Fortbildung)
   - Sonderausgaben (Versicherungen, Spenden, Kirchensteuer)
   - Außergewöhnliche Belastungen
   - Haushaltsnahe Dienstleistungen / Handwerkerleistungen

2. **Rentner**
   - Rentenbezugsmitteilungen
   - Weitere Einkünfte (Betriebsrente, Riester)
   - Kranken-/Pflegeversicherungsbeiträge
   - Altersentlastungsbetrag

3. **Vermieter (einzelne Objekte)**
   - Anlage V (Einkünfte aus Vermietung und Verpachtung)
   - Werbungskosten (AfA, Zinsen, Instandhaltung, Verwaltung)
   - Umlagen und Nebenkosten

4. **Kleinunternehmer / Freiberufler**
   - Anlage S / Anlage G
   - Einnahmenüberschussrechnung (EÜR) – Anlage EÜR
   - Betriebsausgaben
   - Umsatzsteuer-Voranmeldung (Hinweis/Verweis)

### Eskalationsregel
Erkennt die App Sachverhalte, die über den MVP-Scope hinausgehen (z.B. Auslandseinkünfte, Kryptowährungen, Erbschaft/Schenkung, komplexe Kapitalerträge), wird der Fall als "Beraterfall" gekennzeichnet und an den Steuerberater eskaliert.

---

## 4. Features (MVP)

### 4.1 Geführte Eingabe (Mandant)
- Schritt-für-Schritt-Wizard in Alltagssprache (kein ELSTER-Deutsch)
- Dynamische Fragen basierend auf vorherigen Antworten
- Fortschrittsanzeige pro Bereich
- Zwischenspeicherung – Mandant kann jederzeit unterbrechen und fortfahren
- Hilfetexte und Tooltips zu jedem Eingabefeld
- Validierung in Echtzeit (Plausibilitätschecks)

### 4.2 Belege fotografieren / hochladen
- Kamera-Integration (PWA: über Browser-API)
- Unterstützte Formate: JPG, PNG, PDF
- Zuordnung zu Kategorien
- Galerie-Ansicht aller hochgeladenen Belege pro Steuererklärung
- Speicherung: verschlüsselt auf dem Server

### 4.3 KI-gestützte Belegauswertung
- OCR (Texterkennung) auf hochgeladenen Belegen
- Automatische Kategorisierung (Belegart erkennen)
- Datenextraktion: relevante Werte aus Belegen auslesen
- Vorschlagswerte in Eingabefelder übernehmen (Mandant bestätigt oder korrigiert)

### 4.4 Chat / Nachrichtenfunktion
- Asynchroner Chat zwischen Mandant und Steuerberater
- Bezug auf konkrete Eingabefelder oder Belege möglich
- Benachrichtigungen (E-Mail und/oder Push via PWA)
- Chat-Verlauf pro Steuererklärung archiviert

### 4.5 Automatische Steuerberechnung / Erstattungsvorschau
- Berechnung der voraussichtlichen Steuerlast / Erstattung in Echtzeit
- Basierend auf aktuellen Steuertabellen und Freibeträgen
- Optimierungshinweise

### 4.6 Steuerberater-Dashboard
- Übersicht aller eingereichten Steuererklärungen mit Status
- Status-Workflow: Entwurf → Eingereicht → In Prüfung → Rückfrage → Freigegeben → Übermittelt
- Detail-Ansicht: alle Eingaben des Mandanten, Belege, berechnete Werte
- Korrekturmöglichkeit
- Freigabe-Button mit digitaler Bestätigung

### 4.7 Export / Schnittstellen
- PDF-Export: Zusammenfassung der Steuererklärung
- DATEV-Export: DATEV-kompatibles Format zum Import in Kanzleisoftware

---

## 5. Technischer Stack

| Komponente | Technologie |
|-----------|------------|
| Frontend | React + TypeScript (PWA mit Workbox) |
| Backend | Python + FastAPI |
| Datenbank | PostgreSQL |
| ORM | SQLAlchemy + Alembic |
| OCR / KI | Tesseract + Claude API |
| Auth | JWT + bcrypt |
| Chat | WebSocket (FastAPI) |
| PDF | WeasyPrint oder ReportLab |
| DATEV-Export | Custom Python-Modul |
| Hosting | Self-hosted, Docker Compose |

---

## 6. Datenmodell

### Kern-Entitäten

```
Tenant (Kanzlei) – Multi-Tenancy von Anfang an
├── id (UUID), name, branding (JSONB), settings (JSONB), datev_config (JSONB)

User
├── id (UUID), tenant_id → Tenant
├── email, password_hash
├── role (MANDANT | STEUERBERATER | ADMIN)
├── first_name, last_name, tax_id
├── created_at, updated_at

TaxReturn (Steuererklärung)
├── id (UUID), tenant_id → Tenant, user_id → User
├── tax_year, status (DRAFT | SUBMITTED | IN_REVIEW | QUERY | APPROVED | EXPORTED)
├── assigned_advisor_id → User
├── scenarios [] (EMPLOYED, RETIREE, LANDLORD, SELF_EMPLOYED)
├── estimated_refund (Decimal)

TaxSection (Bereich)
├── id (UUID), tax_return_id → TaxReturn
├── section_type (INCOME, EXPENSES, SPECIAL_EXPENSES, RENTAL, BUSINESS, etc.)
├── status (NOT_STARTED | IN_PROGRESS | COMPLETED)
├── data (JSONB)

Document (Beleg)
├── id (UUID), tax_return_id → TaxReturn, tax_section_id → TaxSection
├── file_path, file_type, category
├── ocr_text, ocr_data (JSONB), ocr_status

Message (Chat)
├── id (UUID), tax_return_id → TaxReturn, sender_id → User
├── content, reference_type (FIELD | DOCUMENT | GENERAL), reference_id
├── read_at, created_at

Calculation (Steuerberechnung)
├── id (UUID), tax_return_id → TaxReturn
├── input_data (JSONB), result_data (JSONB), estimated_refund

AdvisorNote (Berater-Anmerkung)
├── id (UUID), tax_return_id → TaxReturn
├── tax_section_id, field_key, note, correction_value
```

---

## 7. MVP-Priorisierung

### V1.0 (Must Have)
- Auth (Mandant + Steuerberater)
- Geführte Eingabe: Szenario "Angestellte"
- Beleg-Upload
- Steuerberater-Dashboard mit Status-Workflow
- Chat
- PDF-Export
- DATEV-Export (Basis)
- Grundlegende Steuerberechnung
- DSGVO-Grundlagen
- Responsive / PWA

### V1.1 (Should Have)
- Szenarien: Rentner, Vermieter
- KI-Belegauswertung (OCR)
- Optimierungshinweise
- E-Mail-Benachrichtigungen
- Mandanten-Einladung per E-Mail

### V1.2+ (Nice to Have)
- Szenario: Kleinunternehmer
- Multi-Tenant UI + Branding
- Push-Notifications
- Erweiterte DATEV-Integration
- Direkte ELSTER-Anbindung
