from crawler import parse_host, get_hosts
from tqdm import tqdm

hosts = get_hosts(max_n=20)

for h in tqdm(hosts):
    parsed = parse_host(h, positive=True)
    print(f"Parsed: {len(parsed)}; unique: {len(set(parsed))}")
