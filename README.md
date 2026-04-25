# ADK PoC #2 — Academic Researcher Agent

Sistema multi-agente construido con **Google ADK** que investiga un tema técnico, sintetiza fuentes y detecta contradicciones entre ellas.

## Arquitectura

```
RootAgent
├── SearcherAgent      → busca 4-5 fuentes con Google Custom Search
├── SynthesizerAgent   → resume cada fuente por separado
└── CriticAgent        → detecta contradicciones entre síntesis
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tus API keys
```

Variables necesarias en `.env`:

| Variable | Descripción |
|---|---|
| `GOOGLE_API_KEY` | Gemini API key (Google AI Studio) |
| `GOOGLE_SEARCH_API_KEY` | Google Custom Search API key |
| `GOOGLE_SEARCH_ENGINE_ID` | ID del Custom Search Engine (cx) |

## Uso

```bash
python main.py "RAG vs Fine-tuning for domain-specific LLMs"
```

El reporte se guarda en `outputs/research_<tema>.md`.

## Estructura

```
.
├── main.py                  # Entry point
├── agents/
│   ├── root_agent.py        # Orquestador
│   ├── searcher_agent.py    # Búsqueda de fuentes
│   ├── synthesizer_agent.py # Síntesis por fuente
│   └── critic_agent.py      # Detección de contradicciones
├── tools/
│   └── search_tool.py       # Google Custom Search wrapper
├── prompts/                 # Instrucciones de cada agente (editables)
└── outputs/                 # Reportes generados
```

## Conceptos ADK practicados

- Multi-agent architecture con 4 agentes especializados
- Agent delegation desde RootAgent a sub-agentes
- Sequential orchestration con pasaje de resultados entre agentes
- Agent specialization (1 responsabilidad por agente)
