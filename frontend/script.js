const API = "http://backend-service:30007/posts";

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
function addPost() {
    const name = document.getElementById("name").value.trim();
    const content = document.getElementById("content").value.trim();

    if (!name) {
        alert("Please enter your name!");
        return;
    }

    if (!content) {
        alert("Please write something in your post!");
        return;
    }

    fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, content })
    })
    .then(res => res.json())
    .then(() => {
        document.getElementById("name").value = "";
        document.getElementById("content").value = "";
        loadPosts();
    })
    .catch(err => {
        console.error(err);
        alert("Failed to add post.");
    });
}

function deletePost(id) {
    if (!confirm("Delete this post?")) return;

    fetch(`${API}/${id}`, { method: "DELETE" })
        .then(res => res.json())
        .then(loadPosts)
        .catch(err => console.error(err));
}

function editPost(id, oldName, oldContent) {

    const name = prompt("Edit name:", oldName);
    if (name === null) return;

    const content = prompt("Edit content:", oldContent);
    if (content === null) return;

    if (!name.trim() || !content.trim()) {
        alert("Fields cannot be empty");
        return;
    }

    fetch(`${API}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: name.trim(),
            content: content.trim()
        })
    })
    .then(res => res.json())
    .then(loadPosts)
    .catch(err => console.error(err));
}
function loadPosts() {
    fetch(API)
    .then(res => res.json())
    .then(data => {

        const postsDiv = document.getElementById("posts");
        postsDiv.innerHTML = "";

        if (data.length === 0) {
            postsDiv.innerHTML = `
                <div class="empty-state">
                    <p>📭 No posts yet!</p>
                    <p style="font-size:14px;color:#bbb;">Be the first to write something.</p>
                </div>`;
            return;
        }

        data.forEach(post => {

            const postId = post.id;
            const postName = escapeHtml(post.name);
            const postContent = escapeHtml(post.content);

            const safeName = postName.replace(/'/g, "\\'");
            const safeContent = postContent.replace(/'/g, "\\'");

            const postBox = document.createElement("div");
            postBox.className = "post";

            postBox.innerHTML = `
                <div class="post-header">
                    <div class="post-name">👤 ${postName}</div>
                </div>

                <div class="post-content">${postContent}</div>

                <div class="actions">
                    <button class="btn-edit"
                        onclick="editPost(${postId}, '${safeName}', '${safeContent}')">
                        ✏️ Edit
                    </button>

                    <button class="btn-delete"
                        onclick="deletePost(${postId})">
                        🗑️ Delete
                    </button>
                </div>
            `;

            postsDiv.appendChild(postBox);
        });
    })
    .catch(err => {
        console.error("Load error:", err);
    });
}

loadPosts();
