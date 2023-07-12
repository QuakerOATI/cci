from typing import List, Any

class TestCaseBase(NamedTuple):
    args: List[Any]
    expect: Any

class TestRunBase(NamedTuple):
    testcase: TestCaseBase
    returned: Optional[Any]
    exception: Optional(Exception) = None
    runtime: float

    @property
    def passed(self) -> bool:
        return self.exception is None and self.returned == self.testcase.expect

    def _get_summary(self):
        summary = [f"runtime: {self.runtime}"]

    def log(self, logger):
        if self.passed:
            logger.info("PASSED")
        else:
            logger.error("FAILED")

