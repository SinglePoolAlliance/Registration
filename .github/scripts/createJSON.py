import pprint, json, time, git, os
from git import Repo

def get_date_from_commit(repo, linenumber ,file):
    raw_blame=repo.git.blame('HEAD', '-L ' + linenumber + ',' + linenumber, file)

    commit_id = raw_blame.split(' ')[0].replace('^','')
    
    commit = repo.commit(commit_id)
    
    commit_date = time.strftime("%Y-%m-%d", time.gmtime(commit.committed_date))
    
    return commit_date

#Defining global variables
repository = os.environ.get('GITHUB_WORKSPACE')

repo = Repo(repository)

registryfile = repository + "/" + 'registry.json'

aboutfile = repository + "/" + 'spa_about.json'
with open(aboutfile,'r') as about_file:
    spa_about = json.load(about_file)

print(spa_about)
with open(registryfile,'r') as pools_file:
    pools = json.load(pools_file)
    poollist = []
    for pool in pools:
        poolinfo = {}
        ticker = pool['ticker']

        poolid = pool['poolId']
        with open(registryfile,'r') as pools_file2:
            linenumber = 0
            for line in pools_file2:
                linenumber += 1
                if ticker in line:
                    
                    join_date = get_date_from_commit(repo,str(linenumber),registryfile)
                    break
        poolinfo['pool_id'] = poolid
        poolinfo['member_since'] = join_date
        poolinfo['name'] = ticker
        poollist.append(poolinfo)
sortedpools = sorted(poollist, key=lambda k: k['member_since'])
json_member_part = {}
for pool in sortedpools:
    json_member_part[str(sortedpools.index(pool))] = pool

spa_about['adapools']['members'] = json_member_part


with open(r'adapools.json','w') as json_file:
    json.dump(spa_about,json_file, indent=2)
