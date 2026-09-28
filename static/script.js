
const form = document.querySelector("#taskForm");
const taskList = document.querySelector("#taskList");


// ===============================
// ADD TASK
// ===============================

form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const title = document.querySelector("#title").value;
    const description = document.querySelector("#description").value;
    const priority = document.querySelector("#priority").value;

    const task = {
        title: title,
        description: description,
        priority: priority
    };

    const response = await fetch("/api/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(task)
    });

    const result = await response.json();

    console.log("Task created:", result);

    form.reset();

    loadTasks();
});


// ===============================
// DISPLAY ALL TASKS
// ===============================

async function loadTasks(filter = "all") {

    const response = await fetch("/api/tasks");

    const tasks = await response.json();
    let filteredTasks = tasks;

if (filter === "pending") {
    filteredTasks = tasks.filter(function(task) {
        return task.status === "pending";
    });
}

if (filter === "completed") {
    filteredTasks = tasks.filter(function(task) {
        return task.status === "completed";
    });
}

    taskList.innerHTML = "";

  filteredTasks.forEach(function(task)  {

        const li = document.createElement("li");

       const createdDate = new Date(task.created_at);

li.textContent =
    task.title +
    " | Priority: " +
    task.priority +
    " | Status: " +
    task.status +
    " | Created: " +
    createdDate.toLocaleString();


        // ===============================
        // COMPLETE BUTTON
        // ===============================

        if (task.status === "pending") {

            const button = document.createElement("button");

            button.textContent = "Complete";

            button.addEventListener("click", function() {
                completeTask(task.id);
            });

            li.appendChild(button);
        }


        // ===============================
        // DELETE BUTTON
        // ===============================

        const deleteButton = document.createElement("button");

        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", function() {
            deleteTask(task.id);
        });

        li.appendChild(deleteButton);


        taskList.appendChild(li);
    });
}


// ===============================
// COMPLETE TASK
// ===============================

async function completeTask(id) {

    const response = await fetch(`/api/tasks/${id}`, {
        method: "PUT"
    });

    const updatedTask = await response.json();

    console.log("Task updated:", updatedTask);

    loadTasks();
}


// ===============================
// DELETE TASK
// ===============================

async function deleteTask(id) {

    const response = await fetch(`/api/tasks/${id}`, {
        method: "DELETE"
    });

    const result = await response.json();

    console.log("Task deleted:", result);

    loadTasks();
}


// ===============================
// LOAD TASKS WHEN PAGE OPENS
// ===============================

document.querySelector("#allBtn").addEventListener("click", function() {
    loadTasks("all");
});

document.querySelector("#pendingBtn").addEventListener("click", function() {
    loadTasks("pending");
});

document.querySelector("#completedBtn").addEventListener("click", function() {
    loadTasks("completed");
});


loadTasks();
