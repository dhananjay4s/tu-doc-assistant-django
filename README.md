# TU BCA Document Assistant

A rule-based academic document validator for **Tribhuvan University (TU) FOHSS** students. Helps validate BCA project reports and internship reports against official TU formatting guidelines.

---

## Supported Documents

| Semester | Document | Course Code |
|----------|----------|-------------|
| 4th | Project I | CACS256 |
| 6th | Project II | CAPJ356 |
| 7th | Internship Report | CACS357 |
| 8th | Project III | CACS452 |

---

## Features

- Section structure detection (required vs missing)
- Grammar analysis using spaCy + LanguageTool
- Passive voice / first-person detection with fix suggestions
- Informal vocabulary checker with academic replacements
- IEEE citation format validation
- DOCX formatting check (font, margins, spacing, page size)
- Group member detection (1 or 2 members)
- PDF + DOCX file upload support
- Analysis report download (PDF)
- Word count analysis with TOC-aware section detection
- Roman numeral false positive filtering (i, ii, iii)
- Nepali name spelling false positive suppression
- Group member detection with roll number parsing
- Analysis report download (print-to-PDF)

---

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **NLP:** spaCy (en_core_web_sm), LanguageTool
- **File parsing:** pdfplumber, python-docx
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Environment:** python-dotenv (.env based config)

---

## Project Structure

```
tu-doc-assistant/
├── backend/
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── analyzer/
│   │   ├── validators/
│   │   │   ├── structure.py        ← Section detection
│   │   │   ├── wordcount.py        ← Word count analysis
│   │   │   ├── language.py         ← Grammar + tone check
│   │   │   ├── formatting.py       ← TU format rules
│   │   │   └── feedback_generator.py ← Fix suggestions
│   │   ├── utils/
│   │   │   └── file_extractor.py   ← PDF/DOCX parser
│   │   └── views.py
│   ├── manage.py
│   ├── requirements.txt
│   └── .env                        ← Create this (see setup)
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```

---

## Setup & Installation

### Requirements
- Python 3.10+
- pip
- Java (required by LanguageTool — install from java.com)

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/tu-doc-assistant.git
cd tu-doc-assistant
```

**2. Create and activate virtual environment**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Download spaCy language model**
```bash
python -m spacy download en_core_web_sm
```

**5. Create `.env` file**

Create `backend/.env` with the following:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
```

Generate a secret key:
```bash
python -c "from django.utils.crypto import get_random_string; print(get_random_string(50))"
```

**6. Run migrations**
```bash
python manage.py migrate
```

**7. Start the backend server**
```bash
python manage.py runserver
```

Backend runs at: `http://127.0.0.1:8000`

**8. Open the frontend**
```bash
cd ../frontend
python -m http.server 3000
```

Open browser: `http://localhost:3000`

> **Note:** First request may take 20-30 seconds as LanguageTool 
> downloads its JAR file (~259MB) on first run. This happens once only.
> Java must be installed for LanguageTool to work.
> DOCX upload recommended over PDF for accurate formatting analysis.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/templates/` | List all TU templates |
| GET | `/api/templates/<doc_type>/` | Get template details |
| POST | `/api/analyze/` | Analyze a document |

### Analyze endpoint

**File upload (PDF/DOCX):**
```
POST /api/analyze/
Content-Type: multipart/form-data

file: <file>
doc_type: project_1 | project_2 | internship | project_3
```

**Plain text:**
```
POST /api/analyze/
Content-Type: application/json

{
  "text": "document content here...",
  "doc_type": "project_2"
}
```

---

## Formatting Standards (TU FOHSS)

| Element | Standard |
|---------|----------|
| Font | Times New Roman |
| Chapter heading | 16pt Bold, Center |
| Section heading | 14pt Bold, Left |
| Sub-section | 12pt Bold |
| Body text | 12pt Regular, Justified |
| Line spacing | 1.5 |
| Left margin | 1.25 inch (35mm) |
| Right/Top/Bottom | 1.0 inch |
| Page numbering | Roman (front matter), Arabic (Chapter 1+) |
| Referencing | IEEE format |
| Binding | Golden Embracing, Black Cover |
| Copies | 3 (Library + Self + Dean Office) |

---

## Contributing

This project is built for TU BCA students. Contributions welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add your feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## Dependencies

django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
pdfplumber==0.10.3
python-docx==1.1.0
spacy==3.7.4
language-tool-python==2.7.1
python-dotenv==1.0.0

---

## License

MIT License — free to use and modify.

---

## Acknowledgements

- Tribhuvan University, Faculty of Humanities and Social Sciences
- United College, Kumaripati (Project II Guidelines 2024)
- TU CDC Official BCA Curriculum Documents