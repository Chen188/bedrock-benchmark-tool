#!/bin/bash
# . ~/bedrock-runtime/bin/activate
source /home/ubuntu/.bashrc
conda activate bedrock-runtime

locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &
locust --locustfile=locustfile.py --worker &

locust --host=http://localhost:7080 --web-port 8000 --locustfile=locustfile.py --master 