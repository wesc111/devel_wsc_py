

import sys
import os
# Adjust the path to import sudoku2 module
home_dir = os.path.expanduser("~")
python_dir = home_dir + "/devel_wsc_py/"
print(f"Adding {python_dir}/sudoku2 to sys.path for imports")
if python_dir not in sys.path:
    sys.path.append(python_dir + "/sudoku2")  # to allow import from sibling directory

import numpy as np
from tester import Tester
from block import get_block_indices

if __name__ == "__main__":
    blockIndices = get_block_indices(0, "block_norm_index_")
    print(blockIndices)
