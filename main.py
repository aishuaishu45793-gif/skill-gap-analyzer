from pathlib import Path

from src.analyzer import SkillGapAnalyzer
from src.data_manager import DataManager, DataManagerError
from src.models import Candidate, SkillGapReport
from src.report_generator import ReportGenerator
from src.validator import (
    ValidationError,
    parse_skills,
    validate_candidate_name
)


BASE_DIRECTORY = Path(__file__).resolve().parent
ROLES_FILE = BASE_DIRECTORY / "data" / "roles.json"
HISTORY_FILE = BASE_DIRECTORY / "data" / "analysis_history.json"
REPORTS_DIRECTORY = BASE_DIRECTORY / "reports"


def print_header(title: str) -> None:
    width = 68
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def display_main_menu() -> None:
    print_header("SKILL GAP ANALYZER")
    print("1. Analyze candidate skills")
    print("2. View available roles")
    print("3. Search roles")
    print("4. View analysis history")
    print("5. Exit")


def display_roles(roles: dict) -> None:
    print_header("AVAILABLE ROLES")

    for index, role in enumerate(roles.values(), start=1):
        print(f"{index}. {role.name}")
        print(f"   {role.description}")


def select_role(
    analyzer: SkillGapAnalyzer
) -> str | None:
    role_names = list(analyzer.roles)

    print("\nSelect a target role:")

    for index, role_name in enumerate(role_names, start=1):
        print(f"{index}. {role_name}")

    choice = input(
        "\nEnter a role number or exact role name: "
    ).strip()

    if not choice:
        print("ERROR: Role selection cannot be empty.")
        return None

    if choice.isdigit():
        role_index = int(choice)

        if 1 <= role_index <= len(role_names):
            return role_names[role_index - 1]

        print(
            f"ERROR: Enter a number from 1 to {len(role_names)}."
        )
        return None

    role_lookup = {
        role.casefold(): role
        for role in role_names
    }

    exact_match = role_lookup.get(choice.casefold())

    if exact_match:
        return exact_match

    suggestions = analyzer.suggest_roles(choice)
    print(f"ERROR: Role '{choice}' was not found.")

    if suggestions:
        print("Did you mean:")

        for suggestion in suggestions:
            print(f"  - {suggestion}")

    return None


def analyze_candidate(
    analyzer: SkillGapAnalyzer,
    data_manager: DataManager
) -> None:
    print_header("NEW SKILL ANALYSIS")

    try:
        candidate_name = validate_candidate_name(
            input("Enter candidate name: ")
        )

        raw_skills = input(
            "Enter skills separated by commas:\n> "
        )

        candidate_skills = parse_skills(raw_skills)
        role_name = select_role(analyzer)

        if role_name is None:
            return

        candidate = Candidate(
            name=candidate_name,
            skills=candidate_skills
        )

        report = analyzer.analyze(candidate, role_name)

        print()
        print(ReportGenerator.create_text_report(report))

        try:
            data_manager.save_report(report)
            print("\nAnalysis saved to history.")
        except DataManagerError as error:
            print(f"\nWARNING: Analysis could not be saved: {error}")

        export_choice = input(
            "\nExport this analysis as a text report? (y/n): "
        ).strip().lower()

        if export_choice in {"y", "yes"}:
            try:
                report_path = ReportGenerator.export_text_report(
                    report,
                    REPORTS_DIRECTORY
                )
                print(f"Report exported to: {report_path}")
            except OSError as error:
                print(f"ERROR: {error}")

        gap_actions(analyzer, report)

    except ValidationError as error:
        print(f"ERROR: {error}")
    except ValueError as error:
        print(f"ERROR: {error}")


def gap_actions(
    analyzer: SkillGapAnalyzer,
    report: SkillGapReport
) -> None:
    while True:
        print("\nGap options:")
        print("1. Filter gaps by priority")
        print("2. Sort gaps alphabetically")
        print("3. Return to main menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            priority = input(
                "Enter HIGH, MEDIUM, or LOW: "
            ).strip()

            try:
                gaps = analyzer.filter_gaps(report, priority)
                print()
                print(ReportGenerator.format_gap_list(gaps))
            except ValueError as error:
                print(f"ERROR: {error}")

        elif choice == "2":
            gaps = analyzer.sort_gaps(
                report.missing_skills,
                "alphabetical"
            )
            print()
            print(ReportGenerator.format_gap_list(gaps))

        elif choice == "3":
            return

        else:
            print("ERROR: Please choose 1, 2, or 3.")


def search_roles(analyzer: SkillGapAnalyzer) -> None:
    print_header("SEARCH ROLES")

    keyword = input(
        "Enter a role, description, or skill keyword: "
    ).strip()

    if not keyword:
        print("ERROR: Search keyword cannot be empty.")
        return

    matches = analyzer.search_roles(keyword)

    if not matches:
        print(f"No roles matched '{keyword}'.")
        return

    print(f"\nFound {len(matches)} matching role(s):")

    for role in matches:
        print(f"\n- {role.name}")
        print(f"  {role.description}")
        print(f"  Skills: {', '.join(role.all_skills())}")


def view_history(data_manager: DataManager) -> None:
    print_header("ANALYSIS HISTORY")

    try:
        history = data_manager.load_history()
    except DataManagerError as error:
        print(f"ERROR: {error}")
        return

    if not history:
        print("No previous analyses were found.")
        return

    sorted_history = sorted(
        history,
        key=lambda item: item.get("generated_at", ""),
        reverse=True
    )

    for index, item in enumerate(sorted_history, start=1):
        candidate_name = item.get(
            "candidate_name",
            "Unknown candidate"
        )
        role_name = item.get(
            "role_name",
            "Unknown role"
        )
        percentage = item.get(
            "match_percentage",
            0
        )
        level = item.get(
            "match_level",
            "Unknown"
        )
        generated_at = item.get(
            "generated_at",
            "Unknown date"
        )

        print(
            f"{index}. {candidate_name} | {role_name} | "
            f"{percentage}% | {level} | {generated_at}"
        )


def run_application() -> None:
    data_manager = DataManager(
        roles_path=ROLES_FILE,
        history_path=HISTORY_FILE
    )

    try:
        roles = data_manager.load_roles()
    except DataManagerError as error:
        print(f"Application startup failed: {error}")
        return

    analyzer = SkillGapAnalyzer(roles)

    while True:
        display_main_menu()
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            analyze_candidate(analyzer, data_manager)

        elif choice == "2":
            display_roles(roles)

        elif choice == "3":
            search_roles(analyzer)

        elif choice == "4":
            view_history(data_manager)

        elif choice == "5":
            print("\nSkill Gap Analyzer closed.")
            break

        else:
            print("ERROR: Please choose a number from 1 to 5.")


if __name__ == "__main__":
    try:
        run_application()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted safely.")
