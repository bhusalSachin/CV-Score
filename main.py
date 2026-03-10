from src.cv_analyzer import CVAnalyzer

def main():

    analyzer = CVAnalyzer()

    # vacancy_requirements = {
    #     "skills": "Python SQL machine learning cloud",
    #     "experience": "software engineer agile project development",
    #     "education": "bachelor computer science"
    # }

    vacancy_requirements = {
        "skills": "drawing music production driver license forklift teamwork activities",
        "experience": "media designer employee sheet metal technology training",
        "education": "school education secondary school vocational training primary school"
    }

    result = analyzer.analyze(
        "./assets/samples/cv2.pdf",
        vacancy_requirements
    )

    with open("result.json", "w") as f:
        import json
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    main()
