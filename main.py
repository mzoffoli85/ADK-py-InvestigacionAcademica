import asyncio
import sys
import os
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

load_dotenv()


def _topic_to_filename(topic: str) -> str:
    """Convert a topic string to a safe filename slug."""
    slug = re.sub(r"[^\w\s-]", "", topic)
    slug = re.sub(r"[\s]+", "_", slug.strip())
    return f"research_{slug[:80]}.md"


async def run_research(topic: str) -> str:
    from agents.root_agent import root_agent

    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="academic_researcher",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="academic_researcher",
        user_id="researcher",
    )

    message = Content(role="user", parts=[Part(text=topic)])

    final_response = ""
    async for event in runner.run_async(
        user_id="researcher",
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text

    return final_response


def save_report(topic: str, content: str) -> Path:
    outputs_dir = Path(__file__).parent / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    filepath = outputs_dir / _topic_to_filename(topic)
    filepath.write_text(content, encoding="utf-8")
    return filepath


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python main.py \"<tema a investigar>\"")
        print("Ejemplo: python main.py \"RAG vs Fine-tuning for domain-specific LLMs\"")
        sys.exit(1)

    topic = sys.argv[1].strip()
    if not topic:
        print("Error: el tema no puede estar vacío.")
        sys.exit(1)

    required_vars = ["GOOGLE_API_KEY", "GOOGLE_SEARCH_API_KEY", "GOOGLE_SEARCH_ENGINE_ID"]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        print(f"Error: faltan variables de entorno: {', '.join(missing)}")
        print("Copia .env.example a .env y completa los valores.")
        sys.exit(1)

    print(f"Iniciando investigación sobre: {topic}")
    print("Esto puede tardar unos minutos...\n")

    try:
        report = asyncio.run(run_research(topic))
    except KeyboardInterrupt:
        print("\nInvestigación cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"Error durante la investigación: {e}")
        sys.exit(1)

    if not report:
        print("Error: el agente no produjo ningún output.")
        sys.exit(1)

    filepath = save_report(topic, report)
    print(f"\nReporte guardado en: {filepath}")
    print("-" * 60)
    print(report)


if __name__ == "__main__":
    main()
