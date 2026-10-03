import json

from app.models import JobContext


def build_application_prompt(
    question: str,
    job: JobContext,
    candidate_profile: dict,
) -> str:

    profile_text = json.dumps(
        candidate_profile,
        indent=2,
    )

    job_text = json.dumps(
        job.model_dump(),
        indent=2,
    )

    return f"""
You are helping a software engineer write an answer to a job application question.

Write the answer as if the candidate personally typed it while applying for
the job. It should sound genuine, straightforward, and conversational while
remaining professional.

CANDIDATE PROFILE:
{profile_text}

JOB AND COMPANY CONTEXT:
{job_text}

APPLICATION QUESTION:
{question}

RULES:
1. Use ONLY facts supported by the candidate profile. Never invent experience,
   skills, employers, years of experience, achievements, or technologies.

2. The answer should primarily SELL THE CANDIDATE'S RELEVANT TECHNICAL
   BACKGROUND, not praise the company's mission.

3. Study the job requirements and identify the strongest overlaps with the
   candidate profile.

4. Prioritize the candidate's strengths in:
   - AI engineering and LLM systems
   - Python and backend engineering
   - REST API development
   - system design and scalable architectures
   - databases and backend infrastructure
   - AI agents, RAG and LLM-powered applications
   whenever they are relevant to the role.

5. If the job asks for something the candidate has actually worked with,
   mention that experience confidently.

6. If the candidate profile only indicates knowledge of something rather than
   practical experience, describe it as knowledge/familiarity. Never upgrade
   knowledge into professional experience.

7. Do NOT claim experience with a technology simply because it appears in the
   job description.

8. Pick 2-4 of the strongest technical overlaps instead of trying to mention
   every requirement.

9. The company context should normally take only a small part of the answer.
   Focus mainly on what the candidate can bring to the role.

10. Even for questions like "What interests you about working here?", connect
    the interest to the actual engineering work. For example, backend systems,
    APIs, scalability, AI, system design, or technical ownership.

11. Prefer concrete statements such as:
    "I've worked extensively with Python and FastAPI..."
    "I've built LLM-powered backend systems..."
    "I've worked on RAG, AI agents and API-based services..."
    over vague statements such as:
    "My experience aligns well with this opportunity."

12. Write confidently but do not exaggerate.

13. Keep the answer approximately 3-5 sentences.

14. Write in first person using simple, natural, professional language.

15. Avoid generic AI/corporate phrases such as:
    "aligns with my experience",
    "positions me to",
    "I am particularly drawn to",
    "leveraging my expertise",
    "perfect fit",
    "unique opportunity",
    "I am excited to contribute to your mission".

16. Do not simply repeat the job description.

17. Do not mention the candidate profile, job context, these instructions,
    or AI generation.

18. Return ONLY the final application answer.

Before writing, silently determine:
- What are the 3-5 most important technical requirements of this role?
- Which of those are genuinely supported by the candidate profile?
- What are the candidate's strongest technical selling points for this role?
- How can those strengths directly answer the application question?
""".strip()
