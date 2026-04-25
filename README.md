# ADK PoC #2 — Academic Researcher Agent

Sistema multi-agente construido con **Google ADK** que investiga un tema técnico, sintetiza fuentes y detecta contradicciones entre ellas.

> **Modelo de IA:** DeepSeek (`deepseek-chat`) via LiteLlm  
> **Búsqueda web:** DuckDuckGo (sin API key, gratuito)

## Arquitectura

```
RootAgent  [DeepSeek]
├── SearcherAgent      [DeepSeek] → busca 4-5 fuentes con DuckDuckGo
├── SynthesizerAgent   [DeepSeek] → resume cada fuente por separado
└── CriticAgent        [DeepSeek] → detecta contradicciones entre síntesis
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Agregar solo DEEPSEEK_API_KEY
```

Variables necesarias en `.env`:

| Variable | Descripción |
|---|---|
| `DEEPSEEK_API_KEY` | API key de DeepSeek (platform.deepseek.com) |

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
│   └── search_tool.py       # DuckDuckGo wrapper
├── prompts/                 # Instrucciones de cada agente (editables)
└── outputs/                 # Reportes generados (ignorados por git)
```

## Conceptos ADK practicados

- Multi-agent architecture con 4 agentes especializados
- Agent delegation desde RootAgent a sub-agentes
- Sequential orchestration con pasaje de resultados entre agentes
- Agent specialization (1 responsabilidad por agente)
- Custom LLM backend via `LiteLlm` (integración con modelos no-Gemini)

<img width="1790" height="854" alt="image" src="https://github.com/user-attachments/assets/dcb0593a-d6bc-403a-8302-edac113adb94" />
