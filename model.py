import re
import time
from tori.db.entity import entity
from tori.db.mapper import link, AssociationType as a, CascadingType as c

@link(
    target='model.Post',
    mapped_by='posts',
    inverted_by='tags',
    association=a.MANY_TO_MANY
)
@entity('tags')
class Tag(object):
    def __init__(self, label, posts=[]):
        self.label = label
        self.posts = posts

@link(
    target=Tag,
    association=a.MANY_TO_MANY,
    mapped_by='tags',
    cascading=[c.PERSIST]
)
@entity('posts')
class Post(object):
    def __init__(self, content, created_at=None, tags=[]):
        self.content = content
        self.tags = tags
        self.created_at = created_at or time.time()

    def structure(self):
        return re.split('\n{2,}', content)
