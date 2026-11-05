def split_into_blocks(text: str) -> list[str]:
    """Split text into blocks without breaking fenced code blocks."""
    lines = text.splitlines()
    blocks = []
    current_block = []
    inside_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            inside_code_block = not inside_code_block

        if not line.strip() and not inside_code_block:
            if current_block:
                blocks.append("\n".join(current_block).strip())
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block).strip())

    return [block for block in blocks if block]


def split_large_block(block: str, max_chars: int) -> list[str]:
    """Split an individual block if it exceeds the size limit."""
    pieces = []

    while len(block) > max_chars:
        split_at = block.rfind("\n", 0, max_chars)

        if split_at == -1:
            split_at = max_chars

        pieces.append(block[:split_at].strip())
        block = block[split_at:].strip()

    if block:
        pieces.append(block)

    return pieces


def chunk_documents(
    documents: list[dict],
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size.")

    chunks = []

    for document in documents:
        blocks = split_into_blocks(document["text"])

        current_chunk = ""
        chunk_index = 0

        for block in blocks:
            pieces = split_large_block(block, chunk_size)

            for piece in pieces:
                candidate = (
                    f"{current_chunk}\n\n{piece}"
                    if current_chunk
                    else piece
                )

                if len(candidate) <= chunk_size:
                    current_chunk = candidate
                    continue

                if current_chunk:
                    chunks.append({
                        "text": current_chunk,
                        "metadata": {
                            **document["metadata"],
                            "chunk_index": chunk_index,
                        },
                    })
                    chunk_index += 1

                previous_overlap = current_chunk[-overlap:] if current_chunk else ""

                current_chunk = (
                    f"{previous_overlap}\n{piece}"
                    if previous_overlap
                    else piece
                )

                if len(current_chunk) > chunk_size:
                    current_chunk = piece

        if current_chunk:
            chunks.append({
                "text": current_chunk,
                "metadata": {
                    **document["metadata"],
                    "chunk_index": chunk_index,
                },
            })

    return chunks