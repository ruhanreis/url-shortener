import json
import unittest
import fakeredis

import app.url_shortener  as api


class ApiTests(unittest.TestCase):

    def setUp(self):
        api.r = r = fakeredis.FakeStrictRedis()
        self.app = api.app.test_client()

    def tearDown(self):
        pass

    def test_create_user(self):
        response = self.app.post(
                "/users"
            ,   data=json.dumps(dict(id='xyz'))
            ,   content_type='application/json' )

        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['id'], 'xyz')

        api.r.flushall()

    def test_create_user_error_409(self):
        self.app.post(
            "/users"
            , data=json.dumps(dict(id='xyz'))
            , content_type='application/json'
        )

        response = self.app.post(
            "/users"
            , data=json.dumps(dict(id='xyz'))
            , content_type='application/json'
        )

        self.assertEqual(response.status_code, 409)

        api.r.flushall()

    def test_create_user_error_400(self):
        response = self.app.post(
            "/users"
            , content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

        api.r.flushall()


    def test_delete_user(self):
        self.app.post(
            "/users"
            , data=json.dumps(dict(id='xyz'))
            , content_type='application/json'
        )

        response = self.app.delete("/user/xyz")
        self.assertEqual(response.status_code, 200)

        api.r.flushall()

    def test_delete_user_error(self):
        response = self.app.delete("/user/123")
        self.assertEqual(response.status_code, 404)

    def test_create_url(self):
        url = "www.teste.com.br"

        self.app.post(
            "/users"
            , data=json.dumps(dict(id='xyz'))
            , content_type='application/json')

        response = self.app.post(
            "/users/xyz/urls"
            , data=json.dumps(dict(url=url))
            , content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data[api.HITS_FIELD], 0)
        self.assertEqual(data[api.URL_FIELD], url)
        self.assertIsNotNone(data[api.SHORT_URL_FIELD])
        self.assertIsNotNone(data[api.ID_FIELD])

        api.r.flushall()

    def test_create_url_error_404(self):
        url = "www.teste.com.br"

        response = self.app.post(
            "/users/xyz/urls"
            , data=json.dumps(dict(url=url))
            , content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)

        api.r.flushall()

    def test_create_url_error_400(self):
        response = self.app.post(
            "/users/xyz/urls"
            , content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

        api.r.flushall()

    def test_get_stats(self):
        self.app.post(
            "/users"
            , data=json.dumps(dict(id='xyz'))
            , content_type='application/json')

        url = "www.teste.com.br"
        self.app.post(
            "/users/xyz/urls"
            , data=json.dumps(dict(url=url))
            , content_type='application/json'
        )

        response = self.app.get("/stats")

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["hits"], 0)
        self.assertEqual(data["urlCount"], 1)
        self.assertIsNotNone(data["topUrls"])

        api.r.flushall()

    def test_get_user_stats(self):
        self.app.post(
            "/users"
            , data=json.dumps(dict(id='xyz'))
            , content_type='application/json')

        url = "www.teste.com.br"
        self.app.post(
            "/users/xyz/urls"
            , data=json.dumps(dict(url=url))
            , content_type='application/json'
        )

        response = self.app.get("/users/xyz/stats")

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data[api.HITS_FIELD], 0)
        self.assertEqual(data["urlCount"], 1)
        self.assertIsNotNone(data["topUrls"])

        api.r.flushall()

    def test_get_user_stats_error(self):
        response = self.app.get("/users/xyz/stats")
        self.assertEqual(response.status_code, 404)

        api.r.flushall()

    def test_get_url_stats(self):
        self.app.post(
            "/users"
            , data=json.dumps(dict(id='xyz'))
            , content_type='application/json')

        url = "www.teste.com.br"
        url_response = self.app.post(
            "/users/xyz/urls"
            , data=json.dumps(dict(url=url))
            , content_type='application/json'
        )

        data = json.loads(url_response.get_data(as_text=True))
        id_url = data["id"]

        response = self.app.get("/stats/" + id_url)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data[api.HITS_FIELD], 0)
        self.assertEqual(data[api.URL_FIELD], url)
        self.assertEqual(data[api.ID_FIELD], id_url)
        self.assertIsNotNone(data[api.SHORT_URL_FIELD])

        api.r.flushall()

    def test_get_url_stats_error(self):
        response = self.app.get("/stats/123")
        self.assertEqual(response.status_code, 404)

        api.r.flushall()

    def test_delete_url(self):
        self.app.post(
            "/users"
            , data=json.dumps(dict(id='xyz'))
            , content_type='application/json')

        url = "www.teste.com.br"
        url_response = self.app.post(
            "/users/xyz/urls"
            , data=json.dumps(dict(url=url))
            , content_type='application/json'
        )

        data = json.loads(url_response.get_data(as_text=True))
        id_url = data["id"]

        response = self.app.delete("/urls/" + id_url)
        self.assertEqual(response.status_code, 200)

        api.r.flushall()

    def test_delete_url_error(self):
        response = self.app.delete("/urls/" + "123")
        self.assertEqual(response.status_code, 404)



