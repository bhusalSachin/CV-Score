from .pdf_extractor import PDFExtractor
from .section_extractor import SectionExtractor, CVSectionClassifier
from .similarity_engine import SimilarityEngine
from .cv_scorer import CVScorer

class CVAnalyzer:

    def __init__(self):

        self.pdf_extractor = PDFExtractor()
        self.section_extractor = SectionExtractor()
        self.cv_classifier = CVSectionClassifier()
        self.similarity_engine = SimilarityEngine()
        self.cv_scorer = CVScorer(self.similarity_engine)

    def analyze(self, pdf_path, vacancy_requirements):

        print("Starting CV analysis...")

        cv_text = self.pdf_extractor.extract_text(pdf_path)

        print("Extracted text:")
        print(cv_text)

        # Extract sections using sentence transformer classifier
        lines = [line.strip() for line in cv_text.split("\n") if len(line.strip()) > 2]
        sections = {"skills": [], "experience": [], "education": []}

        for line in lines:
            label = self.cv_classifier.classify_line(line)
            if label in sections:
                sections[label].append(line)

        # Convert lists to strings
        for key in sections:
            sections[key] = " ".join(sections[key])

        print("Extracted sections:")
        print(sections)

        scores = self.cv_scorer.score_sections(
            sections,
            vacancy_requirements
        )

        print("Calculated scores:")
        print(scores)

        return {
            "sections": sections,
            "scores": scores
        }