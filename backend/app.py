from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = "blog.db"


def init_db():
    """Initialize the database and create the posts table if it doesn't exist"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

@app.route("/posts", methods=["GET"])
def get_posts():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, content FROM posts ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        # Convert tuples → JSON objects
        posts = [
            {"id": r[0], "name": r[1], "content": r[2]}
            for r in rows
        ]

        return jsonify(posts), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/posts", methods=["POST"])
def add_post():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get("name", "").strip()
        content = data.get("content", "").strip()

        if not name or not content:
            return jsonify({"error": "Name and content are required"}), 400

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO posts (name, content) VALUES (?, ?)",
            (name, content)
        )

        conn.commit()
        post_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "message": "Post added successfully",
            "id": post_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/posts/<int:id>", methods=["PUT"])
def update_post(id):
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get("name", "").strip()
        content = data.get("content", "").strip()

        if not name or not content:
            return jsonify({"error": "Name and content are required"}), 400

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE posts SET name=?, content=? WHERE id=?",
            (name, content, id)
        )

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Post not found"}), 404

        conn.commit()
        conn.close()

        return jsonify({"message": "Post updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM posts WHERE id=?", (id,))

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Post not found"}), 404

        conn.commit()
        conn.close()

        return jsonify({"message": "Post deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    init_db()
    print("Starting Flask server on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
