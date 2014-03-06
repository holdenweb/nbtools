#
# Tests for the O'Reilly Media "Intermediate Python" videos project
#
import os; print os.getcwd()

import unittest
import sanity

class TestStructure(unittest.TestCase):

    def setUp(self):
        root = sanity.Directory(".")
        self.rootdirs = set(root.dirs)
        self.roofiles = set(root.files)

    def test_for_directories(self):
        self.assertEqual(self.rootdirs,
                         {'data', 'figures', 'slides', 'tools', 'notebooks'})

if __name__ == "__main__":
    unittest.main()