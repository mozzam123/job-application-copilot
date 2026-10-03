from pydantic import BaseModel


class JobContext(BaseModel):
    company_name: str | None = None
    job_title: str | None = None
    company_description: str | None = None
    job_description: str | None = None
    requirements: str | None = None
    source_url: str | None = None


class GenerateAnswerRequest(BaseModel):
    question: str
    job: JobContext


class GenerateAnswerResponse(BaseModel):
    answer: str
