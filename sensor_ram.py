#!/usr/bin/python3

import psutil
import pause
import requests
import platform
import argparse
import socket
import json
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--name', '-n', help="sensor name",
                    type=str, required=False)
parser.add_argument('--address', '-a', help="host address",
                    type=str, required=True)
parser.add_argument('--interval', '-i',
                    help="inteval in seconds", type=float, default=1.0)
args = parser.parse_args()

init_data = {
    "sensor_id": args.name,
    "host_name": socket.gethostname(),
    "platform": platform.system() + " "+platform.release(),
    "metric": "RamUsage",
    "unit": "%"
}
r = requests.post(args.address, data=json.dumps(init_data))
if(r.status_code == 200):
    while(True):
        timestamp = datetime.timestamp(datetime.now())
        msrmnt = {
            "timestamp": int(timestamp),
            "value": psutil.virtual_memory().percent
        }
        try:
            requests.post(args.address, data=json.dumps(msrmnt))
        except:
            print("nobody cares")
        pause.until(datetime.fromtimestamp(timestamp + args.interval))
else:
    print("NO CONNECTION")
