import json
from pathlib import Path

from assertpy.assertpy import assert_that
from config import settings as conf

in_root = Path(conf.input.root)
ext = conf.input.ext
files = {}

assert_that(in_root).is_directory().is_readable()
print("Scanning directories...")

for split in "train", "val", "test":
    for file in (in_root / split).glob(f"**/*{ext}"):
        files[file.stem.strip()] = str(file.parent.relative_to(in_root))

with open(conf.fileloc, "w") as f:
    json.dump(files, f)

replacements = [
    file.stem
    for file in (in_root / "replacement/replacement_for_corrupted_k400").glob(
        f"**/*{ext}"
    )
]

with open(conf.replacements.list, "w") as f:
    json.dump(replacements, f)
