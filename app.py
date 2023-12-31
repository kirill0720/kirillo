from api import API

app = API()


@app.route('/home')
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route('/about')
def about(request, response):
    response.text = "Hello from the ABOUT page"


@app.route('/hello/{name}')
def hello(request, response, name):
    print(app.routes)
    response.text = f"Hello {name}!"


@app.route('/hello/{surname}')
def index(request, response, surname):
    response.text = f"Hello2 {surname}!"


@app.route('/welcome/{name}//{surname}')
def hello_full(request, response, name, surname):
    response.text = f"Welcome {name} {surname}!"


@app.route("/sum/{num_1:d}/{num_2:d}")
def _sum(request, response, num_1, num_2):
    total = int(num_1) + int(num_2)
    response.text = f"{num_1} + {num_2} = {total}"


@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

    def put(self, req, resp):
        resp.text = "Endpoint to update a book"

    def delete(self, req, resp):
        resp.text = "Endpoint to delete a book"


def handler(req, resp):
    resp.text = 'Sample'


app.add_route('/sample', handler)


@app.route('/template')
def template_handler(req, resp):
    resp.body = app.template('index.html', context={"name": "Kirillo", "title": "Best Framework"}).encode()


def custom_exception_handler(req, resp, exc):
    resp.text = str(exc)


app.add_exception_handler(custom_exception_handler)


@app.route('/exception')
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be used.")
