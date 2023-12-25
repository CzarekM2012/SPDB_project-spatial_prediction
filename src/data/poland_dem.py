"""
Remove headers from files with segments of Poland DEM
"""
from pathlib import Path

if __name__ == "__main__":
    DATA_DIR = Path("data/raw/poland_DEM")
    RESULTS_DIR = Path("data/processed/poland_DEM")
    if not RESULTS_DIR.is_dir():
        RESULTS_DIR.mkdir()
    for file in (path for path in DATA_DIR.iterdir() if path.is_file()):
        result = RESULTS_DIR.joinpath(file.name)
        with (
            open(file, encoding="utf-8") as reader,
            open(result, "w", encoding="utf-8") as writer,
        ):
            for _ in range(2):
                line = reader.readline()
                writer.write(line)
            for _ in range(4):
                next(reader)
            for line in reader:
                writer.write(line)
