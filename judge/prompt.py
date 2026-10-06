"""The fixed judge prompt. Same model, prompt and rubric for every memory condition."""
from pathlib import Path

SYSTEM = """You are an AI teammate in a company chat workspace. After each message, decide
whether to act. Follow this rubric exactly:

{RUBRIC}

Respond with ONLY JSON:
{"label": "IGNORE" | "TRACK" | "INTERVENE", "severity": 1 | 2 | 3,
 "cited_value": "<the specific fact you are acting on, or empty>", "reason": "<one sentence>"}"""

USER = """Today is {TODAY}.

Your memory of the workspace (retrieved; may be incomplete):
{MEMORY}

Recent messages in {CHANNEL} (most recent last):
{WINDOW}

What do you do after the last message?"""


def system_prompt() -> str:
    return SYSTEM.replace("{RUBRIC}", Path("rubric.md").read_text())


def user_prompt(today: str, memory: str, channel: str, window: str) -> str:
    return (USER.replace("{TODAY}", today).replace("{MEMORY}", memory or "(none)")
            .replace("{CHANNEL}", channel).replace("{WINDOW}", window))
