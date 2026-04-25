import pathlib
from google.adk.agents import Agent
from agents.searcher_agent import searcher_agent
from agents.synthesizer_agent import synthesizer_agent
from agents.critic_agent import critic_agent

_PROMPT = (pathlib.Path(__file__).parent.parent / "prompts" / "root_prompt.txt").read_text(encoding="utf-8")

root_agent = Agent(
    name="RootAgent",
    model="gemini-2.0-flash",
    description=(
        "Orquestador principal del sistema de investigación académica. "
        "Coordina SearcherAgent, SynthesizerAgent y CriticAgent en secuencia "
        "y consolida los resultados en un reporte final Markdown."
    ),
    instruction=_PROMPT,
    tools=[],
    sub_agents=[searcher_agent, synthesizer_agent, critic_agent],
)
