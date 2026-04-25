import pathlib
from google.adk.agents import Agent
from tools.search_tool import search_academic_sources

_PROMPT = (pathlib.Path(__file__).parent.parent / "prompts" / "searcher_prompt.txt").read_text(encoding="utf-8")

searcher_agent = Agent(
    name="SearcherAgent",
    model="gemini-2.0-flash",
    description=(
        "Busca 4-5 fuentes técnicas y académicas de alta calidad sobre un tema dado. "
        "Devuelve un JSON con título, URL y snippet de cada fuente."
    ),
    instruction=_PROMPT,
    tools=[search_academic_sources],
)
