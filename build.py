import json
import os
import shutil
from pathlib import Path

from assertpy.assertpy import assert_that
from config import settings as conf
from tqdm import tqdm

in_root = Path(conf.input.root)
out_root = Path(conf.output.root)
n_classes = conf.output.n_classes
partition = conf.output.partition
ext = conf.input.ext
op = conf.op
replacement_dir = conf.replacements.dir
replacement_count = 0
n_files = 0

assert_that(in_root).is_directory().is_readable()

with open(conf.fileloc) as f:
    fileloc = json.load(f)

with open(conf.replacements.list) as f:
    replacements = json.load(f)

for split in "labeled0", "unlabeled0", "val0":
    file_list_path = (
        Path("VideoSSL/datasplit/kinetics")
        / f"ssl_sub{n_classes}c_{partition}_{split}.lst"
    )

    assert_that(file_list_path).is_file().is_readable()
    print(f"\n[{split}]")

    with open(file_list_path) as f:
        file_list = f.readlines()

    bar = tqdm(total=len(file_list))

    for file in file_list:
        target_split, action, filename = file.strip().split("/")
        filename = filename.split("*")[0]
        stem = filename.split(".")[0]

        if stem in replacements:
            src = in_root / replacement_dir / filename
            replacement_count += 1
        elif stem in fileloc:
            src = in_root / fileloc[stem] / filename
        else:
            continue

        dst = out_root / target_split.lower() / action / filename
        n_files += 1

        dst.parent.mkdir(parents=True, exist_ok=True)

        if op == "copy":
            shutil.copy(src, dst)
        else:
            os.symlink(src, dst)

        bar.update(1)

    bar.close()

print("Replacements:", replacement_count)
print("Total:", n_files)
