from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityEngine:

    def calculate_similarity(self, text1: str, text2: str) -> float:
        # Handle empty strings
        if not text1.strip() or not text2.strip():
            return 0.0
            
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))

        tfidf_matrix = vectorizer.fit_transform([text1, text2])

        score = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        return round(float(score) * 100, 2)