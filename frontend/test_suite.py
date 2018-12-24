#!/usr/bin/env python3
import unittest
import user_test
import votation_test
import option_test
#import guarantor_test
import backend_test
import vote_test
import voter_test

test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(user_test.user_test))
test_suite.addTest(unittest.makeSuite(votation_test.votation_test))
test_suite.addTest(unittest.makeSuite(option_test.option_test))
#test_suite.addTest(unittest.makeSuite(guarantor_test.guarantor_test))
test_suite.addTest(unittest.makeSuite(vote_test.vote_test))
test_suite.addTest(unittest.makeSuite(voter_test.voter_test))

r = unittest.TextTestRunner()
r.run(test_suite)
