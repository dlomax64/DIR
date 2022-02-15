import sys
import gzip

auths = {}
with gzip.open('/da3_data/basemaps/gz/c2datFullT' + sys.argv[1] + '.s', mode='rt', encoding="utf8", errors='ignore') as a:
    for line in a:
        try:
            comm, time, _, auth, _, _ = line.strip().split(';')
        except ValueError:
            # print(f'Bad line: {line}', file=sys.stderr)
            pass
        if auth not in auths or auths[auth][0] > time:
            auths[auth] = (time, comm)

for k, v in auths.items():
    print(f'{k};{v[0]};{v[1]}')
