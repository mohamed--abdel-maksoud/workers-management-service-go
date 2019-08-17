import requests
import os
import unittest

BASE_URL = os.getenv('API_URL', 'http://localhost:8000')


class MarketsTest(unittest.TestCase):

    def test_get_employee(self):
        response = requests.get(f'{BASE_URL}/worker/ceo@mail.com')
        self.assertEqual(response.status_code, 200)
        try:
            payload = response.json()
        except ValueError:
            self.assertTrue(False, 'failed to decode the payload')
        self.assertIn('email', payload)
        self.assertEqual(payload['email'], 'ceo@mail.com')
        self.assertIn('tags', payload)
        self.assertIs(type(payload['tags']), list)
        self.assertIn('isContractor', payload)
        self.assertIs(type(payload['isContractor']), bool)
        self.assertFalse(payload['isContractor'])

    def test_get_contractor(self):
        response = requests.get(f'{BASE_URL}/worker/contractor@mail.com')
        self.assertEqual(response.status_code, 200)
        try:
            payload = response.json()
        except ValueError:
            self.assertTrue(False, 'failed to decode the payload')
        self.assertIn('email', payload)
        self.assertEqual(payload['email'], 'contractor@mail.com')
        self.assertIn('tags', payload)
        self.assertIs(type(payload['tags']), list)
        self.assertIn('isContractor', payload)
        self.assertIs(type(payload['isContractor']), bool)
        self.assertTrue(payload['isContractor'])

    def test_get_nonexisting_worker(self):
        response = requests.get(f'{BASE_URL}/worker/invalid-223412fa@aaaaa')
        self.assertEqual(response.status_code, 404)

    def test_update_contractor(self):
        contractor = {
            'email': 'contractor@mail.com',
            'name': 'john contractor smith',
            'isContractor': True,
            'contractEnd': '2050-11-30T15:04:05Z',
            'tags': ['mongodb', 'mysql', 'aws']
        }
        response = requests.put(f'{BASE_URL}/worker/', json=contractor)
        self.assertEqual(response.status_code, 200)
        try:
            payload = response.json()
        except ValueError:
            self.assertTrue(False, 'failed to decode the payload')
        self.assertIn('message', payload)
        self.assertEqual(payload['message'], 'OK')

        response = requests.get(f'{BASE_URL}/worker/contractor@mail.com')
        self.assertEqual(response.status_code, 200)
        try:
            payload = response.json()
        except ValueError:
            self.assertTrue(False, 'failed to decode the payload')

        for field in contractor:
            self.assertTrue(payload.get(field), contractor[field])

    def test_delete_employee(self):
        response = requests.delete(f'{BASE_URL}/worker/empl@mail.com')
        self.assertEqual(response.status_code, 200)
        try:
            payload = response.json()
        except ValueError:
            self.assertTrue(False, 'failed to decode the payload')
        self.assertIn('message', payload)
        self.assertEqual(payload['message'], 'OK')

        response = requests.get(f'{BASE_URL}/worker/empl@mail.com')
        self.assertEqual(response.status_code, 404)

    def test_create_contractor(self):
        contractor = {
            'email': 'contractor2@mail.com',
            'name': 'john contractor2 smith',
            'isContractor': True,
            'contractEnd': '2022-01-30T00:00:00Z',
            'tags': ['copywriting', 'seo']
        }
        response = requests.post(f'{BASE_URL}/worker/', json=contractor)
        self.assertEqual(response.status_code, 200)
        try:
            payload = response.json()
        except ValueError:
            self.assertTrue(False, 'failed to decode the payload')
        self.assertIn('message', payload)
        self.assertEqual(payload['message'], 'OK')

        response = requests.get(f'{BASE_URL}/worker/contractor2@mail.com')
        self.assertEqual(response.status_code, 200)
        try:
            payload = response.json()
        except ValueError:
            self.assertTrue(False, 'failed to decode the payload')

        for field in contractor:
            self.assertEqual(payload.get(field), contractor[field])

    def test_create_contractor_missing_contract_end(self):
        contractor = {
            'email': 'contractor-invalid@mail.com',
            'name': 'john contractor2 smith',
            'isContractor': True,
            'tags': ['copywriting', 'seo']
        }
        response = requests.post(f'{BASE_URL}/worker/', json=contractor)
        self.assertEqual(response.status_code, 400)

    def test_create_contractor_invalid_contract_end(self):
        contractor = {
            'email': 'contractor-invalid@mail.com',
            'name': 'john contractor2 smith',
            'isContractor': True,
            'contractEnd': 'Jan 31st, 2022',
            'tags': ['copywriting', 'seo']
        }
        response = requests.post(f'{BASE_URL}/worker/', json=contractor)
        self.assertEqual(response.status_code, 400)

    def test_create_contractor_with_job_title(self):
        contractor = {
            'email': 'contractor-invalid@mail.com',
            'name': 'john contractor2 smith',
            'isContractor': True,
            'contractEnd': '2022-01-30T00:00:00Z',
            'jobTitle': 'seo admin',
            'tags': ['copywriting', 'seo']
        }
        response = requests.post(f'{BASE_URL}/worker/', json=contractor)
        self.assertEqual(response.status_code, 400)

    def test_create_worker_with_missing_email(self):
        contractor = {
            'name': 'john contractor2 smith',
            'isContractor': True,
            'contractEnd': '2022-01-30T00:00:00Z',
            'tags': ['copywriting', 'seo']
        }
        response = requests.post(f'{BASE_URL}/worker/', json=contractor)
        self.assertEqual(response.status_code, 400)

    def test_create_employee(self):
        employee = {
            'email': 'empl2@mail.com',
            'name': 'john employee2 smith',
            'isContractor': False,
            'jobTitle': 'seo admin',
            'tags': ['copywriting', 'seo']
        }
        response = requests.post(f'{BASE_URL}/worker/', json=employee)
        self.assertEqual(response.status_code, 200)
        try:
            payload = response.json()
        except ValueError:
            self.assertTrue(False, 'failed to decode the payload')
        self.assertIn('message', payload)
        self.assertEqual(payload['message'], 'OK')

        response = requests.get(f'{BASE_URL}/worker/empl2@mail.com')
        self.assertEqual(response.status_code, 200)
        try:
            payload = response.json()
        except ValueError:
            self.assertTrue(False, 'failed to decode the payload')

        for field in employee:
            self.assertEqual(payload.get(field), employee[field])

    def test_create_employee_missing_job_title(self):
        employee = {
            'email': 'employee-invalid@mail.com',
            'name': 'john contractor2 smith',
            'isContractor': False,
            'tags': ['copywriting', 'seo']
        }
        response = requests.post(f'{BASE_URL}/worker/', json=employee)
        self.assertEqual(response.status_code, 400)

    def test_create_employee_with_contract_end(self):
        employee = {
            'email': 'employee-invalid@mail.com',
            'name': 'john contractor2 smith',
            'isContractor': False,
            'contractEnd': '2022-01-30T00:00:00Z',
            'jobTitle': 'seo admin',
            'tags': ['copywriting', 'seo']
        }
        response = requests.post(f'{BASE_URL}/worker/', json=employee)
        self.assertEqual(response.status_code, 400)

