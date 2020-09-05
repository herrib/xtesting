#!/usr/bin/env python
#
# Copyright (c) 2018 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

"""
Wrapper for launching Python test
"""

import logging
import subprocess
import time

from xtesting.core import testcase


class PythonTesting(testcase.TestCase):
    """Python test runner"""

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "test_url"
        super(PythonTesting, self).__init__(**kwargs)
        self.cmd = []
        self.result = 0
        self.start_time = 0
        self.stop_time = 0

    def run(self, **kwargs):
        "Run PythonTesting"
        self.start_time = time.time()
        try:
            self.run_pythontest()
            self.result = 100
            res = self.EX_OK
        except Exception:  # pylint: disable=broad-except
            res = self.EX_TESTCASE_FAILED
            self.__logger.exception("Error while running pythontest")
            self.result = 0
        self.stop_time = time.time()
        return res
    def run_pythontest(self):  # pylint: disable=too-many-branches
        """Run the test suites"""
        cmd_line = self.cmd
        self.__logger.info("Starting Python test: '%s'.", cmd_line)

        process = subprocess.Popen(cmd_line, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        output = process.stdout.read().decode("utf-8")
        result = eval(output)
        (OK, message, url) = result
        if OK:
            self.details="successful test: {} - url: {}".format(message, url)
        else:
            self.details = "unsuccessful test: {} - url: {}".format(message, url)



        # create a log file
        file_name = self.case_name + ".log"
        log_file = open(file_name, "w")
        log_file.write(output)
        log_file.close()

class Test1(PythonTesting):
    """Kubernetes smoke test suite"""
    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs.get("case_name", 'python-test1')
        super(Test1, self).__init__(**kwargs)
        self.cmd = ['python3', "/home/herve/PycharmProjects/xtesting/venv/test_url.py", "http://www.google.fr"]


test=Test1()
test.run()
#test.run_pythontest()
print ('le résultat est : {}'.format(test.is_successful()))
print ('la valeur est : {}'.format(test.details))