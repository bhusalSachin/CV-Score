class CVScorer:

    def __init__(self, similarity_engine):
        self.similarity_engine = similarity_engine

    def score_sections(self, cv_sections, vacancy_requirements):

        scores = {}

        weights = {
            "skills": 0.4,
            "experience": 0.4,
            "education": 0.2
        }

        overall = 0

        for section, cv_text in cv_sections.items():

            vacancy_text = vacancy_requirements.get(section, "")

            score = self.similarity_engine.calculate_similarity(
                cv_text,
                vacancy_text
            )

            scores[section] = score
            overall += score * weights.get(section, 0)

        scores["overall"] = round(overall, 2)

        return scores