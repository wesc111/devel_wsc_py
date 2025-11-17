# sudoku2_basic_tests.py

import sys, os

# Adjust the path to import sudoku2 module
home_dir = os.path.expanduser("~")
python_dir = home_dir + "/OneDrive/devel_wsc_private/python"
if python_dir not in sys.path:
    sys.path.append(python_dir + "/sudoku2")  # to allow import from sibling directory

from candidate import Candidate
from tester import Tester
from util.string2array import string2array


if __name__ == '__main__':
    tester = Tester()
    
    # Test: Initialization with values (order-independent comparison)
    candidate = Candidate(0, 0, [3, 2, 1])
    tester.test_checker(candidate.compare_values(Candidate(0, 0, [1, 2, 3])), 
                        "Candidate initialization")

    # Test: set all values to 1-9, compare with shuffled list
    candidate.set_values([1, 2, 3, 4, 5, 6, 7, 8, 9])
    tester.test_checker(candidate.compare_values(Candidate(0, 0, [1, 9, 7, 8, 6, 5, 4, 3, 2])), 
                        "Set values to full range 1-9")
    
    # Test: Set values
    candidate.set_values([4, 5, 6])
    tester.test_checker(candidate.compare_values(Candidate(0, 0, [4, 5, 6])), 
                        "Set values")

    # Test: Add value
    candidate.add_value(7)
    tester.test_checker(candidate.compare_values(Candidate(0, 0, [4, 5, 6, 7])), 
                        "Add value")

    # Test: Remove value
    candidate.remove_value(5)
    tester.test_checker(candidate.compare_values(Candidate(0, 0, [4, 6, 7])), 
                        "Remove value")
    
    # Test: Add duplicate value (should not add)
    candidate.add_value(7)
    tester.test_checker(candidate.compare_values(Candidate(0, 0, [4, 6, 7])), 
                        "Add duplicate value (should be no-op)")
    
    # Test: Remove non-existent value (should not error)
    candidate.remove_value(99)
    tester.test_checker(candidate.compare_values(Candidate(0, 0, [4, 6, 7])), 
                        "Remove non-existent value (should be no-op)")
    
    # Test: Access attributes directly
    tester.test_checker(candidate.row == 0 and candidate.col == 0, 
                        "Direct attribute access")
    
    # Final results
    print("\n" + "="*50)
    print(tester)
    print("="*50)