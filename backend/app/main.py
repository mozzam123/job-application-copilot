from fastapi import FastAPI, HTTPException

from app.candidate_profile import CANDIDATE_PROFILE
from app.knowledge.project_index import ProjectIndex
from app.llm.ollama import OllamaProvider
from app.models import (
    GenerateAnswerRequest,
    GenerateAnswerResponse,
)
from app.prompt_builder import build_application_prompt


app = FastAPI(title="Job Application Copilot API")


llm = OllamaProvider(model="qwen3:8b")


project_index = ProjectIndex()


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

    # Build a retrieval query from the technical
    # parts of the job description.
    retrieval_query = f"""
Job Title:
{request.job.job_title or ""}

Job Description:
{request.job.job_description or ""}

Requirements:
{request.job.requirements or ""}
""".strip()

    try:

        relevant_projects = project_index.search(
            retrieval_query,
            top_k=3,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Project retrieval failed: {exc}",
        )

    print("\nRelevant GitHub Projects:")

    for project in relevant_projects:
        print(f"- {project['repository']} " f"({project['score']:.3f})")

    print()

    prompt = build_application_prompt(
        question=request.question,
        job=request.job,
        candidate_profile=CANDIDATE_PROFILE,
        relevant_projects=relevant_projects,
    )

    try:

        answer = llm.generate(prompt)

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=f"LLM generation failed: {exc}",
        )

    return GenerateAnswerResponse(answer=answer)
