from pathlib import Path


def load_markdown_documents(knowledge_base_dir: str | Path) -> list[dict]:
    knowledge_base_path = Path(knowledge_base_dir)

    if not knowledge_base_path.exists():
        raise FileNotFoundError(
            f"Knowledge base directory not found: {knowledge_base_path}"
        )

    documents = []

    for file_path in sorted(knowledge_base_path.rglob("*.md")):
        content = file_path.read_text(encoding="utf-8").strip()

        if not content:
            continue

        documents.append({
            "text": content,
            "metadata": {
                "source": file_path.relative_to(
                    knowledge_base_path
                ).as_posix(),
                "topic": file_path.stem,
            },
        })

    if not documents:
        raise ValueError("No Markdown documents found in the knowledge base.")

    return documents