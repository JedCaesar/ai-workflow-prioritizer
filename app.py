"""Command-line interface for the AI Workflow Prioritizer."""

import argparse

from workflow_scorer import Workflow, assess_workflow


def ask_rating(prompt: str) -> int:
    """Ask for a rating until the user enters a number from 1 to 5."""

    while True:
        try:
            value = int(input(f"{prompt} (1-5): "))
            if 1 <= value <= 5:
                return value
        except ValueError:
            pass
        print("Please enter a whole number from 1 to 5.")


def collect_workflow() -> Workflow:
    """Collect workflow details from the terminal."""

    print("\nAI Workflow Prioritizer")
    print("Score a task to see whether it is ready for an AI pilot.\n")

    name = input("Workflow name: ").strip() or "Untitled workflow"

    while True:
        try:
            hours = float(input("Hours spent on it each week: "))
            if hours >= 0:
                break
        except ValueError:
            pass
        print("Please enter zero or a positive number.")

    return Workflow(
        name=name,
        frequency=ask_rating("How frequently does it happen?"),
        hours_per_week=hours,
        repetition=ask_rating("How repetitive and rule-based is it?"),
        data_readiness=ask_rating("How organized and accessible is the data?"),
        risk=ask_rating("How serious would an incorrect result be?"),
    )


def show_assessment(workflow: Workflow) -> None:
    """Print a clear assessment for one workflow."""

    result = assess_workflow(workflow)
    print("\n" + "=" * 48)
    print(workflow.name)
    print(f"AI readiness score: {result.score}/100")
    print(f"Recommendation: {result.recommendation}")
    print(result.explanation)
    print("=" * 48)


def demo_workflow() -> Workflow:
    """Return an example that can be run without answering prompts."""

    return Workflow(
        name="Classify and route customer support requests",
        frequency=5,
        hours_per_week=18,
        repetition=4,
        data_readiness=4,
        risk=2,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score a business workflow for AI automation readiness."
    )
    parser.add_argument(
        "--demo", action="store_true", help="run with a sample customer-support workflow"
    )
    args = parser.parse_args()
    show_assessment(demo_workflow() if args.demo else collect_workflow())


if __name__ == "__main__":
    main()
