document.addEventListener("DOMContentLoaded", () => {
  const todoList = document.getElementById("todo-list");
  const titleInput = document.getElementById("title");
  const descriptionInput = document.getElementById("description");
  const addBtn = document.getElementById("add-btn");

  const apiUrl = "http://127.0.0.1:8000/todos/";

  // Fetch Todos from API and update the UI
  function fetchTodos() {
    fetch(apiUrl)
      .then(response => response.json())
      .then(todos => {
        todoList.innerHTML = "";
        todos.forEach(todo => {
          const li = document.createElement("li");
          li.textContent = `${todo.title}: ${todo.description || "No description"}`;
          const deleteBtn = document.createElement("button");
          deleteBtn.textContent = "Delete";
          deleteBtn.onclick = () => deleteTodo(todo.id);
          li.appendChild(deleteBtn);
          todoList.appendChild(li);
        });
      })
      .catch(error => console.error("Error fetching todos:", error));
  }

  // Create a new Todo
  function addTodo() {
    const title = titleInput.value.trim();
    const description = descriptionInput.value.trim();

    if (title) {
      fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, description }),
      })
      .then(response => response.json())
      .then(() => {
        fetchTodos();
        titleInput.value = "";
        descriptionInput.value = "";
      })
      .catch(error => console.error("Error adding todo:", error));
    } else {
      alert("Title cannot be empty");
    }
  }

  // Delete a Todo
  function deleteTodo(todoId) {
    fetch(`${apiUrl}${todoId}`, {
      method: "DELETE",
    })
    .then(() => fetchTodos())
    .catch(error => console.error("Error deleting todo:", error));
  }

  // Initialize
  addBtn.addEventListener("click", addTodo);
  fetchTodos();
});
