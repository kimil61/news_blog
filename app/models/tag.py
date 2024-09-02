from app import db

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', secondary=post_tags, backref=db.backref('tags', lazy='dynamic'))

    @staticmethod
    def clean_tag_name(name):
        return name.strip().lower().replace('#', '')

    def __init__(self, *args, **kwargs):
        if 'name' in kwargs:
            kwargs['name'] = self.clean_tag_name(kwargs['name'])
        super(Tag, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Tag {self.name}>'