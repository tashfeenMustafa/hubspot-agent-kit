# Contributing to HubSpot Agent Kit

We welcome contributions to the HubSpot Agent Kit! Please read through these guidelines to ensure a smooth contribution process.

## How to Add a New Audit Rule

To add a new audit rule:

1.  **Create a new rule file**: In the `rules/` directory, create a new Markdown file named `wfXXX.md` (e.g., `wf001.md`), where `XXX` is a unique three-digit identifier.
2.  **Implement detection logic**: In the `scripts/audit/rules/` directory, add a Python function `detect()` within a new or existing module that implements the logic for detecting this rule.
3.  **Add to INDEX.md**: Update the `rules/INDEX.md` file to include your new rule and its description.

## How to Add a New Skill

To add a new skill:

1.  **Create a skill directory**: In the `skills/` directory, create a new sub-directory named after your skill (e.g., `skills/my-new-skill/`).
2.  **Create SKILL.md**: Inside your new skill directory, create a `SKILL.md` file that describes the skill, its purpose, parameters, and usage, following the existing `SKILL.md` templates.
3.  **Implement skill logic**: Add any necessary Python scripts or other files within the skill directory to implement the skill's functionality.

## Pull Request Requirements

When submitting a pull request, please ensure the following:

*   **Test against a dev HubSpot portal**: All new features or changes should be tested against a development HubSpot portal to ensure functionality and prevent unintended side effects.
*   **No hardcoded IDs**: Avoid hardcoding any HubSpot object IDs (e.g., workflow IDs, property IDs) directly in the code. Use configuration or dynamic retrieval where possible.
*   **No real API keys**: Never commit real HubSpot API keys or sensitive credentials. Use environment variables or placeholder values for examples.
