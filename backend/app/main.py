from fastapi import FastAPI, HTTPException

from app.candidate_profile import CANDIDATE_PROFILE
from app.llm.ollama import OllamaProvider
from app.models import (
    GenerateAnswerRequest,
    GenerateAnswerResponse,
)
from app.prompt_builder import build_application_prompt


app = FastAPI(title="Job Application Copilot API")


llm = OllamaProvider(model="qwen3:8b")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post(
    "/generate",
    response_model=GenerateAnswerResponse,
)
def generate_answer(
    request: GenerateAnswerRequest,
):

    prompt = build_application_prompt(
        question=request.question,
        job=request.job,
        candidate_profile=CANDIDATE_PROFILE,
    )

    try:
        answer = llm.generate(prompt)

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"LLM generation failed: {exc}",
        )

    return GenerateAnswerResponse(answer=answer)
