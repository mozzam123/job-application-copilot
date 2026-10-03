from fastapi import FastAPI

from app.models import (
    GenerateAnswerRequest,
    GenerateAnswerResponse,
)

from app.candidate_profile import CANDIDATE_PROFILE


app = FastAPI(title="Job Application Copilot API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateAnswerResponse)
def generate_answer(request: GenerateAnswerRequest):

    print("\n--- APPLICATION QUESTION ---")
    print(request.question)

    print("\n--- JOB CONTEXT ---")
    print(request.job.model_dump())

    print("\n--- CANDIDATE PROFILE ---")
    print(CANDIDATE_PROFILE)

    return GenerateAnswerResponse(
        answer="Backend received the job context successfully."
    )
