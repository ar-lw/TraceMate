
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from google.genai import errors
from pydantic import BaseModel, Field

from tracemate.config import get_settings
from tracemate.providers.factory import (
    get_embedding_provider,
    get_llm_provider,
)
from tracemate.rag.qa import TraceMateRAG
from tracemate.rag.vector_store import VectorStore


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="TraceMate API",
    description="Java DSA learning assistant powered by RAG",
    version="0.2.0",
)


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    mode: str = "explain"
    code: str = ""
    hint_level: int = Field(default=1, ge=1, le=5)


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


def create_assistant() -> TraceMateRAG:
    project_root = Path(__file__).resolve().parents[2]
    persist_directory = project_root / "data" / "chroma"

    settings = get_settings()

    llm_provider = get_llm_provider(settings)
    embedding_provider = get_embedding_provider(settings)

    vector_store = VectorStore(
        embedding_provider=embedding_provider,
        persist_directory=str(persist_directory),
    )

    return TraceMateRAG(
        llm_provider=llm_provider,
        vector_store=vector_store,
    )


assistant = create_assistant()


@app.get("/health")
def health_check():
    try:
        chunk_count = assistant.vector_store.collection.count()

        return {
            "status": "healthy" if chunk_count > 0 else "degraded",
            "app": "TraceMate",
            "knowledge_chunks": chunk_count,
        }

    except Exception:
        logger.exception("Health check failed")
        raise HTTPException(
            status_code=503,
            detail="Knowledge store is unavailable.",
        )
@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    try:
        return assistant.answer_question(
            question=request.question,
            mode=request.mode,
            code=request.code,
            hint_level=request.hint_level,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except errors.ServerError:
        logger.exception("Gemini service is temporarily unavailable")
        raise HTTPException(
            status_code=503,
            detail=(
                "The AI service is temporarily unavailable. "
                "Please try again shortly."
            ),
        )

    except Exception:
        logger.exception("TraceMate API request failed")
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your request.",
        )
