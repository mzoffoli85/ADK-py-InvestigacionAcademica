import pathlib
from google.adk.agents import Agent

_PROMPT = (pathlib.Path(__file__).parent.parent / "prompts" / "critic_prompt.txt").read_text(encoding="utf-8")

critic_agent = Agent(
    name="CriticAgent",
    model="gemini-2.0-flash",
    description=(
        "Recibe las síntesis de múltiples fuentes y detecta contradicciones, tensiones "
        "y desacuerdos entre ellas. Devuelve un JSON con las contradicciones y una conclusión."
    ),
    instruction=_PROMPT,
    tools=[],
)
