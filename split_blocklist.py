from pathlib import Path

source = Path("wildcard/tif.mini.txt")
output_dir = Path("wildcard/tif.mini.parts")
limit = 100_000

# Each nonblank line counts as one entry; comment lines are retained and count too.
entries = [
    line for line in source.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

output_dir.mkdir(parents=True, exist_ok=True)

# Remove old generated parts so rerunning doesn't leave stale files.
for old_file in output_dir.glob("part-*.txt"):
    old_file.unlink()

for start in range(0, len(entries), limit):
    part_num = start // limit + 1
    chunk = entries[start : start + limit]
    output = output_dir / f"part-{part_num:04}.txt"
    output.write_text("\n".join(chunk) + "\n", encoding="utf-8")
    print(f"{output}: {len(chunk)} lines")
