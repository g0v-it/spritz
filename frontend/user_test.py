#!/usr/bin/env python3
import unittest
import user

class user_test(unittest.TestCase):
    def test_insert(self):
        u = user.user_dto()
        u.user_name = 'test.user'
        u.pass_word = 'secret'
        user.delete_user_by_username(u.user_name)
        user.insert_user_dto(u)
        u1 = user.load_user_by_id(u.user_id)
        self.assertIsNotNone(u1)
        self.assertEqual(u.user_id, u1.user_id)
        self.assertEqual(u.user_name, u1.user_name)
        self.assertEqual(u.pass_word, u1.pass_word)
        user.delete_user_by_id(u.user_id)

    def test_delete_by_username(self):
        u = user.user_dto()
        u.user_name = 'test.delete.name'
        u.pass_word = 'secret'
        user.delete_user_by_username( u.user_name)
        user.insert_user_dto(u)
        user.delete_user_by_username( u.user_name)
        self.assertIsNone( user.load_user_by_username(u.user_name))
        
    def test_delete_by_id(self):
        u = user.user_dto()
        u.user_name = 'test.delete.id'
        u.pass_word = 'secret'
        user.delete_user_by_username( u.user_name)
        user.insert_user_dto(u)
        u1 = user.load_user_by_id(u.user_id)
        user.delete_user_by_id( u1.user_id)
        self.assertIsNone( user.load_user_by_id(u1.user_id))
        
    def test_load_by_username(self):
        u = user.user_dto()
        u.user_name = 'test.user'
        u.pass_word = 'secret'
        user.delete_user_by_username(u.user_name)
        user.insert_user_dto(u)
        u1 = user.load_user_by_username(u.user_name)
        self.assertIsNotNone(u1)
        self.assertEqual(u.user_id, u1.user_id)
        self.assertEqual(u.user_name, u1.user_name)
        self.assertEqual(u.pass_word, u1.pass_word)
        user.delete_user_by_id(u.user_id)
    def test_load_by_id(self):
        self.assertIsNone(user.load_user_by_id(999))
        

if __name__ == '__main__':
    unittest.main()
