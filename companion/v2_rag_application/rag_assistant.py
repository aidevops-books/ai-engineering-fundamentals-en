"""AI Knowledge Assistant -- Version 2: RAG Application (Chapter 9).

The retrieval and reranking stages (retrieve, rerank) need only
sentence-transformers and run fully offline after the first model download --
they are verified independently of any LLM API key. Only rag_answer()'s
final generation step requires OPENAI_API_KEY.

Run:
    python rag_assistant.py                 # retrieval + reranking only
    OPENAI_API_KEY=sk-... python rag_assistant.py --generate   # full pipeline
"""

import sys
from pathlib import Path

import numpy as np
from sentence_transformers import CrossEncoder, SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "shared"))
from knowledge_base import KNOWLEDGE_BASE  # noqa: E402

embedder = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
kb_embeddings = embedder.encode(KNOWLEDGE_BASE)


def retrieve(query: str, top_k: int = 5) -> list[str]:
    """Stage 4: fast initial candidate retrieval by embedding similarity."""
    query_emb = embedder.encode(query)
    scores = np.dot(kb_embeddings, query_emb) / (
        np.linalg.norm(kb_embeddings, axis=1) * np.linalg.norm(query_emb)
    )
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [KNOWLEDGE_BASE[i] for i in top_indices]


def rerank(query: str, candidates: list[str], top_k: int = 2) -> list[str]:
    """Stage 5: slower, more accurate reordering of the initial candidates."""
    pairs = [(query, c) for c in candidates]
    scores = reranker.predict(pairs)
    ranked = [c for _, c in sorted(zip(scores, candidates), reverse=True)]
    return ranked[:top_k]


def rag_answer(question: str) -> str:
    """Full pipeline including generation -- requires OPENAI_API_KEY."""
    from openai import OpenAI

    candidates = retrieve(question)
    retrieved = rerank(question, candidates)
    context = "\n".join(f"- {chunk}" for chunk in retrieved)

    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # illustrative model name -- see Chapter 1's note
        messages=[
            {"role": "system", "content":
                "Answer the user's question using ONLY the context below. "
                "If the answer isn't in the context, say you don't have that information.\n\n"
                f"Context:\n{context}"},
            {"role": "user", "content": question},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    question = "How long do I have to return a product?"

    candidates = retrieve(question)
    print("Retrieved candidates:", candidates)
    top = rerank(question, candidates)
    print("After reranking:", top)

    if "--generate" in sys.argv:
        print("\nFull answer:", rag_answer(question))
    else:
        print("\n(Pass --generate with OPENAI_API_KEY set to also generate an answer.)")
