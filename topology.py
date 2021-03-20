import requests
import json


API_URL= "https://graphql-api.mainnet.dandelion.link"
r = requests.get('https://raw.githubusercontent.com/SinglePoolAlliance/Registration/master/registry.json')
pools = json.loads(r.text)
spa_relays = []
for pool in pools:
    #(pool['poolId'])
    headers = {'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json', 'Accept': 'application/json', 'Connection': 'keep-alive', 'DNT': '1', 'Origin': 'http://localhost:3100'}

    data = {"query":'''{ stakePools ( where: 
         { hash: 
                 {  _eq: "''' + pool['poolId']  +'''"}} ) { relays { ipv4 dnsName port} } }'''}

    r = requests.post(API_URL, data=json.dumps(data), headers=headers)
    relays = json.loads( r.text)['data']['stakePools'][0]['relays']
    for relay in relays: 
        if relay['ipv4'] == None :
           if relay['dnsName'] == None :
              print("invalid")
           else :
              spa_relays.append( {"addr": relay['dnsName'], "port": relay['port'], "valency": 1 }  )      
              break      
        else:       
           spa_relays.append( {"addr": relay['ipv4'], "port": relay['port'], "valency": 1 }  )      
           break      

print(json.dumps(spa_relays, indent=4, sort_keys=True))
