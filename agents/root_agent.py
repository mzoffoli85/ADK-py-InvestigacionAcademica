import pathlib
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from agents.searcher_agent import searcher_agent
from agents.synthesizer_agent import synthesizer_agent
from agents.critic_agent import critic_agent

_PROMPT = (pathlib.Path(__file__).parent.parent / "prompts" / "root_prompt.txt").read_text(encoding="utf-8")
_MODEL = LiteLlm(model="deepseek/deepseek-chat")

root_agent = Agent(
    name="RootAgent",
    model=_MODEL,
    description=(
        """
        Orquestador principal del sistema de investigación académica.
        Coordina SearcherAgent, SynthesizerAgent y CriticAgent en secuencia
        y consolida los resultados en un reporte final Markdown.
        """    
    ),
    instruction=_PROMPT,
    tools=[
        AgentTool(agent=searcher_agent),
        AgentTool(agent=synthesizer_agent),
        AgentTool(agent=critic_agent),
    ],
)
