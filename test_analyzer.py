import json
import tempfile
import unittest
from pathlib import Path

from src.analyzer import SkillGapAnalyzer
from src.data_manager import DataManager
from src.models import Candidate, Role
from src.validator import (
    ValidationError,
    parse_skills
)


class TestSkillGapAnalyzer(unittest.TestCase):

    def setUp(self) -> None:
        role = Role(
            name="Machine Learning Engineer",
            description="Builds machine-learning systems.",
            required=[
                "Python",
                "SQL",
                "Machine Learning",
                "Scikit-learn"
            ],
            important=[
                "Git",
                "Deep Learning"
            ],
            optional=[
                "Docker"
            ]
        )

        self.analyzer = SkillGapAnalyzer(
            {role.name: role}
        )
        self.role_name = role.name

    def test_all_skills_present_returns_100_percent(self) -> None:
        candidate = Candidate(
            name="Asha",
            skills=parse_skills(
                "Python, SQL, ML, sklearn, Git, "
                "Deep Learning, Docker"
            )
        )

        report = self.analyzer.analyze(
            candidate,
            self.role_name
        )

        self.assertEqual(report.match_percentage, 100.0)
        self.assertEqual(report.missing_skills, [])
        self.assertEqual(report.match_level, "Strong Match")

    def test_partial_skills_identifies_missing_skills(self) -> None:
        candidate = Candidate(
            name="Asha",
            skills=parse_skills("Python, SQL")
        )

        report = self.analyzer.analyze(
            candidate,
            self.role_name
        )

        missing_names = {
            gap.skill for gap in report.missing_skills
        }

        self.assertIn("Machine Learning", missing_names)
        self.assertIn("Scikit-learn", missing_names)
        self.assertLess(report.match_percentage, 100)

    def test_empty_skill_input_raises_validation_error(self) -> None:
        with self.assertRaises(ValidationError):
            parse_skills("   ")

    def test_duplicate_skills_are_removed(self) -> None:
        skills = parse_skills(
            "Python, python, PYTHON, SQL, sql"
        )

        self.assertEqual(skills, ["python", "sql"])

    def test_alias_sklearn_is_normalized(self) -> None:
        skills = parse_skills("sklearn")

        self.assertEqual(skills, ["scikit-learn"])

    def test_different_capitalization_matches(self) -> None:
        candidate = Candidate(
            name="Asha",
            skills=parse_skills("PYTHON, sql")
        )

        report = self.analyzer.analyze(
            candidate,
            self.role_name
        )

        self.assertIn("Python", report.matched_skills)
        self.assertIn("SQL", report.matched_skills)

    def test_unknown_role_raises_value_error(self) -> None:
        candidate = Candidate(
            name="Asha",
            skills=["python"]
        )

        with self.assertRaises(ValueError):
            self.analyzer.analyze(
                candidate,
                "Unknown Role"
            )

    def test_high_priority_filter(self) -> None:
        candidate = Candidate(
            name="Asha",
            skills=parse_skills("Python")
        )

        report = self.analyzer.analyze(
            candidate,
            self.role_name
        )

        high_priority_gaps = self.analyzer.filter_gaps(
            report,
            "HIGH"
        )

        self.assertTrue(high_priority_gaps)
        self.assertTrue(
            all(
                gap.priority == "HIGH"
                for gap in high_priority_gaps
            )
        )

    def test_role_search_by_skill(self) -> None:
        results = self.analyzer.search_roles("machine learning")

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].name,
            "Machine Learning Engineer"
        )

    def test_history_is_saved_and_loaded(self) -> None:
        candidate = Candidate(
            name="Asha",
            skills=parse_skills("Python, SQL")
        )
        report = self.analyzer.analyze(
            candidate,
            self.role_name
        )

        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            roles_path = directory_path / "roles.json"
            history_path = directory_path / "history.json"

            roles_path.write_text(
                json.dumps(
                    {
                        "Machine Learning Engineer": {
                            "description": "ML role",
                            "required": ["Python"],
                            "important": [],
                            "optional": []
                        }
                    }
                ),
                encoding="utf-8"
            )

            manager = DataManager(
                roles_path,
                history_path
            )

            manager.save_report(report)
            history = manager.load_history()

            self.assertEqual(len(history), 1)
            self.assertEqual(
                history[0]["candidate_name"],
                "Asha"
            )


if __name__ == "__main__":
    unittest.main()
