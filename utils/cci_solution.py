from typing import List, Any
from .test_logger import TestLogger
from .test_case import TestCaseBase, TestRunBase

class CCISolution:
    from random import choice, randint
    from timeit import default_timer as now

    class TestCase(TestCaseBase): pass
    class TestRun(TestRunBase): pass
    class SolutionException(Exception): pass

    testcases = {"passed": [], "failed": []}
    runs = []

    def __init__(self, loglevel=TestLogger.INFO):
        self.logger = TestLogger(self.__class__, loglevel)

    def test(self):
        self.logger.debug("Running testcase...")
        start = self.now()
        testcase = self.generate_testcase()
        ret = None
        exc = None
        runtime = -1.0
        try:
            ret = self.solution(*testcase.args)
        except Exception as e:
            self.logger.error("Exception while running testcase: %s" % e)
            exc = e
        finally:
            run = self.TestRun(testcase, ret, exc, self.now() - start)
            title = "PASSED" if run.passed else "FAILED"
            self.logger.log({title: run._asdict()}, levels={
                    "runtime": self.logger.INFO,
                    "exception": self.logger.ERROR,
                    "returned": self.logger.INFO,
                    "expect": self.logger.INFO,
                    "args": self.logger.DEBUG
                }, conditions={
                    "exception": not run.passed,
                    "returned": not run.passed,
                    "expect": not run.passed
                })

            if run.passed:
                self.testcases["passed"].append(run.testcase)
            else:
                self.testcases["failed"].append(run.testcase)
            self.runs.append(run)
            return run

    def generate_testargs(self) -> List[Any]:
        raise NotImplementedException

    def get_answer(self) -> Any:
        raise NotImplementedException

    def generate_testcase(self) -> TestCaseBase:
        args = self.generate_testargs()
        ans = self.get_answer(*args)
        return self.TestCase(args=args, expect=ans)
