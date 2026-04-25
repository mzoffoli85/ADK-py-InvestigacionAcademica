import pathlib
from google.adk.agents import Agent

_PROMPT = (pathlib.Path(__file__).parent.parent / "prompts" / "synthesizer_prompt.txt").read_text(encoding="utf-8")

synthesizer_agent = Agent(
    name="SynthesizerAgent",
    model="gemini-2.0-flash",
    description=(
        "Recibe una lista de fuentes y genera un resumen independiente de 3-5 oraciones "
        "para cada una. No compara fuentes entre sí. Devuelve un JSON con las síntesis."
    ),
    instruction=_PROMPT,
    tools=[],
)
