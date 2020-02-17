from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# instantiate the APP
APP = Flask(__name__)
APP.config.from_object(__name__)

# enable CORS
CORS(APP, resources={r'/*': {'origins': '*'}})

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/tagging.sqlite3'
DB = SQLAlchemy(APP)


class Content(DB.Model):
    """ Represents main object """
    __tablename__ = 'content'
    id = DB.Column(DB.Integer, primary_key=True)
    type = DB.Column(DB.String(255))
    tags = DB.relationship('Tag', backref="content", lazy=False)

    def to_dict(self):
        """Serialisation"""
        return dict(id=self.id,
                    type=self.type,
                    tags=[tag.value for tag in self.tags])


class Tag(DB.Model):
    """ Represents tags associated to Content"""
    __tablename__ = 'tag'
    id = DB.Column(DB.Integer, primary_key=True)
    value = DB.Column(DB.String(255))
    content_id = DB.Column(DB.Integer, DB.ForeignKey("content.id"))

    def to_dict(self):
        """Serialisation"""
        return dict(id=self.id,
                    value=self.value)


@APP.route('/api/init')
def init_db():
    """ Initialisation sqlite database"""
    DB.create_all()
    return jsonify('DB init!')


@APP.route('/<object_type>/<object_id>', methods=['POST', 'DELETE'])
def content(object_type, object_id):
    """Insert or delete content"""
    response_object = {'status': 'success'}
    if request.method == 'POST':
        # Get tags from body
        post_data = request.get_json()
        post_data = list(map(lambda x: x.rstrip(), post_data))

        my_content = Content(id=object_id, type=object_type)
        DB.session.add(my_content)

        for data in post_data:
            # For each tag, reference the associated content
            tag = Tag(content=my_content, value=data)
            DB.session.add(tag)
        DB.session.commit()
        response_object['message'] = 'Content added!'
        return jsonify(response_object)

    elif request.method == 'DELETE':
        # Delete Content and all tags associated
        Content.query.filter_by(id=object_id).delete()
        Tag.query.filter_by(content_id=object_id).delete()
        DB.session.commit()
        return jsonify(response_object)
    else:
        return jsonify({'status': 'error'})


@APP.route('/<object_type>')
def search_by_tags(object_type):
    """ Search content by tags """
    response_object = {'status': 'success'}
    args = request.args
    # get tags from parameters
    lookup_tags = args.getlist('tags[]')

    # Lookup to all content id's
    content_ids = Tag.query.with_entities(Tag.content_id).filter(Tag.value.in_(lookup_tags)).all()
    content_ids = list(map(lambda x: x[0], content_ids))

    # Query corresponding contents
    contents = Content.query.filter(Content.id.in_(content_ids), Content.type.is_(object_type)).all()
    response_object['data'] = [s.to_dict() for s in contents]
    return jsonify(response_object)


@APP.route('/export')
def get_export():
    """ Export all content """
    response_object = {'status': 'success'}
    full = Content.query.all()
    response_object['data'] = [s.to_dict() for s in full]
    return jsonify(response_object)


@APP.route('/ping', methods=['GET'])
def ping_pong():
    """ Ping-pong"""
    return jsonify('pong!')


@APP.route('/', methods=['GET'])
def home():
    """ Home """
    return jsonify('Hello api!')


if __name__ == '__main__':
    APP.run(debug=True, host='0.0.0.0', port=5000)
