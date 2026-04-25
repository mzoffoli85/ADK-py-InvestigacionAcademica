import pathlib
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

_PROMPT = (pathlib.Path(__file__).parent.parent / "prompts" / "critic_prompt.txt").read_text(encoding="utf-8")
_MODEL = LiteLlm(model="deepseek/deepseek-chat")

critic_agent = Agent(
    name="CriticAgent",
    model=_MODEL,
    description=(
        "Recibe las síntesis de múltiples fuentes y detecta contradicciones, tensiones "
        "y desacuerdos entre ellas. Devuelve un JSON con las contradicciones y una conclusión."
    ),
    instruction=_PROMPT,
    tools=[],
)
