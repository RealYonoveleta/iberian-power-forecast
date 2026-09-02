import time
import pandas as pd
from datetime import datetime
from precio_electricidad_ml.esios import request_esios_indicator
from precio_electricidad_ml.download.utils import generate_chunks, download_chunks

def download_esios_indicator_data(
    indicator,
    start_date=datetime(2023, 1, 1), 
    end_date=datetime(2026, 1, 1),
    chunk_offset=None,
    max_workers=10
):
    # some indicators (e.g. per-province breakdowns) are too large for a yearly chunk and time out
    chunks = generate_chunks(start_date, end_date, **(chunk_offset or {}))

    def process_chunk(start_date, end_date):

        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "time_trunc": "hour",
            "time_agg": "average"
        }

        # ESIOS occasionally serves a gateway-timeout/error page under concurrent load; retry before failing
        for attempt in range(3):
            try:
                data = request_esios_indicator(indicator, params=params)
                return [row for row in data["indicator"]["values"]]
            except ValueError:
                if attempt == 2:
                    raise
                time.sleep(5 * (attempt + 1))

    data = download_chunks(chunks, process_chunk, max_workers=max_workers)

    df = pd.DataFrame(data)

    df["datetime"] = pd.to_datetime(
        df["datetime"],
        utc=True
    )

    # some indicators ignore end_date and keep returning data up to "now"
    df = df[
        (df["datetime"] >= pd.Timestamp(start_date, tz="UTC"))
        & (df["datetime"] < pd.Timestamp(end_date, tz="UTC"))
    ]

    return df[["datetime", "value"]]