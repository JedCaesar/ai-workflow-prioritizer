"""Scoring logic for the AI Workflow Prioritizer."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Workflow:
    """A business workflow that may benefit from AI or automation."""

    name: str
    frequency: int
    hours_per_week: float
    repetition: int
    data_readiness: int
    risk: int


@dataclass(frozen=True)
class Assessment:
    """The score and recommendation produced for a workflow."""

    score: int
    recommendation: str
    explanation: str


def _validate_rating(name: str, value: int) -> None:
    if not 1 <= value <= 5:
        raise ValueError(f"{name} must be between 1 and 5")


def assess_workflow(workflow: Workflow) -> Assessment:
    """Return an AI-readiness assessment on a 0 to 100 scale."""

    _validate_rating("frequency", workflow.frequency)
    _validate_rating("repetition", workflow.repetition)
    _validate_rating("data_readiness", workflow.data_readiness)
    _validate_rating("risk", workflow.risk)

    if workflow.hours_per_week < 0:
        raise ValueError("hours_per_week cannot be negative")

    time_score = min(workflow.hours_per_week / 20, 1) * 25
    frequency_score = workflow.frequency / 5 * 20
    repetition_score = workflow.repetition / 5 * 25
    data_score = workflow.data_readiness / 5 * 20
    risk_penalty = (workflow.risk - 1) / 4 * 20

    score = round(
        max(0, min(100, time_score + frequency_score + repetition_score + data_score - risk_penalty))
    )

    if score >= 70:
        recommendation = "Strong candidate"
        explanation = "Start with a small pilot and measure time saved, quality, and adoption."
    elif score >= 45:
        recommendation = "Promising with human review"
        explanation = "Test one step first and keep a person responsible for final decisions."
    else:
        recommendation = "Prepare the foundations"
        explanation = "Improve the data or simplify the process before adding AI."

    return Assessment(score, recommendation, explanation)
