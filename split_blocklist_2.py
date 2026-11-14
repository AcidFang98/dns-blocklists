from pathlib import Path
from urllib.request import urlopen

url = (
    "https://raw.githubusercontent.com/AcidFang98/dns-blocklists/"
    "refs/heads/main/wildcard/multi-onlydomains.txt.txt"
)
output_dir = Path("wildcard/multi-onlydomains.parts")
limit = 100_000

with urlopen(url, timeout=60) as response:
    text = response.read().decode("utf-8")

# Keep each nonblank line as an entry.
entries = [line for line in text.splitlines() if line.strip()]

output_dir.mkdir(parents=True, exist_ok=True)
for old_file in output_dir.glob("part-*.txt"):
    old_file.unlink()

for start in range(0, len(entries), limit):
    part_num = start // limit + 1
    chunk = entries[start : start + limit]
    output = output_dir / f"part-{part_num:04}.txt"
    output.write_text("\n".join(chunk) + "\n", encoding="utf-8")
    print(f"{output}: {len(chunk)} lines")
