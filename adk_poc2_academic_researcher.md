# ADK PoC #2 — Academic Researcher Agent
> Este archivo es el inicializador del proyecto. Léelo completo antes de escribir una sola línea de código.

---

## Contexto del proyecto

Este es el segundo de una serie de 5 PoCs construidos con **Google ADK (Agent Development Kit)** en Python. El objetivo no es construir un chat, sino demostrar arquitecturas de agentes reales.

**Serie completa:**
1. ✅ Daily Brief + Research Prep *(Tool Use + Tool Chaining)*
2. 👉 **Academic Researcher** *(Multi-agent + Delegation)* ← este proyecto
3. Memory Agent *(State + Memory + Sessions)*
4. Content Pipeline *(Callbacks + Guardrails)*
5. Live API Agent *(Streaming + Live API)*

---

## Objetivo del PoC

Dado un tema técnico como input, un sistema de agentes lo investiga, sintetiza fuentes y detecta **contradicciones entre ellas**.

El foco está en la **arquitectura multi-agente**, no en el output final.

---

## ¿Qué hace el sistema?

```
INPUT: Un tema técnico (ej: "RAG vs Fine-tuning for domain-specific LLMs")

FLUJO:
1. RootAgent recibe el tema y orquesta
2. SearcherAgent    → busca 4-5 fuentes con Google Search
3. SynthesizerAgent → resume cada fuente por separado
4. CriticAgent      → compara las síntesis y detecta contradicciones
5. RootAgent        → consolida y genera reporte final

OUTPUT: research_TEMA.md con fuentes, síntesis y tensiones detectadas
```

---

## Arquitectura de agentes

```
RootAgent
├── SearcherAgent      (tool: Google Search)
├── SynthesizerAgent   (tool: ninguna, razona sobre texto)
└── CriticAgent        (tool: ninguna, compara síntesis)
```

### Responsabilidades

| Agente | Rol | Tools |
|---|---|---|
| `RootAgent` | Orquesta y consolida | Ninguna directa |
| `SearcherAgent` | Busca fuentes sobre el tema | `google_search` |
| `SynthesizerAgent` | Resume cada fuente individualmente | Ninguna |
| `CriticAgent` | Detecta contradicciones entre síntesis | Ninguna |

---

## Conceptos ADK que se practican

| Concepto | Dónde aparece |
|---|---|
| **Multi-agent architecture** | 4 agentes con roles distintos |
| **Agent delegation** | Root delega explícitamente a cada sub-agente |
| **Agent specialization** | Cada agente tiene 1 sola responsabilidad |
| **Result passing** | Output de Searcher → input de Synthesizer → input de Critic |
| **Root aggregation** | Root consolida los 3 outputs en 1 reporte |
| **Sequential orchestration** | Los agentes corren en secuencia, no en paralelo |

---

## Estructura de carpetas esperada

```
adk-poc2-academic-researcher/
├── main.py                  # Entry point — recibe el tema como argumento
├── agents/
│   ├── __init__.py
│   ├── root_agent.py        # RootAgent: orquesta el flujo completo
│   ├── searcher_agent.py    # SearcherAgent: busca fuentes
│   ├── synthesizer_agent.py # SynthesizerAgent: resume fuentes
│   └── critic_agent.py      # CriticAgent: detecta contradicciones
├── tools/
│   ├── __init__.py
│   └── search_tool.py       # Wrapper de Google Search para ADK
├── prompts/
│   ├── root_prompt.txt
│   ├── searcher_prompt.txt
│   ├── synthesizer_prompt.txt
│   └── critic_prompt.txt
├── outputs/                 # Aquí se guardan los reportes generados
├── .env.example
├── requirements.txt
└── README.md
```

---

## Cómo se ejecuta

```bash
# Instalar dependencias
pip install google-adk python-dotenv

# Configurar variables de entorno
cp .env.example .env
# Editar .env con GOOGLE_API_KEY y GOOGLE_SEARCH_API_KEY

# Ejecutar el agente con un tema
python main.py "RAG vs Fine-tuning for domain-specific LLMs"

# Output esperado en: outputs/research_RAG_vs_Fine-tuning.md
```

---

## Variables de entorno necesarias

```env
GOOGLE_API_KEY=your_gemini_api_key
GOOGLE_SEARCH_API_KEY=your_search_api_key
GOOGLE_SEARCH_ENGINE_ID=your_custom_search_engine_id
```

---

## Formato del output esperado

```markdown
# Research Report: [TEMA]
Generado: YYYY-MM-DD HH:MM

## Fuentes encontradas
1. [Título] — [URL]
2. ...

## Síntesis por fuente
### Fuente 1: [Título]
[Resumen de 3-5 oraciones]

### Fuente 2: ...

## Contradicciones detectadas
### Tensión 1: [Descripción]
- **Fuente A dice:** ...
- **Fuente B dice:** ...
- **Análisis:** ...

## Conclusión del CriticAgent
[Párrafo final con el estado del debate]
```

---

## Restricciones de scope (qué NO hacer)

- ❌ No construir UI ni chat interface
- ❌ No agregar memoria persistente (eso es el PoC #3)
- ❌ No correr agentes en paralelo (mantener flujo secuencial simple)
- ❌ No más de 4 agentes
- ✅ Foco en que la **delegación y el pasaje de resultados entre agentes** funcione correctamente

---

## Definition of Done

- [ ] Los 4 agentes existen como clases ADK separadas
- [ ] RootAgent puede delegar a cada sub-agente
- [ ] SearcherAgent retorna al menos 3 fuentes reales
- [ ] SynthesizerAgent genera un resumen por fuente
- [ ] CriticAgent detecta al menos 1 contradicción o tensión
- [ ] El output se guarda como archivo `.md` en `/outputs`
- [ ] Se puede ejecutar con `python main.py "TEMA"`

---

## Notas para Claude Code

- Usar `google-adk` como framework principal
- Gemini model: `gemini-2.0-flash` (balance costo/velocidad)
- Cada agente debe estar en su propio archivo dentro de `agents/`
- Los prompts van en archivos `.txt` en `prompts/` para facilitar iteración
- No hardcodear el tema — siempre leer desde `sys.argv[1]`
- Manejar errores de API con try/except y mensajes descriptivos
