from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for tasks
tasks = []

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>To-Do App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .task-form {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .task-list {
            list-style: none;
            padding: 0;
        }
        .task-item {
            padding: 12px;
            margin-bottom: 8px;
            background: #f8f9fa;
            border-radius: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .delete-btn {
            background-color: #dc3545;
            padding: 5px 10px;
            font-size: 12px;
        }
        .delete-btn:hover {
            background-color: #c82333;
        }
        .version {
            text-align: center;
            color: #666;
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 To-Do List</h1>
        
        <form class="task-form" method="POST" action="/add">
            <input type="text" name="task" placeholder="Enter a new task" required>
            <button type="submit">Add Task</button>
        </form>
        
        <ul class="task-list">
            {% for i, task in enumerate(tasks) %}
            <li class="task-item">
                <span>{{ task }}</span>
                <form method="POST" action="/delete/{{ i }}" style="margin: 0;">
                    <button type="submit" class="delete-btn">Delete</button>
                </form>
            </li>
            {% endfor %}
        </ul>
        
        {% if not tasks %}
        <p style="text-align: center; color: #999;">No tasks yet. Add one above!</p>
        {% endif %}
        
        <div class="version">Version 1.0.0</div>
    </div>
</body>
</html>
"""  # noqa: W293


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, tasks=tasks, enumerate=enumerate)


@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        tasks.append(task)
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "healthy", "tasks_count": len(tasks)}, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7000)
