import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def generate_chunks(start_date, end_date, **offset):
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)

    chunks = []

    if not offset:
        offset = {"years": 1}

    while start < end:
        chunk_end = min(
            start + pd.DateOffset(**offset),
            end
        )

        chunks.append((start, chunk_end))

        start = chunk_end

    return chunks


def download_chunks(chunks, process_chunk):

    with ThreadPoolExecutor(max_workers=10) as executor:
        full_response = [
            record
            for response in executor.map(
                lambda chunk: process_chunk(*chunk),
                chunks
            )
            for record in response
        ]

    return (
        pd.DataFrame(full_response)
        .drop_duplicates()
        .to_dict()
    )