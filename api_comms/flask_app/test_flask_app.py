import json
import unittest
from app import app


class AppTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_page_get(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_register_page_post(self):
        data = {
            'username': 'myName',
            'password': "12345678",
            'email': '123456@gmail.com'
        }
        response = self.app.get('/register', follow_redirects=True, data=data)
        self.assertEqual(response.status_code, 200)

    def test_login_page_get(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_page_post(self):
        data = {
            'username': 'admin',
            'password': "admin",
        }
        response = self.app.get('/login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_raw_report_page_get(self):
        data = {'username': 'admin'}
        response = self.app.get('/raw_report', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_raw_report_page_post(self):
        data = {
            'name': 'Walmart',
            'cik': '12345678',
            'report_date': '2021-04-02',
            'username': 'admin'
        }

        response = self.app.get('/raw_report', data=data,
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_generated_report_page_get(self):
        data = {'username': 'admin'}
        response = self.app.get('/generated_report', data=data,
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_report_analysis_page_get(self):
        data = {}
        response = self.app.get('/analysis/report', data=data,
                                follow_redirects=True)
        self.assertTrue(response is not None)

    def test_reorganize_reports(self):
        report = {
            "name": "report_name",
            "id": -1,
            "json_schema": "{\"Document And Entity Information\": {\"Nov. 26, 2016 - 12 Months Ended\": {\"Document "
                           "Information [Line Items] - CATEGORY\": 0.0}, \"Jan. 06, 2017\": {\"Document Information ["
                           "Line Items] - CATEGORY\": 0.0}, \"May 28, 2016\": {\"Document Information [Line Items] - "
                           "CATEGORY\": 0.0}, \"Nov. 28, 2015 - 12 Months Ended\": {\"Document Information [Line "
                           "Items] - CATEGORY\": 0.0}, \"Jan. 08, 2016\": {\"Document Information [Line Items] - "
                           "CATEGORY\": 0.0}, \"May. 30, 2015\": {\"Document Information [Line Items] - CATEGORY\": "
                           "0.0}}, \"Consolidated Balance Sheets\": {\"2016-11-26\": {\"Current assets - CATEGORY\": "
                           "0.0}, \"2015-11-28\": {\"Current assets - CATEGORY\": 0.0}, \"2015-11-28 dp_1\": {"
                           "\"Current assets - CATEGORY\": 0.0}, \"2014-11-29\": {\"Current assets - CATEGORY\": "
                           "0.0}}} "
        }

        response = self.app.get('/reorganize_report',
                                query_string={'report': report},
                                follow_redirects=True)
        self.assertTrue(response is not None)

    def test_view_generated_report(self):
        sheets = [
            {
                'name': 'Document And Entity Information',
                'headers': [
                    'Index',
                    'Nov. 26, 2016 - 12 Months Ended',
                    'Jan. 06, 2017',
                    'May 28, 2016',
                    'Nov. 28, 2015 - 12 Months Ended',
                    'Jan. 08, 2016',
                    'May. 30, 2015'
                ],
                'rows': {
                    'Document Information [Line Items] - CATEGORY': [
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0
                    ]
                }
            },
            {
                'name': 'Consolidated Balance Sheets',
                'headers': [
                    'Index',
                    '2016-11-26',
                    '2015-11-28',
                    '2015-11-28 dp_1',
                    '2014-11-29'
                ],
                'rows': {
                    'Current assets - CATEGORY': [0.0, 0.0, 0.0, 0.0]
                }
            }
        ]

        response = self.app.get('/generated_report/test-11',
                                data={'report_name': 'test', 'report_id': 11},
                                query_string={'sheets': json.dumps(sheets)},
                                follow_redirects=True)
        self.assertTrue(response is not None)

    def test_report_generation_get(self):
        response = self.app.get('/report_generation',
                                follow_redirects=True)
        self.assertTrue(response is not None)

    def test_report_generation_post(self):
        data = {'report_name': 'report_name', 'company': 'Bassett', 'cik': '0000010329',
                'years': '2021,2020,2019,2018', 'type': 'json'}

        response = self.app.post(
            '/report_generation',
            data=data
        )
        self.assertTrue(response is not None)


class GeneratedReportAnalysisTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def test_analysis_endpoint_has_response(self):
        report_id = 1

        response = self.app.post(
            f'/generated_report/analysis/{report_id}'
        )

        self.assertTrue(response is not None)

    def test_analysis_endpoint_forbidden(self):
        report_id = 1

        not_logged_in = self.app.post(
            f'/generated_report/analysis/{report_id}'
        )

        with self.app as client:
            with client.session_transaction() as sess:
                sess['username'] = 'patrick'
                sess['password'] = 'incorrect'

        wrong_user = self.app.post(
             f'/generated_report/analysis/{report_id}'
        )

        self.assertEqual(403, not_logged_in.status_code)
        self.assertEqual(403, wrong_user.status_code)

    def test_analysis_endpoint_not_found(self):
        report_id = 0

        with self.app as client:
            with client.session_transaction() as sess:
                sess['username'] = 'admin'
                sess['password'] = 'admin'

        response = self.app.post(
            f'/generated_report/analysis/{report_id}'
        )

        self.assertEqual(404, response.status_code)

    def test_analysis_endpoint_ok(self):
        report_id = 1

        with self.app as client:
            with client.session_transaction() as sess:
                sess['username'] = 'admin'
                sess['password'] = 'admin'

        response = self.app.post(
            f'/generated_report/analysis/{report_id}'
        )

        self.assertEqual(302, response.status_code)


if __name__ == "__main__":
    unittest.main()
