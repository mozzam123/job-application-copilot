from app.knowledge.project_index import ProjectIndex


project_index = ProjectIndex()


query = """
Looking for an engineer experienced with
AI agents, LangChain, LangGraph,
multi-agent systems, tool calling,
and human-in-the-loop workflows.
"""


results = project_index.search(
    query,
    top_k=5,
)


for result in results:

    print("\n-------------------------")

    print(
        "Project:",
        result["repository"],
    )

    print(
        "Score:",
        round(result["score"], 3),
    )

    print(
        "URL:",
        result["url"],
    )
