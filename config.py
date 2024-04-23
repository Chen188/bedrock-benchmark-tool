from urllib.parse import quote

REGION = 'us-east-1'
HOST = f'bedrock-runtime.{REGION}.amazonaws.com'

## Model id for PT mode
# ORI_MODEL_ID = 'arn:aws:bedrock:us-east-1:123456789123:provisioned-model/ppa0wv52cyfz' # PT
# MODEL_ID = quote(ORI_MODEL_ID, safe='')

## Model id for OD mode
# MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'
MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'

BEDROCK_ENDPOINT_URL = f'https://{HOST}/model/{MODEL_ID}/invoke'
BEDROCK_ENDPOINT_STREAM_URL = f'https://{HOST}/model/{MODEL_ID}/invoke-with-response-stream'

## PUT your AK / SK here
ACCESS_KEY = 'your-access-key'
SECRET_KEY = 'your-serect-key'

CONTENT_TYPE = 'application/json'
METHOD = 'POST'
SERVICE = 'bedrock'
SIGNED_HEADERS = 'host;x-amz-date'
CANONICAL_QUERY_STRING = ''
ALGORITHM = 'AWS4-HMAC-SHA256'
