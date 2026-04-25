# ADK PoC #2 — Academic Researcher Agent · Registro de cambios

> Este archivo documenta las modificaciones realizadas respecto al diseño inicial (`adk_poc2_academic_researcher.md`).  
> El archivo original se conserva sin cambios como referencia del diseño base.

---

## Resumen ejecutivo de cambios

| Aspecto | Diseño inicial | Estado actual |
|---|---|---|
| Modelo de IA | `gemini-2.0-flash` (Google Gemini) | `deepseek-chat` (DeepSeek) via LiteLlm |
| Integración modelo | String directo en ADK | `LiteLlm` wrapper de ADK |
| Variable de IA | `GOOGLE_API_KEY` | `DEEPSEEK_API_KEY` |
| Búsqueda web | Google Custom Search API | DuckDuckGo (sin API key) |
| Variables de búsqueda | `GOOGLE_SEARCH_API_KEY`, `GOOGLE_SEARCH_ENGINE_ID` | Eliminadas — sin configuración necesaria |
| Dependencias | `google-adk`, `python-dotenv`, `requests` | `+litellm`, `+duckduckgo-search`, `-requests` |
| `.gitignore` | No existía | Creado |
| Patrón multi-agente | `sub_agents` (transfer_to_agent) | `AgentTool` (agent-as-tool) |

---

## Cambio 1 — Modelo de IA: Gemini → DeepSeek

### Motivación
Se decidió no utilizar Google como proveedor de IA. El modelo `gemini-2.0-flash` fue reemplazado por `deepseek-chat` de DeepSeek.

### Mecanismo de integración
Google ADK soporta modelos externos a través de su integración con **LiteLlm**. Esto permite usar cualquier modelo compatible con LiteLlm sin cambiar la arquitectura de agentes.

```python
# Antes (diseño inicial)
from google.adk.agents import Agent

agent = Agent(
    model="gemini-2.0-flash",
    ...
)

# Ahora
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

_MODEL = LiteLlm(model="deepseek/deepseek-chat")

agent = Agent(
    model=_MODEL,
    ...
)
```

### Archivos modificados
- [agents/root_agent.py](agents/root_agent.py)
- [agents/searcher_agent.py](agents/searcher_agent.py)
- [agents/synthesizer_agent.py](agents/synthesizer_agent.py)
- [agents/critic_agent.py](agents/critic_agent.py)

### Patrón aplicado (igual en los 4 agentes)
```python
from google.adk.models.lite_llm import LiteLlm

_MODEL = LiteLlm(model="deepseek/deepseek-chat")
```
La instancia `_MODEL` se define a nivel de módulo y se pasa al constructor del agente. El parámetro `DEEPSEEK_API_KEY` es reconocido automáticamente por LiteLlm desde el entorno.

---

## Cambio 2 — Variables de entorno

### Antes
```env
GOOGLE_API_KEY=...          # Gemini
GOOGLE_SEARCH_API_KEY=...   # Google Custom Search
GOOGLE_SEARCH_ENGINE_ID=... # Google Custom Search
```

### Ahora
```env
DEEPSEEK_API_KEY=...        # DeepSeek (reemplaza GOOGLE_API_KEY)
GOOGLE_SEARCH_API_KEY=...   # Google Custom Search (sin cambio — es búsqueda, no IA)
GOOGLE_SEARCH_ENGINE_ID=... # Google Custom Search (sin cambio)
```

**Nota:** `GOOGLE_SEARCH_API_KEY` y `GOOGLE_SEARCH_ENGINE_ID` se conservan porque el componente de búsqueda web (Google Custom Search REST API) es independiente del proveedor de IA. Es un servicio de indexación, no un modelo de lenguaje.

### Archivos modificados
- [.env.example](.env.example)

---

## Cambio 3 — Dependencias

Se agregó `litellm` como dependencia requerida para la integración de DeepSeek con ADK.

```txt
# requirements.txt
google-adk>=0.4.0
litellm>=1.40.0        # ← nueva
python-dotenv>=1.0.0
requests>=2.31.0
```

### Archivo modificado
- [requirements.txt](requirements.txt)

---

## Cambio 4 — .gitignore (nuevo archivo)

Se creó [.gitignore](.gitignore) para proteger el archivo `.env` (que contiene API keys) y excluir artefactos de Python y los reportes generados localmente.

Entradas clave:
```gitignore
.env          # API keys — nunca commitear
outputs/*.md  # Reportes generados localmente
__pycache__/
.venv/
```

---

## Cambio 5 — Búsqueda web: Google Custom Search → DuckDuckGo

