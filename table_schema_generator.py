import io
import argparse
import pandas as pd

from common.config import s3InputBucket, s3_client
from common.constant import EMPTY
from common.s3_util import get_object


def change_case(str):
    str = str.replace(' ', '_')
    str = str.replace('-', '_')
    res = [str[0].lower()]
    previous = res
    for c in str[1:]:
        if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            if previous != '_':
                res.append('_')
            res.append(c.lower())
        else:
            previous = c
            res.append(c)
    return ''.join(res)


def get_primary_key(df):
    for data in df:
        deDuped = df.drop_duplicates(data)
        if len(deDuped.index) == len(df.index):
            return change_case(data)
    return EMPTY


def create_redshift_table_stmt(df, table, schema='public'):
    d_types = df.convert_dtypes()
    output = io.StringIO()
    output.write(f"CREATE TABLE IF NOT EXISTS {schema}.{table} (")
    sort_key = EMPTY
    for d in d_types:
        if d_types[d].dtype == 'string':
            try:
                pd.to_datetime(df[d], dayfirst=True, errors='ignore')
                output.write(f'{change_case(d)} TIMESTAMP, ')
                if sort_key == EMPTY:
                    sort_key = change_case(d)
            except Exception as e:
                try:
                    pd.to_timedelta(df[d])
                    output.write(f'{change_case(d)} TIMESTAMP, ')
                    if sort_key == EMPTY:
                        sort_key = change_case(d)
                except Exception as e:
                    output.write(f'{change_case(d)}  VARCHAR({int(df[d].str.len().max())}), ')
        elif d_types[d].dtype == 'Int64':
            if df[d].isin([0, 1]).all():
                output.write(f'{change_case(d)} BOOLEAN, ')
            else:
                output.write(f'{change_case(d)} INTEGER, ')
        elif d_types[d].dtype == 'Float64':
            output.write(f'{change_case(d)} FLOAT, ')
    sql = output.getvalue()[:-2]
    sql = sql + ')'

    primary_key = get_primary_key(df)
    if len(primary_key) > 0:
        sql += f' DISTSTYLE KEY DISTKEY({primary_key})'
    if sort_key != EMPTY:
        sql += f' SORTKEY {sort_key}'
    sql += ';'
    return sql


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("s3_object_name", help="CSV filename uploaded to S3 bucket.")
    parser.add_argument("table_name", help="Preferred table name.")
    parser.add_argument("--schema_name", "-s", default="public",
                        help="Schema name in which you want to create a table.")

    args = vars(parser.parse_args())
    object_key = args['s3_object_name']
    table_name = args['table_name']
    schema_name = args['schema_name']
    obj = get_object(s3_client, s3InputBucket, object_key)
    df = pd.read_csv(obj, low_memory=False)
    sql = create_redshift_table_stmt(df, table_name, schema_name)
    with open('output/create_table.sql', 'w') as f:
        f.write(sql)
    print('################## CREATE TABLE DDL ##################')
    print(sql)
    print('######################################################')
