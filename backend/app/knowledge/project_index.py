import json
from pathlib import Path

import faiss
import httpx
import numpy as np


OLLAMA_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"

INDEX_DIR = Path("data/project_index")
INDEX_FILE = INDEX_DIR / "projects.faiss"
METADATA_FILE = INDEX_DIR / "metadata.json"


class ProjectIndex:

    def __init__(self):
        self.index = None
        self.metadata = []

    def embed(self, text: str) -> np.ndarray:
        response = httpx.post(
            f"{OLLAMA_URL}/api/embed",
            json={
                "model": EMBEDDING_MODEL,
                "input": text,
            },
            timeout=120.0,
        )

        response.raise_for_status()

        data = response.json()

        embedding = np.array(
            data["embeddings"][0],
            dtype="float32",
        )

        # Normalize so inner product behaves like cosine similarity.
        faiss.normalize_L2(embedding.reshape(1, -1))

        return embedding

    def add_projects(self, projects: list[dict]):
        if not projects:
            raise ValueError("No projects provided.")

        embeddings = []

        for project in projects:
            text = project["content"]

            embedding = self.embed(text)

            embeddings.append(embedding)

            self.metadata.append(
                {
                    "repository": project["repository"],
                    "url": project["url"],
                    "content": text,
                }
            )

            print(f"Embedded: {project['repository']}")

        matrix = np.vstack(embeddings).astype("float32")

        dimension = matrix.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(matrix)

    def save(self):
        if self.index is None:
            raise ValueError("Index has not been created.")

        INDEX_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            str(INDEX_FILE),
        )

        with open(
            METADATA_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.metadata,
                file,
                indent=2,
            )

    def load(self):
        if not INDEX_FILE.exists():
            raise FileNotFoundError(
                "Project index does not exist. " "Run build_project_index.py first."
            )

        self.index = faiss.read_index(str(INDEX_FILE))

        with open(
            METADATA_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            self.metadata = json.load(file)

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict]:

        if self.index is None:
            self.load()

        query_embedding = self.embed(query).reshape(1, -1)

        scores, indexes = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for score, index in zip(
            scores[0],
            indexes[0],
        ):
            if index == -1:
                continue

            project = self.metadata[index]

            results.append(
                {
                    **project,
                    "score": float(score),
                }
            )

        return results
