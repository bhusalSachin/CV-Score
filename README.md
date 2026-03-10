# CV Parser

A powerful Python-based tool designed to automate the process of analyzing Curriculum Vitae (CV) files. It extracts text from PDFs and DOCX files, categorizes content into key sections (Skills, Experience, Education), and calculates a similarity score against specific job vacancy requirements using advanced NLP techniques.

## 🚀 Key Features

- **Multi-format Extraction**: Supports text and table extraction from PDF files using `pdfplumber` and DOCX files via `kreuzberg`.
- **AI-Powered Sectioning**: Utilizes `flair` and `sentence-transformers` to intelligently classify CV lines into relevant sections.
- **Intelligent Scoring**: Calculates similarity scores between CV sections and job requirements using `TfidfVectorizer` and Cosine Similarity.
- **Weighted Analysis**: Provides an overall score based on customizable weights for different sections (default: Skills 40%, Experience 40%, Education 20%).
- **Structured Output**: Generates a detailed `result.json` containing extracted sections and their respective scores.

## 🛠️ Tech Stack

- **Language**: Python 3.12+
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **NLP Libraries**:
  - `flair`: For text classification.
  - `sentence-transformers`: For semantic similarity and line classification.
  - `scikit-learn`: For TF-IDF vectorization and cosine similarity.
- **Extraction**:
  - `pdfplumber`: For robust PDF processing.
  - `kreuzberg`: For high-quality text extraction from various formats (DOCX).

## 📦 Installation

This project uses `uv` for dependency management. Ensure you have it installed, then run:

```bash
uv sync
```

## 💻 Usage

To analyze a CV, you can run the main entry point:

```bash
uv run main.py
```

### Example Configuration (`main.py`)

You can define the vacancy requirements directly in `main.py`:

```python
vacancy_requirements = {
    "skills": "Python SQL machine learning cloud",
    "experience": "software engineer agile project development",
    "education": "bachelor computer science"
}

result = analyzer.analyze("./assets/samples/cv2.pdf", vacancy_requirements)
```

The results will be saved to `result.json`.

## 📂 Project Structure

```text
cv_parser/
├── main.py                # Entry point for the application
├── src/
│   ├── cv_analyzer.py     # Main orchestration logic
│   ├── pdf_extractor.py   # PDF text and table extraction
│   ├── section_extractor.py # AI-powered section classification
│   ├── similarity_engine.py # Text similarity calculation
│   ├── cv_scorer.py       # Weighted scoring logic
│   └── kreuzberg.py       # DOCX extraction utility
├── assets/
│   ├── samples/           # Sample CV files (PDF, DOCX)
│   └── outputs/           # Directory for generated results
└── pyproject.toml         # Project dependencies and metadata
```

## ⚙️ Configuration

You can adjust the importance of each section by modifying the `weights` dictionary in `src/cv_scorer.py`:

```python
weights = {
    "skills": 0.4,
    "experience": 0.4,
    "education": 0.2
}
```

## 📄 License

Sachin Bhusal
