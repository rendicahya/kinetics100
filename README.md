# Kinetics-100 Dataset

# Steps

1. Download Kinetics-400 using the provided `k400_downloader.sh` and `k400_extractor.sh` in https://github.com/cvdfoundation/kinetics-dataset.git.
2. Clone repo.

```bash
git clone --recursive https://github.com/rendicahya/kinetics100.git
cd kinetics100
```

3. Configure `config.json`.
4. Run `check.py` for a precheck. As of January 5, 2024:

| Split | Total | Found |
|-------|-------|-------|
| Train | 6,400 | 6,351 |
| Val   | 1,200 | 1,190 |
| Test  | 2,400 | 2,379 |

5. Run `build.py` to build Kinetics-100.
