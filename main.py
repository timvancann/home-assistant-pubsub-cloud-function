import datetime
import json
import base64

from google.cloud import bigquery

DATASET = ''
TABLE = ''

bigquery_client = bigquery.Client()
dataset = bigquery_client.dataset(DATASET)
table_ref = dataset.table(TABLE)
table = bigquery_client.get_table(table_ref)


def hello_pubsub(data, context):

    if 'data' in data:
        state = json.loads(
            base64.b64decode(
                data['data']
            )
        )
    else:
        raise ValueError('No data provided')

    dt = {
        'entity_id': state['entity_id'],
        'state': state['state'],
        'attributes': json.dumps(state['attributes']),
        'last_changed': datetime.datetime.fromisoformat(state['last_changed'].replace('"', '')),
        'last_updated': datetime.datetime.fromisoformat(state['last_updated'].replace('"', '')),
        'context': json.dumps(state['context'])
    }
    res = bigquery_client.insert_rows(table, [dt])
