from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]
next_id = len(POSTS) + 1


def sort_posts(posts, sort_by, direction):
    pass


@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'GET':
        sort_by = request.args.get('sort')
        direction = request.args.get('direction')
        sorted_posts = POSTS[:]

        if sort_by or direction:
            if sort_by not in ['title', 'content']:
                return jsonify({'error': 'Invalid sort field.'}), 400
            if direction not in ['asc', 'desc']:
                return jsonify({'error': 'Invalid direction.'}), 400

            sort_posts(sorted_posts, sort_by, direction)

        return jsonify(sorted_posts), 200

    elif request.method == 'POST':
        if 'title' not in request.json or 'content' not in request.json:
            return jsonify({'error': 'Title and content are required.'}), 400

        title = request.json['title']
        content = request.json['content']

        new_post = {
            "id": len(POSTS) + 1,
            "title": title,
            "content": content
        }

        POSTS.append(new_post)

        return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE', 'PUT'])
def delete_or_update_post(id):
    if request.method == 'DELETE':
        for post in POSTS:
            if id == post['id']:
                POSTS.remove(post)
                return jsonify({'message': f'Post with id {id} has been deleted successfully.'}), 202
        return jsonify({'error': 'Post not found.'}), 404

    elif request.method == 'PUT':
        for post in POSTS:
            if id == post['id']:
                if 'title' in request.json:
                    post['title'] = request.json['title']
                if 'content' in request.json:
                    post['content'] = request.json['content']
                return jsonify(post), 200
        return jsonify({'error': 'Post not found.'}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_for_post():
    title_query = request.args.get('title')  # Get the title query parameter from the request URL
    content_query = request.args.get('content')  # Get the content query parameter from the request URL

    results = []  # List to store matching posts

    for post in POSTS:
        if title_query and title_query.lower() in post['title'].lower():
            results.append(post)
        elif content_query and content_query.lower() in post['content'].lower():
            results.append(post)

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
