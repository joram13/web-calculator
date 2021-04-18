import os
import unittest
import requests
from sqlalchemy import create_engine

class IntegrationTest(unittest.TestCase):

    def test_valid_expression(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression':'2+3'})
        self.assertEqual(r.status_code, 200)
    
    def test_invalid_expression(self):
        r = requests.post('http://127.0.0.1:5000/add', data = {'expression': 'er2'})
        self.assertNotEqual(r.status_code, 200)
    
    def test_db(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression':'100+100'})
        engine = create_engine('postgresql://cs162_user:cs162_password@127.0.0.1:5432/cs162', echo = True)

        with engine.connect() as con:
            rs = con.execute("SELECT * FROM Expression WHERE text = '100+100'")
            rows = rs.fetchall()

        self.assertNotEqual(len(rows), 0)

    
    def test_no_invalid_row_added(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression':'1+2'})
        engine = create_engine('postgresql://cs162_user:cs162_password@127.0.0.1:5432/cs162', echo = True)

        with engine.connect() as con:
            rs = con.execute("SELECT * FROM Expression")
            rows = rs.fetchall()
        
        r = requests.post('http://127.0.0.1:5000/add', data={'expression':'1+'})
        with engine.connect() as con:
            rs2 = con.execute("SELECT * FROM Expression")
            rows2 = rs.fetchall()
        
        self.assertEqual(rows == rows2)
