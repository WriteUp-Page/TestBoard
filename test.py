from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 데이터 저장을 위한 간단한 리스트
posts = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        password = request.form['password']
        post_id = len(posts) + 1
        posts.append({'id': post_id, 'title': title, 'content': content, 'password': password})
        return redirect(url_for('index'))
    return render_template('write.html')

@app.route('/post/<int:post_id>')
def read(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404
    return render_template('read.html', post=post)

@app.route('/edit_password/<int:post_id>', methods=['GET', 'POST'])
def edit_password(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        password = request.form['password']
        if post['password'] == password:
            return redirect(url_for('edit', post_id=post_id))
        else:
            return "Incorrect password", 403
    return render_template('edit_password.html', post_id=post_id)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        return redirect(url_for('read', post_id=post_id))
    return render_template('edit.html', post=post)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    global posts
    posts = [post for post in posts if post['id'] != post_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
