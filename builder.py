#!/bin/python3

import sys
from os import system as s

parsedargs = sys.argv[1:]

commands={
        "auth": "docker build auth_service/ -t hmx098/auth:latest",
        "converter" : "docker build converter_svc/ -t hmx098/converter_svc:latest",
        "gateway": "docker build gateway/ -t hmx098/gateway:latest",
        "notification": "docker build notification_service/ -t hmx098/notification:latest"
        }

for i in parsedargs:
    if i=='.':
        for j in commands.keys():
            print("Building {j} service")
            s(commands[j])
    elif i in commands.keys():
        print(f"Building {i} service")
        s(commands[i])
    else:
        print("Error")



