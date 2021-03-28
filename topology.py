#!/usr/bin/python3

import requests
import json
import time
import argparse


parser = argparse.ArgumentParser(description='''Generate CSPA relay metadata''')
parser.add_argument('--output', help="output", required=True)
args = parser.parse_args()

API_URL= "http://change.this:3100/graphql"

try:
  r = requests.get('https://raw.githubusercontent.com/SinglePoolAlliance/Registration/master/registry.json')
except requests.exceptions.RequestException as e: 
  raise SystemExit(e)

pools = json.loads(r.text)
spa_relays = []
for pool in pools:
  headers = {'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json', 'Accept': 'application/json', 'Connection': 'keep-alive', 'DNT': '1', 'Origin': 'http://localhost:3100'}
  data = {"query":'''{ stakePools ( where: 
         { hash: 
                 {  _eq: "''' + pool['poolId']  +'''"}} ) { relays { ipv4 dnsName port} } }'''}

  while True:
    try:
      r = requests.post(API_URL, data=json.dumps(data), headers=headers)
    except:
      print ("[err] got an exception while querying graphql...retrying")
      time.sleep(1)
      pass
    else:
      break

  struct_query = json.loads(r.text)
  while r.status_code != 200 or "errors" in struct_query:
    print ("[err] got an error while querying graphql...retrying")
    time.sleep(1)
    while True:
      try:
        r = requests.post(API_URL, data=json.dumps(data), headers=headers)
      except:
        print ("[err] got an exception while querying graphql...retrying")
        time.sleep(5)
        pass
      else:
        break
    struct_query = json.loads(r.text)
 
  print("[debug] {0}".format(r.text.strip()))
  relays = json.loads( r.text)['data']['stakePools'][0]['relays']
  for relay in relays: 
    if relay['dnsName'] != None:
      spa_relays.append({"addr": relay['dnsName'], "port": relay['port'], "valency": 1 })
      break
    elif relay['ipv4'] != None:
      spa_relays.append({"addr": relay['ipv4'], "port": relay['port'], "valency": 1 })
      break

with open(args.output, 'w') as f:
  json.dump(spa_relays, f, indent=4, sort_keys=True)
