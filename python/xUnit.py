class TestCase:
    def __init__(self, name):
        self.name = name

    def setUp(self):
        pass

    def run(self, result):
        result.testStarted()

        self.setUp()
        try:
            exec "self." + self.name + "()"
        except:
            result.testFailed()
        self.tearDown()
        return result

    def tearDown(self):
        pass


class WasRun(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)

    def setUp(self):
        self.log = "setUp "

    def testMethod(self):
        self.log += "testMethod "

    def testBrokenMethod(self):
        raise Exception

    def tearDown(self):
        self.log += "tearDown "


class TestResult:
    def __init__(self):
        self.errorCount = 0
        self.runCount = 0

    def testStarted(self):
        self.runCount += 1

    def testFailed(self):
        self.errorCount += 1

    def summary(self):
        return "%d run, %d failed" % (self.runCount, self.errorCount)

    def addListener(self, listener):
        pass


class TestSuite:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)
        return result


class TestCaseTest(TestCase):
    def setUp(self):
        self.result = TestResult()

    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run(self.result)
        assert ("setUp testMethod tearDown " == test.log)

    def testResult(self):
        test = WasRun("testMethod")
        test.run(self.result)
        assert ("1 run, 0 failed" == self.result.summary())

    def testFailedResult(self):
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert ("1 run, 1 failed" == self.result.summary())

    def testFailedResultFormatting(self):
        self.result.testStarted()
        self.result.testFailed()
        assert ("1 run, 1 failed" == self.result.summary())

    def testSuite(self):
        self.suite = TestSuite()
        self.suite.add(WasRun("testMethod"))
        self.suite.add(WasRun("testBrokenMethod"))
        self.suite.run(self.result)
        assert ("2 run, 1 failed" == self.result.summary())


class ResultListenerTest():
    def testNotification(self):
        self.count = 0
        result = TestResult()
        result.addListener(self)
        WasRun("testMethod").run(result)
        assert 1 == self.count

    def startTest(self):
        self.count += 1


def main():
    # TestCaseTest("testSuite").run(TestResult())
    suite = TestSuite()
    suite.add(TestCaseTest("testTemplateMethod"))
    suite.add(TestCaseTest("testResult"))
    suite.add(TestCaseTest("testFailedResultFormatting"))
    suite.add(TestCaseTest("testFailedResult"))
    suite.add(TestCaseTest("testSuite"))
    result = TestResult()
    suite.run(result)
    print result.summary()


main()
