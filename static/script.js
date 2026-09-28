
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

    try {
        const response = await fetch("/api/tasks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(task)
        });

        const result = await response.json();

        // Handle API errors
        if (!response.ok) {
            alert(result.error);
            return;
        }

        console.log("Task created:", result);

        // Clear form
        form.reset();

        // Reload tasks
        loadTasks();

    } catch (error) {
        console.error("Error adding task:", error);
        alert("Unable to connect to the server.");
    }
});


// ===============================
// LOAD TASKS
// ===============================

async function loadTasks(filter = "all") {

    try {
        const response = await fetch("/api/tasks");

        const tasks = await response.json();

        // Handle API errors
        if (!response.ok) {
            alert(tasks.error);
            return;
        }

        // Clear current task list
        taskList.innerHTML = "";

        let filteredTasks = tasks;


        // ===============================
        // PENDING FILTER
        // ===============================

        if (filter === "pending") {

            filteredTasks = tasks.filter(function(task) {
                return task.status === "pending";
            });
        }


        // ===============================
        // COMPLETED FILTER
        // ===============================

        if (filter === "completed") {

            filteredTasks = tasks.filter(function(task) {
                return task.status === "completed";
            });
        }


        // ===============================
        // DISPLAY TASKS
        // ===============================

        filteredTasks.forEach(function(task) {

            const li = document.createElement("li");

            li.textContent =
                task.title +
                " | " +
                task.description +
                " | Priority: " +
                task.priority +
                " | Status: " +
                task.status;


            // ===============================
            // COMPLETE BUTTON
            // ===============================

            if (task.status === "pending") {

                const completeButton = document.createElement("button");

                completeButton.textContent = "Complete";

                completeButton.addEventListener("click", function() {
                    completeTask(task.id);
                });

                li.appendChild(completeButton);
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


            // Add task to page
            taskList.appendChild(li);
        });

    } catch (error) {

        console.error("Error loading tasks:", error);

        alert("Unable to connect to the server.");
    }
}


// ===============================
// COMPLETE TASK
// ===============================

async function completeTask(id) {

    try {

        const response = await fetch(`/api/tasks/${id}`, {
            method: "PUT"
        });

        const result = await response.json();

        // Handle API errors
        if (!response.ok) {
            alert(result.error);
            return;
        }

        console.log("Task updated:", result);

        // Reload tasks
        loadTasks();

    } catch (error) {

        console.error("Error completing task:", error);

        alert("Unable to connect to the server.");
    }
}


// ===============================
// DELETE TASK
// ===============================

async function deleteTask(id) {

    try {

        const response = await fetch(`/api/tasks/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        // Handle API errors
        if (!response.ok) {
            alert(result.error);
            return;
        }

        console.log("Task deleted:", result);

        // Reload tasks
        loadTasks();

    } catch (error) {

        console.error("Error deleting task:", error);

        alert("Unable to connect to the server.");
    }
}


// ===============================
// ALL TASKS BUTTON
// ===============================

document.querySelector("#allBtn").addEventListener("click", function() {

    loadTasks("all");

});


// ===============================
// PENDING TASKS BUTTON
// ===============================

document.querySelector("#pendingBtn").addEventListener("click", function() {

    loadTasks("pending");

});


// ===============================
// COMPLETED TASKS BUTTON
// ===============================

document.querySelector("#completedBtn").addEventListener("click", function() {

    loadTasks("completed");

});


// ===============================
// LOAD TASKS WHEN PAGE OPENS
// ===============================

loadTasks();

