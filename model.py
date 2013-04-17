import re
import time
from tori.db.entity import entity
from tori.db.mapper import link, AssociationType as t

@link(
    target='model.Post',
    mapped_by='posts',
    inverted_by='tags',
    association=t.MANY_TO_MANY
)
@entity('tags')
class Tag(object):
    def __init__(self, label, posts=[]):
        self.label = label
        self.posts = posts

@link(
    target=Tag,
    association=t.MANY_TO_MANY,
    mapped_by='tags',
    read_only=True
)
@entity('posts')
class Post(object):
    def __init__(self, content, created_at=None, tags=[]):
        self.content = content
        self.tags = tags
        self.created_at = created_at or time.time()

    def structure(self):
        structure = {
            'title': '',
            'body': ''
        }

        content  = re.sub('<', '&lt;', re.sub('>', '&gt;', self.content))
        segments = re.split('\s{2,}', content)

        if len(segments) > 2:
            structure['title'] = segments.pop(0)

        structure['body']  = '<p>{}</p>'.format('</p><p>'.join(segments[1:]))
        
        return structure
