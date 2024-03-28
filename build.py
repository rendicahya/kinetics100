import os
from pathlib import Path

from assertpy.assertpy import assert_that
from config import settings as conf
from tqdm import tqdm

k400_root = Path(conf.kinetics400.root)
k100_root = Path(conf.kinetics100.root)
ext = conf.kinetics400.ext
files = {}

assert_that(k400_root).is_directory().is_readable()
print("Scanning directories...")

bar = tqdm()

for split in "train", "val", "test":
    for action in (k400_root / "videos" / split).iterdir():
        bar.set_description(f"{split}/{action.name}")
        files.update(
            {
                file.stem.strip(): file
                for file in action.iterdir()
                if file.is_file() and file.suffix == ext
            }
        )

print("\nCreating symlinks...")

created = 0

for split in "train", "val", "test":
    file_list_path = Path("CMN/kinetics-100") / f"{split}.list"

    assert_that(file_list_path).is_file().is_readable()

    with open(file_list_path) as f:
        file_list = f.readlines()

    for file in file_list:
        action, stem = file.strip().split("/")

        if stem not in files.keys():
            continue

        src = files[stem]
        dst = (k100_root / split / action / stem).with_suffix(ext)

        dst.parent.mkdir(parents=True, exist_ok=True)
        bar.set_description(f"{split}/{action}/{stem}")
        os.symlink(src, dst)

        created += 1

bar.close()
print("Created symlinks:", created)
