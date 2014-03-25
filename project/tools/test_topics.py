"""Test topic matching and the like"""
import os
import unittest

import lib
import topics

os.chdir(lib.get_project_dir())
topic_list = topics.get_topics()


class TestMatching(unittest.TestCase):
    
    def test_matching(self):
        title_list = "the quick brown fox".split()
        for word in title_list:
            self.assertTrue(topics.matching(word, title_list))
        for word in title_list:
            self.assertTrue(topics.matching(word[1:-1], title_list))
        self.assertTrue(topics.matching("", []))
        self.assertTrue(topics.matching("unicode", ["unicode?"]))
if __name__ == "__main__":
    unittest.main()