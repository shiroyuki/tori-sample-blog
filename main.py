from flask import Flask
from flask import render_template as rt
from tori.db.criteria import Criteria, Order
from tori.db.manager import Manager
from model import Post

app = Flask(__name__)
em  = Manager('tori_sample_blog')

@app.route('/')
def home():
    session = em.open_session()
    repo    = session.repository(Post)

    criteria = Criteria(order_by={'created_at': Order.DESC})
    posts    = repo.find(criteria)

    return rt('index.html', posts=posts)

@app.route('/post/', methods=['GET'])
def post():
    return

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)