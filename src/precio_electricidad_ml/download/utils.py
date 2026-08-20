import pandas as pd

def generate_chunks(start_date, end_date, years=1):
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)

    chunks = []

    while start < end:
        chunk_end = min(
            start + pd.DateOffset(years=years),
            end
        )

        chunks.append((start, chunk_end))

        start = chunk_end

    return chunks


def download_chunks(chunks, process_cunk):

    full_response = []

    for start, end in chunks:
        response = process_cunk(start, end)
        full_response.extend(response)

    records = (
        pd.DataFrame(full_response)
        .drop_duplicates()
        .to_dict()
    )

    return records