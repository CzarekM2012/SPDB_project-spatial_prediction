from pathlib import Path

import numpy as np

_COLUMNS_NUMBER_HEADER = "ncols"
_ROWS_NUMBER_HEADER = "nrows"


def read_data(file: Path):
    with open(file, encoding="utf-8") as reader:
        shape = {}
        for _ in range(2):
            line = reader.readline()
            line = line.rstrip()
            line = line.split()
            shape[line[0]] = int(line[1])
        data = np.fromfile(reader, sep=" ")
        data = data.reshape((shape[_ROWS_NUMBER_HEADER], shape[_COLUMNS_NUMBER_HEADER]))
    return data


def write_data(dest: Path, data: np.ndarray):
    with open(dest, "w", encoding="utf-8") as writer:
        writer.writelines(
            [
                f"{_ROWS_NUMBER_HEADER}        {data.shape[1]}\n",
                f"{_COLUMNS_NUMBER_HEADER}        {data.shape[0]}\n",
            ]
        )
        np.savetxt(writer, data)
