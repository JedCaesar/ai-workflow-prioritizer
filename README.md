# AI Workflow Prioritizer

A beginner-friendly Python tool that helps teams decide which business workflows are good candidates for AI automation.

It turns five practical questions into a readiness score and a clear next step. The project uses only the Python standard library, so there are no packages or API keys to install.

## What it evaluates

- How often the workflow happens
- How much time it consumes
- How repetitive and rule-based it is
- Whether the required data is ready
- How risky an incorrect result would be

## Quick start

You need Python 3.10 or newer.

```bash
git clone https://github.com/JedCaesar/ai-workflow-prioritizer.git
cd ai-workflow-prioritizer
python app.py
```

Run the included example:

```bash
python app.py --demo
```

Example output:

```text
Classify and route customer support requests
AI readiness score: 74/100
Recommendation: Strong candidate
Start with a small pilot and measure time saved, quality, and adoption.
```

## How the score works

The score rewards frequent, time-consuming, repetitive workflows with accessible data. Risk acts as a penalty because high-impact decisions need stronger safeguards and human review.

This is a prioritization aid, not a guarantee that AI is the right solution. Always consider privacy, security, cost, and the people affected by the workflow.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Ideas for beginners

- Export the result to a JSON or CSV file
- Score several workflows and rank them
- Add a simple web interface with Flask or Streamlit
- Store previous assessments in SQLite
- Draw a chart of the strongest candidates

## Project structure

```text
ai-workflow-prioritizer/
|-- app.py
|-- workflow_scorer.py
|-- tests/
|   `-- test_workflow_scorer.py
|-- LICENSE
`-- README.md
```

## License

MIT
