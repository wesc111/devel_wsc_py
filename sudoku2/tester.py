# Tester.py

class Tester:
    """Simple test framework for tracking pass/fail counts."""
    
    def __init__(self):
        self.pass_count = 0
        self.fail_count = 0
        self.testGroup = ""
    
    def setTestGroup(self, group_name: str) -> None:
        """Set the current test group name."""
        self.testGroup = group_name
        print(f"--- Test Group: {self.testGroup} ---")
    
    def test_checker(self, passed: bool, test_name: str) -> None:
        """Check a test result and update counters."""
        if passed:
            self.pass_count += 1
            print(f"✓ {test_name}: PASS")
        else:
            self.fail_count += 1
            print(f"✗ {test_name}: FAIL")
    
    def __str__(self) -> str:
        total = self.pass_count + self.fail_count
        line1 = f"Tests Passed: {self.pass_count}/{total}, Tests Failed: {self.fail_count}/{total}"
        line2 = "PASS: All tests passed!" if self.fail_count == 0 else "ERROR: Some tests failed."
        return line1 + "\n" + line2

