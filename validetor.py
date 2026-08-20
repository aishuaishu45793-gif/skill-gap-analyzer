import re


class ValidationError(ValueError):
    """Raised when user input does not satisfy application rules."""


SKILL_ALIASES = {
    "js": "javascript",
    "javascript programming": "javascript",
    "ml": "machine learning",
    "machine-learning": "machine learning",
    "dl": "deep learning",
    "deep-learning": "deep learning",
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "scikit_learn": "scikit-learn",
    "numpy library": "numpy",
    "pandas library": "pandas",
    "oop": "object-oriented programming",
    "object oriented programming": "object-oriented programming",
    "object oriented": "object-oriented programming",
    "object-oriented": "object-oriented programming",
    "restful api": "rest api",
    "restful apis": "rest api",
    "apis": "rest api",
    "nlp": "natural language processing",
    "powerbi": "power bi",
    "power-bi": "power bi",
    "cicd": "ci/cd",
    "ci cd": "ci/cd",
    "continuous integration": "ci/cd",
    "k8s": "kubernetes",
    "amazon web services": "cloud computing",
    "aws": "cloud computing",
    "gcp": "cloud computing",
    "azure": "cloud computing",
    "version control": "git",
    "github": "git",
    "data structure": "data structures"
}


def validate_candidate_name(name: str) -> str:
    """Validate and return a cleaned candidate name."""

    if not isinstance(name, str):
        raise ValidationError("Candidate name must be text.")

    cleaned_name = " ".join(name.strip().split())

    if not cleaned_name:
        raise ValidationError("Candidate name cannot be empty.")

    if len(cleaned_name) > 80:
        raise ValidationError(
            "Candidate name cannot contain more than 80 characters."
        )

    return cleaned_name


def normalize_skill(skill: str) -> str:
    """Convert a skill into a consistent comparison format."""

    if not isinstance(skill, str):
        raise ValidationError("Every skill must be text.")

    normalized = skill.strip().lower()
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = normalized.strip(" ,;|")

    if not normalized:
        return ""

    return SKILL_ALIASES.get(normalized, normalized)


def parse_skills(raw_skills: str) -> list[str]:
    """Parse comma, semicolon, pipe, or newline-separated skills."""

    if not isinstance(raw_skills, str):
        raise ValidationError("Skills must be entered as text.")

    if not raw_skills.strip():
        raise ValidationError("Skill list cannot be empty.")

    parts = re.split(r"[,;\n|]+", raw_skills)
    normalized_skills = []

    for part in parts:
        normalized = normalize_skill(part)
        if normalized and normalized not in normalized_skills:
            normalized_skills.append(normalized)

    if not normalized_skills:
        raise ValidationError("Please enter at least one valid skill.")

    if len(normalized_skills) > 100:
        raise ValidationError("A maximum of 100 skills is allowed.")

    return normalized_skills


def validate_role_name(role_name: str, available_roles: list[str]) -> str:
    """Return the correctly cased role name or raise an error."""

    if not isinstance(role_name, str) or not role_name.strip():
        raise ValidationError("Role name cannot be empty.")

    lookup = {
        role.casefold(): role
        for role in available_roles
    }

    matched_role = lookup.get(role_name.strip().casefold())

    if matched_role is None:
        raise ValidationError(f"Unknown role: {role_name.strip()}")

    return matched_role
