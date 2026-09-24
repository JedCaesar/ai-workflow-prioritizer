"""Command-line interface for the AI Workflow Prioritizer."""

import argparse
import csv
import json
from pathlib import Path

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


def assessment_record(workflow: Workflow) -> dict[str, object]:
    """Return a serializable assessment for APIs and automation workflows."""

    result = assess_workflow(workflow)
    return {
        "workflow": workflow.name,
        "score": result.score,
        "recommendation": result.recommendation,
        "explanation": result.explanation,
    }


def show_json(workflows: tuple[Workflow, ...]) -> None:
    """Print one or more assessments as structured JSON."""

    records = [assessment_record(workflow) for workflow in workflows]
    output: object = records[0] if len(records) == 1 else records
    print(json.dumps(output, indent=2))


def load_workflows(path: str) -> tuple[Workflow, ...]:
    """Load workflow assessments from a CSV file."""

    required_columns = {
        "name",
        "frequency",
        "hours_per_week",
        "repetition",
        "data_readiness",
        "risk",
    }

    with Path(path).open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        missing = required_columns - set(reader.fieldnames or ())
        if missing:
            columns = ", ".join(sorted(missing))
            raise ValueError(f"CSV is missing required columns: {columns}")

        workflows = tuple(
            Workflow(
                name=row["name"].strip(),
                frequency=int(row["frequency"]),
                hours_per_week=float(row["hours_per_week"]),
                repetition=int(row["repetition"]),
                data_readiness=int(row["data_readiness"]),
                risk=int(row["risk"]),
            )
            for row in reader
        )

    if not workflows:
        raise ValueError("CSV must include at least one workflow")
    return workflows


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


def comparison_workflows() -> tuple[Workflow, ...]:
    """Return realistic examples with different levels of AI readiness."""

    return (
        demo_workflow(),
        Workflow(
            name="Extract data from supplier invoices",
            frequency=4,
            hours_per_week=12,
            repetition=5,
            data_readiness=3,
            risk=2,
        ),
        Workflow(
            name="Make final executive strategy decisions",
            frequency=2,
            hours_per_week=5,
            repetition=1,
            data_readiness=3,
            risk=5,
        ),
    )


def show_comparison(workflows: tuple[Workflow, ...]) -> None:
    """Rank workflows from strongest to weakest AI candidate."""

    ranked = sorted(
        ((workflow, assess_workflow(workflow)) for workflow in workflows),
        key=lambda item: item[1].score,
        reverse=True,
    )

    print("\nAI Workflow Comparison")
    print("=" * 78)
    print(f"{'Score':<8}{'Workflow':<48}Recommendation")
    print("-" * 78)
    for workflow, result in ranked:
        print(f"{result.score:<8}{workflow.name:<48}{result.recommendation}")
    print("=" * 78)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score a business workflow for AI automation readiness."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--demo", action="store_true", help="run with a sample customer-support workflow"
    )
    mode.add_argument(
        "--compare", action="store_true", help="rank several example workflows"
    )
    mode.add_argument(
        "--input", metavar="CSV_FILE", help="score workflows from a CSV file"
    )
    parser.add_argument(
        "--json", action="store_true", help="print machine-readable JSON output"
    )
    args = parser.parse_args()

    if args.input:
        workflows = load_workflows(args.input)
    elif args.compare:
        workflows = comparison_workflows()
    else:
        workflows = (demo_workflow() if args.demo else collect_workflow(),)

    if args.json:
        show_json(workflows)
        return

    if len(workflows) > 1:
        show_comparison(workflows)
    else:
        show_assessment(workflows[0])


if __name__ == "__main__":
    main()
