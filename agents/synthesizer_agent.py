import pathlib
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

_PROMPT = (pathlib.Path(__file__).parent.parent / "prompts" / "synthesizer_prompt.txt").read_text(encoding="utf-8")
_MODEL = LiteLlm(model="deepseek/deepseek-chat")

synthesizer_agent = Agent(
    name="SynthesizerAgent",
    model=_MODEL,
    description=(
        "Recibe una lista de fuentes y genera un resumen independiente de 3-5 oraciones "
        "para cada una. No compara fuentes entre sí. Devuelve un JSON con las síntesis."
    ),
    instruction=_PROMPT,
    tools=[],
)
