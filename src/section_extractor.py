import re
from flair.data import Sentence
from flair.models import TextClassifier

class SectionExtractor:

    def __init__(self) -> None:
        """
        Initialize the SectionExtractor with flair models for classification
        """
        self.classifier = TextClassifier.load('sentiment')
    

    def _preprocess_text(self, cv_text: str):
        """
        Split CV text into clean lines
        """
        lines = [line.strip() for line in cv_text.split("\n")]
        return [line for line in lines if len(line) > 2]

    def _classify_line(self, line: str):
        """
        Predict section label for a single line
        """
        sentence = Sentence(line)
        self.classifier.predict(sentence)

        if sentence.labels:
            return sentence.labels[0].value

        return "other"

    def extract_sections_with_flair(self, cv_text: str):
        """
        Extract structured sections from CV
        """
        sections = {
            "skills": [],
            "experience": [],
            "education": []
        }

        lines = self._preprocess_text(cv_text)

        for line in lines:
            label = self._classify_line(line)

            if label in sections:
                sections[label].append(line)

        # convert to string
        for key in sections:
            sections[key] = " ".join(sections[key])

        return sections
    
    def extract_cv_sections(self, cv_text: str) -> dict: 
        """Extract different sections from CV text using improved categorization""" 

        sections = { "skills": [], "experience": [], "education": [] } 
        
        # Define section keywords and patterns 
        section_patterns = { 
            "skills": [ 
                r"(?i)skills?:?\s*", 
                r"(?i)technical\s+skills?:?\s*", 
                r"(?i)competenc(?:y|ies):?\s*", 
                r"(?i)expertise?:?\s*", 
                r"(?i)proficiencies?:?\s*",
                r"(?i)interests?:?\s*",
                r"(?i)hobbies?:?\s*",
                r"(?i)activities?:?\s*"
            ], 
            "experience": [ 
                r"(?i)experience?:?\s*", 
                r"(?i)work\s+experience?:?\s*", 
                r"(?i)employment\s+history?:?\s*", 
                r"(?i)professional\s+experience?:?\s*", 
                r"(?i)career\s+history?:?\s*",
                r"(?i)vocational\s+training?:?\s*",
                r"(?i)training?:?\s*",
                r"(?i)employment?:?\s*"
            ], 
            "education": [ 
                r"(?i)education?:?\s*", 
                r"(?i)academic\s+background?:?\s*", 
                r"(?i)qualifications?:?\s*", 
                r"(?i)degrees?:?\s*", 
                r"(?i)university?:?\s*",
                r"(?i)school\s+education?:?\s*"
            ] 
        }
        
        # Define content patterns for each section 
        content_patterns = { "skills": [ r"(?i)(?:python|java|javascript|sql|html|css|react|angular|node\.?js|aws|azure|docker|kubernetes)", r"(?i)(?:leadership|communication|teamwork|problem\s+solving|analytical|project\s+management)", r"(?i)(?:machine\s+learning|data\s+analysis|web\s+development|software\s+development)" ], "experience": [ r"(?i)(?:\d{1,2}\s*(?:years?|yrs?)\s*(?:of\s+)?experience)", r"(?i)(?:senior|junior|lead|principal|manager|developer|engineer|analyst)", r"(?i)(?:responsible\s+for|managed|developed|implemented|designed|created)" ], "education": [ r"(?i)(?:bachelor|master|phd|doctorate|degree|diploma|certificate)", r"(?i)(?:university|college|institute|school)", r"(?i)(?:computer\s+science|engineering|business|arts|science)" ] } 
        
        lines = cv_text.split('\n') 
        
        current_section = None 
        
        section_content = {section: [] for section in sections} 
        
        # First pass: Identify section headers 
        for i, line in enumerate(lines): 
            line_stripped = line.strip() 
            
            # Check for section headers - prioritize more specific patterns first
            for section_name, patterns in section_patterns.items(): 
                for pattern in patterns: 
                    if re.match(pattern, line_stripped): 
                        # If this is vocational training, prioritize experience over education
                        if "vocational" in line_stripped.lower() and section_name == "education":
                            current_section = "experience"
                        else:
                            current_section = section_name 
                        break 
            
            # Add content to current section if current_section and line_stripped:
            if current_section and line_stripped:
                section_content[current_section].append(line_stripped) 
        
        # Second pass: Categorize uncategorized content using content patterns 
        for i, line in enumerate(lines): 
            line_stripped = line.strip() 
            
            if not line_stripped or len(line_stripped) < 3: 
                continue 
            
            # Skip if already categorized 
            already_categorized = False 
            for section_lines in section_content.values(): 
                if line_stripped in section_lines: 
                    already_categorized = True 
                    break 
            
            if not already_categorized: 
                # Use content patterns to categorize 
                section_scores = {} 
                for section_name, patterns in content_patterns.items(): 
                    score = 0 
                    for pattern in patterns: 
                        if re.search(pattern, line_stripped): 
                            score += 1 
                    section_scores[section_name] = score 
                
                # Assign to section with highest score 
                if max(section_scores.values()) > 0: 
                    best_section = max(section_scores, key=section_scores.get) 
                    section_content[best_section].append(line_stripped) 
        
        # Convert lists to strings 
        for section_name in sections: 
            sections[section_name] = " ".join(section_content[section_name]) 
        
        return sections

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class CVSectionClassifier:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.section_prototypes = {
            "skills": "python java docker kubernetes programming languages technical skills",
            "experience": "worked at company engineer developer project experience job role",
            "education": "bachelor degree university college academic education diploma"
        }

        self.section_embeddings = {
            k: self.model.encode(v)
            for k, v in self.section_prototypes.items()
        }

    def classify_line(self, line):
        line_embedding = self.model.encode(line)

        scores = {
            section: cosine_similarity(
                [line_embedding], [emb]
            )[0][0]
            for section, emb in self.section_embeddings.items()
        }

        return max(scores, key=scores.get)