### Motivación
Google Custom Search requiere registro, creación de un Search Engine y dos API keys. DuckDuckGo no requiere ninguna configuración y es gratuito.

### Implementación
Se usa la librería `duckduckgo-search` (`DDGS`). La interfaz de la función `search_academic_sources` no cambió — los agentes no notan la diferencia.

```python
# tools/search_tool.py
from duckduckgo_search import DDGS

def search_academic_sources(query: str) -> dict:
    with DDGS() as ddgs:
        hits = list(ddgs.text(query, max_results=5))
    results = [{"title": h["title"], "url": h["href"], "snippet": h["body"]} for h in hits]
    return {"results": results, "count": len(results)}
```

### Variables eliminadas
- `GOOGLE_SEARCH_API_KEY`
- `GOOGLE_SEARCH_ENGINE_ID`

El `.env` ahora solo necesita `DEEPSEEK_API_KEY`.

### Archivos modificados
- [tools/search_tool.py](tools/search_tool.py)
- [requirements.txt](requirements.txt) — `duckduckgo-search>=6.0.0`, eliminado `requests`
- [.env.example](.env.example) — solo `DEEPSEEK_API_KEY`
- [main.py](main.py) — validación de env vars simplificada

---

## Cambio 6 — Patrón multi-agente: `sub_agents` → `AgentTool`

### Problema detectado
Con el patrón `sub_agents`, ADK usa `transfer_to_agent` para delegar: el `RootAgent` cede el control **completamente** al sub-agente y ese sub-agente responde como respuesta final. El flujo nunca retorna al root para continuar con los pasos siguientes. El reporte generado solo contenía el output del `SearcherAgent`.

### Solución aplicada
Se reemplazó `sub_agents=[...]` por `AgentTool` en el `RootAgent`. Con este patrón, cada sub-agente funciona como una **herramienta**: el root llama al agente, recibe el resultado como respuesta de tool, y continúa con el siguiente paso.

```python
# Antes — root pierde el control al primer transfer
root_agent = Agent(
    ...
    sub_agents=[searcher_agent, synthesizer_agent, critic_agent],
)

# Ahora — root mantiene el control en todo momento
from google.adk.tools.agent_tool import AgentTool

root_agent = Agent(
    ...
    tools=[
        AgentTool(agent=searcher_agent),
        AgentTool(agent=synthesizer_agent),
        AgentTool(agent=critic_agent),
    ],
)
```

### Impacto
- El `RootAgent` ahora ejecuta el flujo completo: busca → sintetiza → critica → consolida.
- El reporte incluye las 4 secciones: fuentes, síntesis, contradicciones y conclusión.
- `root_prompt.txt` actualizado para reflejar que los sub-agentes son herramientas, no transfers.

### Archivos modificados
- [agents/root_agent.py](agents/root_agent.py)
- [prompts/root_prompt.txt](prompts/root_prompt.txt)

---

## Decisiones de diseño que NO cambiaron

- Arquitectura de 4 agentes (`RootAgent`, `SearcherAgent`, `SynthesizerAgent`, `CriticAgent`)
- Orquestación secuencial (no paralela)
- Prompts en archivos `.txt` separados en `prompts/`
- Herramienta de búsqueda: Google Custom Search via `tools/search_tool.py`
- Entry point: `python main.py "<tema>"`
- Formato del reporte: `outputs/research_<tema>.md`
- Formato de respuesta entre agentes: JSON estructurado

---

## Modelo DeepSeek — referencia rápida

| Modelo | String LiteLlm | Uso recomendado |
|---|---|---|
| DeepSeek-V3 (chat) | `deepseek/deepseek-chat` | Orquestación, síntesis, crítica ← **el que usamos** |
| DeepSeek-R1 (razonamiento) | `deepseek/deepseek-reasoner` | Tareas que requieren cadena de razonamiento larga |

La variable de entorno `DEEPSEEK_API_KEY` es detectada automáticamente por LiteLlm; no requiere configuración adicional en el código.

---

## Estado del Definition of Done

| Criterio | Estado |
|---|---|
| Los 4 agentes existen como clases ADK separadas | ✅ |
| RootAgent puede delegar a cada sub-agente | ✅ |
| SearcherAgent usa Google Custom Search | ✅ |
| SynthesizerAgent genera un resumen por fuente | ✅ |
| CriticAgent detecta contradicciones | ✅ |
| El output se guarda como `.md` en `/outputs` | ✅ |
| Se ejecuta con `python main.py "TEMA"` | ✅ |
| Modelo de IA: DeepSeek (no Gemini) | ✅ |
| `.gitignore` con `.env` protegido | ✅ |
