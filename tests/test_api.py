import pytest


def test_basic_route_adding(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "Test"


def test_route_overlap_throws_exception(api):
    @api.route('/home')
    def home(req, resp):
        resp.text = "Test"

    with pytest.raises(AssertionError):
        @api.route('/home')
        def home2(req, resp):
            resp.text = "Test"


def test_client_can_send_requests(api, client):
    response_text = "THIS IS COOL"

    @api.route('/hey')
    def hey(req, resp):
        resp.text = response_text

    assert client.get('http://testserver/hey').text == response_text


def test_parameterized_route(api, client):
    @api.route('/{name}')
    def home(req, resp, name):
        resp.text = f'hello, {name}'

    assert client.get('http://testserver/kirill').text == 'hello, kirill'
    assert client.get('http://testserver/ivan').text == 'hello, ivan'


def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")

    assert response.status_code == 404
    assert response.text == "Not Found."


def test_class_based_handler_get(api, client):
    response_text = 'Test get'

    @api.route('/home')
    class Home:
        def get(self, req, resp):
            resp.text = response_text

    assert client.get('http://testserver/home').text == response_text


def test_class_based_handler_post(api, client):
    response_text = 'Test post'

    @api.route('/home')
    class Home:
        def post(self, req, resp):
            resp.text = response_text

    assert client.post('http://testserver/home').text == response_text


def test_class_based_handler_not_allowed_method(api, client):
    @api.route('/home')
    class Home:
        def post(self, req, resp):
            pass

    with pytest.raises(AttributeError):
        client.put('http://testserver/home')
