import os
import shutil
import unittest
from NixRawIO import NixRawIO
from neo.rawio.tests.common_rawio_test import BaseTestRawIO


testfname = "neoraw.nix"


class TestNixRawIO(BaseTestRawIO, unittest.TestCase, ):
    rawioclass = NixRawIO
    entities_to_test = [testfname]


if __name__ == "__main__":
    testfilepath = "/tmp/files_for_testing_neo/nix/"
    os.makedirs(testfilepath, exist_ok=True)
    shutil.copy(testfname, testfilepath)
    unittest.main()
