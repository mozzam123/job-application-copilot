import json

from app.models import JobContext


def build_application_prompt(
    question: str,
    job: JobContext,
    candidate_profile: dict,
    relevant_projects: list[dict],
) -> str:

    profile_text = json.dumps(
        candidate_profile,
        indent=2,
    )

    job_text = json.dumps(
        job.model_dump(),
        indent=2,
    )

    project_evidence = []

    for project in relevant_projects:
        project_evidence.append(
            {
                "repository": project["repository"],
                "url": project["url"],
                "content": project["content"],
            }
        )

    projects_text = json.dumps(
        project_evidence,
        indent=2,
    )

    return f"""
You are helping a software engineer write an answer to a job application question.

Write the answer as if the candidate personally typed it while applying for
the job. The answer should primarily demonstrate why the candidate's actual
technical background is relevant to this specific role.

CANDIDATE PROFILE:
{profile_text}

RELEVANT GITHUB PROJECT EVIDENCE:
{projects_text}

JOB AND COMPANY CONTEXT:
{job_text}

APPLICATION QUESTION:
{question}

RULES:

1. Use ONLY facts supported by the candidate profile or GitHub project
   evidence.

2. Never invent experience, technologies, employers, years of experience,
   achievements, metrics, or responsibilities.

3. Treat GitHub projects as hands-on project experience, NOT professional
   employment experience.

4. Study the job requirements and identify the strongest technical overlaps
   with the candidate's profile and projects.

5. Prioritize concrete technical evidence over generic statements.

6. When a GitHub project directly demonstrates something requested by the
   job, use that project as evidence.

   For example, prefer:

   "I've built multi-agent workflows using LangGraph with supervisor/worker
   agents, tool calling, parallel execution and human-in-the-loop flows."

   Instead of:

   "I have experience with AI agents."

7. You may reference one or two relevant projects when they strengthen the
   answer. You do not need to mention repository names unless doing so sounds
   natural.

8. Do NOT mention technologies from the job description unless the candidate
   profile or project evidence supports them.

9. Do NOT turn project experience into professional experience.

10. Pick approximately 2-4 of the strongest technical overlaps. Do not try to
    match every requirement.

11. The company mission or company description should normally be a small
    part of the answer. Focus primarily on the engineering work and what the
    candidate can bring to the role.

12. Even for questions such as "What interests you about working here?",
    connect the interest to the actual technical work described in the role.

13. Prioritize the candidate's AI engineering, Python/backend engineering,
    APIs, system design, databases, RAG, LLM systems and agentic AI experience
    whenever supported and relevant.

14. Write confidently but never exaggerate.

15. Keep the answer approximately 3-5 sentences.

16. Write in first person using simple, natural and professional language.

17. Avoid generic corporate or AI-sounding phrases such as:
    "aligns with my experience",
    "positions me to",
    "I am particularly drawn to",
    "leveraging my expertise",
    "perfect fit",
    "unique opportunity",
    "I am excited to contribute to your mission".

18. Do not simply repeat or paraphrase the job description.

19. Do not mention the candidate profile, retrieved evidence, these
    instructions, semantic search, RAG, or AI generation.

20. Return ONLY the final application answer.

Before writing, silently determine:

- What are the most important technical requirements of this role?
- Which requirements have strong evidence in the candidate profile?
- Which requirements have strong evidence in the GitHub projects?
- Which 1-2 projects provide the strongest evidence?
- What are the strongest technical reasons this candidate fits this role?

Then write the answer naturally.
""".strip()
