import re
from pathlib import Path

from src.models import SkillGap, SkillGapReport


class ReportGenerator:
    """Formats analysis results for display and export."""

    @staticmethod
    def _format_skill_list(
        title: str,
        skills: list[str],
        marker: str
    ) -> list[str]:
        lines = [title]

        if not skills:
            lines.append("  None")
            return lines

        for skill in skills:
            lines.append(f"  {marker} {skill}")

        return lines

    @staticmethod
    def format_gap_list(
        gaps: list[SkillGap]
    ) -> str:
        if not gaps:
            return "No missing skills found for this filter."

        lines = []

        for index, gap in enumerate(gaps, start=1):
            lines.append(
                f"{index}. [{gap.priority}] {gap.skill} "
                f"({gap.category.title()})"
            )

        return "\n".join(lines)

    @classmethod
    def create_text_report(
        cls,
        report: SkillGapReport
    ) -> str:
        width = 68
        border = "=" * width
        separator = "-" * width

        lines = [
            border,
            "SKILL GAP ANALYZER".center(width),
            border,
            f"Candidate: {report.candidate_name}",
            f"Target Role: {report.role_name}",
            f"Generated: {report.generated_at}",
            "",
            f"Weighted Skill Match: {report.match_percentage:.2f}%",
            f"Assessment: {report.match_level}",
            separator
        ]

        lines.extend(
            cls._format_skill_list(
                "Candidate Skills:",
                report.candidate_skills,
                "+"
            )
        )

        lines.append(separator)

        lines.extend(
            cls._format_skill_list(
                "Matched Role Skills:",
                report.matched_skills,
                "+"
            )
        )

        lines.append(separator)
        lines.append("Missing Skills by Priority:")

        if not report.missing_skills:
            lines.append("  No missing role skills.")
        else:
            for priority in ("HIGH", "MEDIUM", "LOW"):
                priority_gaps = [
                    gap
                    for gap in report.missing_skills
                    if gap.priority == priority
                ]

                lines.append(f"\n{priority}:")

                if priority_gaps:
                    for index, gap in enumerate(priority_gaps, start=1):
                        lines.append(
                            f"  {index}. {gap.skill} "
                            f"({gap.category.title()})"
                        )
                else:
                    lines.append("  None")

        lines.append("")
        lines.append(separator)

        lines.extend(
            cls._format_skill_list(
                "Additional Candidate Skills:",
                report.extra_skills,
                "+"
            )
        )

        lines.append(separator)

        high_priority = [
            gap.skill
            for gap in report.missing_skills
            if gap.priority == "HIGH"
        ]

        if high_priority:
            recommendation = ", ".join(high_priority[:3])
            lines.append(
                f"Recommendation: Focus first on {recommendation}."
            )
        elif report.missing_skills:
            recommendation = ", ".join(
                gap.skill for gap in report.missing_skills[:3]
            )
            lines.append(
                f"Recommendation: Continue with {recommendation}."
            )
        else:
            lines.append(
                "Recommendation: All listed role skills are covered."
            )

        lines.append(border)

        return "\n".join(lines)

    @classmethod
    def export_text_report(
        cls,
        report: SkillGapReport,
        reports_directory: str | Path
    ) -> Path:
        directory = Path(reports_directory)
        directory.mkdir(parents=True, exist_ok=True)

        safe_candidate_name = re.sub(
            r"[^a-zA-Z0-9_-]+",
            "_",
            report.candidate_name.strip()
        ).strip("_") or "candidate"

        timestamp = re.sub(
            r"[^0-9]",
            "",
            report.generated_at
        )

        output_path = directory / (
            f"{safe_candidate_name}_{timestamp}_skill_gap_report.txt"
        )

        try:
            output_path.write_text(
                cls.create_text_report(report),
                encoding="utf-8"
            )
        except OSError as error:
            raise OSError(
                f"Could not export report: {error}"
            ) from error

        return output_path
