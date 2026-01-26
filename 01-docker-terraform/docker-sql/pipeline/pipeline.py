#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
import pyarrow.parquet as pq
from tqdm import tqdm
import fsspec

def get_iterator(url,chunksize):
    if url.endswith('.parquet'):
        fs, path = fsspec.core.url_to_fs(url)
        file_obj = fs.open(path)
        
        file = pq.ParquetFile(file_obj)
        return file.iter_batches(batch_size=chunksize)
    else:
        return pd.read_csv(url,iterator=True, chunksize=chunksize)

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')
@click.option('--url', help='URL of the file (optional)')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunksize,url):
    """Ingest NYC taxi data into PostgreSQL database."""
    
    if not url:
        prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
        url = f'{prefix}/green_tripdata_{year}-{month:02d}.parquet'

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    df_iter = get_iterator(url, chunksize)

    first = True

    for batch in tqdm(df_iter,desc='Ingesting data'):
        df_chunk = batch.to_pandas() if hasattr(batch,'to_pandas') else batch
        
        if first:
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )

if __name__ == '__main__':
    run()