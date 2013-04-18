import re
from flask import Flask
from flask import render_template as rt
from flask import redirect, request
from tori.db.criteria import Criteria, Order
from tori.db.manager import Manager
from model import Post, Tag

app = Flask(__name__)
em  = Manager('tori_sample_blog')

@app.route('/')
def home():
    session = em.open_session()
    repo    = session.repository(Post)

    criteria = Criteria(order_by={'created_at': Order.DESC})
    posts    = repo.find(criteria)

    return rt('index.html', posts=posts)

@app.route('/tags/')
def tags():
    session = em.open_session()
    repo    = session.repository(Tag)

    criteria = Criteria(order_by={'label': Order.ASC})
    tags     = repo.find(criteria)

    return rt('tags.html', tags=tags)

@app.route('/tags/<label>')
def tag(label):
    session = em.open_session()
    repo    = session.repository(Tag)

    criteria = Criteria({'label': label}, limit=1)
    tag      = repo.find(criteria)

    return rt('tags.get.html', tag=tag)

@app.route('/post/new', methods=['GET'])
def post_new():
    return rt('post.new.html')

@app.route('/post/', methods=['POST'])
def post_create():
    session = em.open_session()
    posts   = session.repository(Post)
    tags    = session.repository(Tag)

    content  = re.sub('\r', '', request.form.get('content').strip())
    raw_tags = re.sub('\r', '', request.form.get('tags', '').strip())

    tag_entities = []

    for raw_tag in re.split('\s{1,}', raw_tags):
        tag = tags.find(Criteria({'label': raw_tag}, limit=1)) or Tag(label=raw_tag)
        tag_entities.append(tag)

    post = posts.new(content=content, tags=tag_entities)

    posts.post(post)

    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)