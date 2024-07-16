from flask import Blueprint, jsonify, request, make_response, current_app
from app.models import User, BlogPost, db
from app import bcrypt
import jwt
import uuid
from functools import wraps

blog_bp = Blueprint('blog', __name__)
@blog_bp.route('/')
def index():
    return "Welcome to the Blog API"

@blog_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    hashed_password = bcrypt.generate_password_hash(data['password']).decode()

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created!'}), 201

@blog_bp.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401)

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401)

    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({"public_id": user.public_id}, current_app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    return make_response('Could not verify', 401)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Extract the token from Authorization header

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception:
            return jsonify({'message': 'Error decoding token!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
@blog_bp.route('/blog', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.get_json()

    new_post = BlogPost(title=data['title'], content=data['content'], author=current_user.username, user_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'New post created!'})

@blog_bp.route('/blog', methods=['GET'])
def get_all_posts():
    posts = BlogPost.query.all()

    output = []
    for post in posts:
        post_data = {}
        post_data['id'] = post.id
        post_data['title'] = post.title
        post_data['content'] = post.content
        post_data['author'] = post.author
        output.append(post_data)

    return jsonify({'posts': output})

@blog_bp.route('/blog/<post_id>', methods=['GET'])
def get_post(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()

    if not post:
        return jsonify({'message': 'Post not found!'})

    post_data = {}
    post_data['id'] = post.id
    post_data['title'] = post.title
    post_data['content'] = post.content
    post_data['author'] = post.author

    return jsonify({'post': post_data})

@blog_bp.route('/blog/<post_id>', methods=['PUT'])
@token_required
def update_post(current_user, post_id):
    data = request.get_json()
    post = BlogPost.query.filter_by(id=post_id, user_id=current_user.id).first()
    if not post:
        return jsonify({'message': 'Post not found or you are not authorized!'})

    post.title = data['title']
    post.content = data['content']
    db.session.commit()

    return jsonify({'message': 'Post updated!'})


@blog_bp.route('/blog/<post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    post = BlogPost.query.filter_by(id=post_id, user_id=current_user.id).first()

    if not post:
        return jsonify({'message': 'Post not found or you are not authorized!'})

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted!'})