#!/usr/bin/env python3
import unittest
import shutil
import backend



class test_create_election(unittest.TestCase):
    def test_success(self):
        shutil.rmtree(backend.election_dir(999))
        result = backend.create_election(999,3,4)
        self.assertTrue(result)
    def test_fail(self):
        result = backend.create_election(999,3,4)
        result = backend.create_election(999,3,4)
        self.assertFalse(result)

class test_send_hash(unittest.TestCase):
    def test_send_ok(self):
        shutil.rmtree(backend.election_dir(999))
        result = backend.create_election(999,3,3)
        self.assertTrue(result)
        self.assertTrue(backend.guarantor_send_hash(999,1,"ciao"))
        self.assertTrue(backend.guarantor_send_hash(999,3,"ciao"))
        self.assertTrue(backend.guarantor_send_hash(999,2,"ciao"))

class test_send_passphrase(unittest.TestCase):
    def test_send_ok(self):
        shutil.rmtree(backend.election_dir(999))
        result = backend.create_election(999,3,3)
        self.assertTrue(result)
        self.assertTrue(backend.guarantor_send_hash(999,1,"ciao"))
        self.assertTrue(backend.guarantor_send_hash(999,2,"ciao"))
        self.assertTrue(backend.guarantor_send_hash(999,3,"ciao"))
        self.assertTrue(backend.candidate_send_passphrase(999,2,"ciao"))
        self.assertTrue(backend.candidate_send_passphrase(999,3,"ciao"))
        self.assertTrue(backend.candidate_send_passphrase(999,1,"ciao"))

class test_confirm_passphrase(unittest.TestCase):
    def test_confirm_ok(self):
        shutil.rmtree(backend.election_dir(999))
        result = backend.create_election(999,3,3)
        self.assertTrue(result)
        self.assertTrue(backend.guarantor_send_hash(999,1,"ciao"))
        self.assertTrue(backend.guarantor_send_hash(999,2,"ciao"))
        self.assertTrue(backend.guarantor_send_hash(999,3,"ciao"))
        self.assertTrue(backend.candidate_send_passphrase(999,3,"ciao"))
        self.assertTrue(backend.candidate_send_passphrase(999,2,"ciao"))
        self.assertTrue(backend.candidate_send_passphrase(999,1,"ciao"))
        self.assertTrue(backend.guarantor_confirm_passphrase(999,2,"ciao"))
        self.assertTrue(backend.guarantor_confirm_passphrase(999,1,"ciao"))
        self.assertTrue(backend.guarantor_confirm_passphrase(999,3,"ciao"))

class test_status(unittest.TestCase):
    def test_status(self):
        shutil.rmtree(backend.election_dir(999))
        result = backend.create_election(999,3,3)
        self.assertTrue(result)
        self.assertTrue(backend.guarantor_send_hash(999,1,"ciao"))
        self.assertTrue(backend.guarantor_send_hash(999,2,"ciao"))
        self.assertTrue(backend.guarantor_send_hash(999,3,"ciao"))
        self.assertTrue(backend.candidate_send_passphrase(999,3,"ciao"))
        self.assertTrue(backend.candidate_send_passphrase(999,2,"ciao"))
        self.assertTrue(backend.candidate_send_passphrase(999,1,"ciao"))
        self.assertTrue(backend.guarantor_confirm_passphrase(999,2,"ciao"))
        self.assertTrue(backend.guarantor_confirm_passphrase(999,1,"ciao"))
        self.assertTrue(backend.guarantor_confirm_passphrase(999,3,"ciao"))
        ar = backend.election_state(999)
        i = 0
        for s in ar:
            i = i + 1
            print("riga {}: {}".format(i,s))



if __name__ == '__main__':
    unittest.main()

