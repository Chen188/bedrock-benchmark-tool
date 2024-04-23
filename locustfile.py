# -*- coding: utf-8 -*-
from locust import HttpUser, task, constant_throughput, events
from contextlib import ContextDecorator, contextmanager
from authorizer import authorize, get_payload_hash
import config as conf
import time
import json
import base64
import re

# ref: https://github.com/locustio/locust/blob/master/examples/manual_stats_reporting.py
@contextmanager
def _manual_report(name, value):
    try:
        yield
    except Exception as e:
        events.request.fire(
            request_type="manual",
            name=name,
            response_time=value,
            response_length=0,
            exception=e,
        )
        raise
    else:
        events.request.fire(
            request_type="manual",
            name=name,
            response_time=value,
            response_length=0,
            exception=None,
        )


def manual_report(name_or_func, value):
    if callable(name_or_func):
        # used as decorator without name argument specified
        return _manual_report(name_or_func.__name__)(name_or_func, value)
    else:
        return _manual_report(name_or_func, value)



# change param as need
PAYLOAD_0 = json.dumps({
    "system": '',
    "messages": [{"role": "user", "content": [{"type": "text", "text": "hi"}]}],
    "anthropic_version":"bedrock-2023-05-31",
    "max_tokens": 10,
    "stop_sequences": ["\n\nHuman:", "\n\nAssistant"],
    "top_p": 0.999,
    "temperature": 1,
})
payload_hash = get_payload_hash(PAYLOAD_0)

class WebsiteUser(HttpUser):
    wait_time = constant_throughput(10)

    # @task  #uncomment this line if you want to do the test in non-stream mode
    def test_post(self):
        global payload_hash
        """
        Load Test Bedrock Endpoint (POST request)
        """
        headers = authorize(PAYLOAD_0, payload_hash)
        resp = self.client.post(conf.BEDROCK_ENDPOINT_URL, data=PAYLOAD_0, headers=headers, name='Post Request')

        if resp.status_code != 200:
            print(resp, resp.reason)
            time.sleep(1)
        else:
            # print("Response status code:", resp.status_code)
            resp_body = json.loads(resp.text)
            assist = resp_body['content'][0]['text']
            usage = resp_body['usage']
            input_tokens = usage['input_tokens']
            output_tokens = usage['output_tokens']

            # print(f"Response. [Len: {len(assist)}]", assist[:10])

    @task
    def test_post_stream(self):
        """
        Load Test Bedrock Endpoint (POST request) with streaming mode, which can log time-to-first-token
        """
        global payload_hash
        headers = authorize(PAYLOAD_0, payload_hash, True)
        resp = self.client.post(conf.BEDROCK_ENDPOINT_STREAM_URL, data=PAYLOAD_0, headers=headers, name='Post Request')

        if resp.status_code != 200:
            print(resp, resp.reason)
            time.sleep(1)
        else:
            stat = resp.text.split('event')[-1]
            try:
                result = re.search('bytes":"(.*)"', stat).group(1).split('"')[0]
                stat = json.loads(base64.b64decode(result).decode())['amazon-bedrock-invocationMetrics']

                with manual_report('invocationLatency', stat['invocationLatency']):
                    pass
                
                with manual_report('firstByteLatency', stat['firstByteLatency']):
                    pass

                with manual_report('perTokenLatency', (stat['invocationLatency'] - stat['firstByteLatency']) / stat['outputTokenCount']):
                    pass
            except:
                print(stat)
                print('---' * 10)

def local_test():
    print('**' * 10)
    import http.client
    conn = http.client.HTTPSConnection(conf.HOST)
    headers = authorize(PAYLOAD_0, payload_hash)
    # print(headers)

    conn.request('POST', f'/model/{conf.MODEL_ID}/invoke', PAYLOAD_0, headers)

    response = conn.getresponse()
    resp_body = json.loads(response.read().decode())
    # print(resp_body)
    print(resp_body['content'][0]['text'])
    usage = resp_body['usage']
    print(usage)


def local_test_stream():
    print('**' * 10)
    import http.client
    conn = http.client.HTTPSConnection(conf.HOST)
    headers = authorize(PAYLOAD_0, payload_hash, True)
    # print(headers)

    conn.request('POST', f'/model/{conf.MODEL_ID}/invoke-with-response-stream', PAYLOAD_0, headers)

    response = conn.getresponse()
    resp = response.read()
    print(resp)

if __name__ == '__main__':
    import logging

    logger = logging.getLogger('my-authorizer')
    logger.setLevel(logging.WARNING)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    local_test_stream()
    local_test()