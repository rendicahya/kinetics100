from pathlib import Path

from assertpy.assertpy import assert_that
from config import settings as conf

k400_root = Path(conf.kinetics400.root)
ext = conf.kinetics400.ext
files = set()

assert_that(k400_root).is_directory().is_readable()
print("Scanning directories...")

for split in "train", "val", "test":
    for action in (k400_root / "videos" / split).iterdir():
        files.update(
            {
                file.stem.strip()
                for file in action.iterdir()
                if file.is_file() and file.suffix == ext
            }
        )

for split in "train", "val", "test":
    file_list_path = Path("CMN/kinetics-100") / f"{split}.list"

    assert_that(file_list_path).is_file().is_readable()

    with open(file_list_path) as f:
        file_list = {file.strip().split("/")[1] for file in f.readlines()}

    total = len(file_list)
    found = len(files & file_list)
    not_found = len(file_list - files)

    print("Total:", total)
    print("Found:", found)
    print("Not found:", not_found, end="\n\n")
