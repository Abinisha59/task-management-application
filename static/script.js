
const form = document.querySelector("#taskForm");
const taskList = document.querySelector("#taskList");
const searchInput = document.querySelector("#searchInput");
const titleInput = document.querySelector("#title");
const descriptionInput = document.querySelector("#description");
const priorityInput = document.querySelector("#priority");
const dueDateInput = document.querySelector("#due_date");

const allBtn = document.querySelector("#allBtn");
const pendingBtn = document.querySelector("#pendingBtn");
const completedBtn = document.querySelector("#completedBtn");

const totalTasksElement = document.querySelector("#totalTasks");
const pendingTasksElement = document.querySelector("#pendingTasks");
const completedTasksElement = document.querySelector("#completedTasks");

const filterButtons = [allBtn, pendingBtn, completedBtn];

let allTasks = [];
let currentFilter = "all";

// Read JSON safely and handle non-JSON server responses.
async function readResponse(response) {
    const text = await response.text();

    if (!text) {
        return {};
    }

    try {
        return JSON.parse(text);
    } catch {
        return { error: "The server returned an unexpected response." };
    }
}

// Display an error without exposing internal server details.
function showError(message) {
    alert(message || "Something went wrong. Please try again.");
}

// ---------- ADD TASK ----------
form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const title = titleInput.value.trim();
    const description = descriptionInput.value.trim();
    const priority = priorityInput.value;
    const dueDate = dueDateInput.value;

    if (!title) {
        showError("Please enter a task title.");
        titleInput.focus();
        return;
    }

    if (!priority) {
        showError("Please select a priority.");
        priorityInput.focus();
        return;
    }

    const task = {
        title: title,
        description: description,
        priority: priority,
        due_date: dueDate || null
    };

    const submitButton = form.querySelector('[type="submit"]');

    try {
        submitButton.disabled = true;

        const response = await fetch("/api/tasks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(task)
        });

        const result = await readResponse(response);

        if (!response.ok) {
            showError(result.error || "Unable to create task.");
            return;
        }

        form.reset();
        currentFilter = "all";
        await loadTasks();

    } catch (error) {
        console.error("Error adding task:", error);
        showError("Unable to connect to the server.");
    } finally {
        submitButton.disabled = false;
    }
});

// ---------- LOAD TASKS ----------
async function loadTasks() {
    try {
        const response = await fetch("/api/tasks");
        const result = await readResponse(response);

        if (!response.ok) {
            showError(result.error || "Unable to load tasks.");
            return;
        }

        if (!Array.isArray(result)) {
            showError("The server returned an invalid task list.");
            return;
        }

        allTasks = result;
        updateStatistics();
        renderTasks();

    } catch (error) {
        console.error("Error loading tasks:", error);
        showError("Unable to load tasks. Check the server connection.");
    }
}

// ---------- UPDATE STATISTICS ----------
function updateStatistics() {
    const total = allTasks.length;
    const completed = allTasks.filter(
        task => task.status === "completed"
    ).length;
    const pending = allTasks.filter(
        task => task.status === "pending"
    ).length;

    totalTasksElement.textContent = total;
    pendingTasksElement.textContent = pending;
    completedTasksElement.textContent = completed;
}

// ---------- DUE DATE INFORMATION ----------
function getDueDateInfo(task) {
    if (!task.due_date) {
        return null;
    }

    // Parse YYYY-MM-DD as a local calendar date to avoid
    // timezone-related date shifts.
    const parts = task.due_date.split("-").map(Number);

    if (
        parts.length !== 3 ||
        parts.some(number => !Number.isInteger(number)) ||
        parts[0] < 1 ||
        parts[1] < 1 || parts[1] > 12 ||
        parts[2] < 1 || parts[2] > 31
    ) {
        return { text: "Invalid due date", className: "due-upcoming" };
    }

    const dueDate = new Date(parts[0], parts[1] - 1, parts[2]);

    if (
        dueDate.getFullYear() !== parts[0] ||
        dueDate.getMonth() !== parts[1] - 1 ||
        dueDate.getDate() !== parts[2]
    ) {
        return { text: "Invalid due date", className: "due-upcoming" };
    }

    const today = new Date();
    const localToday = new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate()
    );

    if (task.status === "completed") {
        return {
            text: "Completed",
            className: "due-completed"
        };
    }

    if (dueDate < localToday) {
        return {
            text: "Overdue",
            className: "overdue"
        };
    }

    if (dueDate.getTime() === localToday.getTime()) {
        return {
            text: "Due today",
            className: "due-today"
        };
    }

    return {
        text: "Due " + dueDate.toLocaleDateString(),
        className: "due-upcoming"
    };
}

// ---------- RENDER TASKS ----------
function renderTasks() {
    const searchTerm = searchInput.value.trim().toLowerCase();

    let filteredTasks = allTasks.filter(function (task) {
        const matchesFilter =
            currentFilter === "all" ||
            task.status === currentFilter;

        const matchesSearch =
            (task.title || "").toLowerCase().includes(searchTerm) ||
            (task.description || "").toLowerCase().includes(searchTerm);

        return matchesFilter && matchesSearch;
    });

    filterButtons.forEach(function (button) {
        button.classList.toggle(
            "active",
            button.id === currentFilter + "Btn"
        );
    });

    taskList.replaceChildren();

    if (filteredTasks.length === 0) {
        const emptyMessage = document.createElement("li");
        emptyMessage.className = "empty-state";
        emptyMessage.textContent = searchTerm
            ? "No tasks match your search."
            : "No tasks here yet. Add a task to get started.";

        taskList.appendChild(emptyMessage);
        return;
    }

    filteredTasks.forEach(function (task) {
        const li = document.createElement("li");

        const heading = document.createElement("h3");
        heading.textContent = task.title;
        li.appendChild(heading);

        const description = document.createElement("p");
        description.textContent =
            task.description || "No description provided.";
        li.appendChild(description);

        const taskMeta = document.createElement("div");
        taskMeta.className = "task-meta";

        addBadge(taskMeta, "Priority: " + task.priority,
            (task.priority || "").toLowerCase());

        addBadge(
            taskMeta,
            task.status === "completed" ? "Completed" : "Pending",
            task.status === "completed" ? "due-completed" : "due-upcoming"
        );

        const dueInfo = getDueDateInfo(task);

        if (dueInfo) {
            addBadge(taskMeta, dueInfo.text, dueInfo.className);
        }

        li.appendChild(taskMeta);

        if (task.status === "pending") {
            const completeButton = document.createElement("button");
            completeButton.type = "button";
            completeButton.textContent = "Mark Complete";

            completeButton.addEventListener("click", function () {
                completeTask(task.id, completeButton);
            });

            li.appendChild(completeButton);
        }

        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", function () {
            deleteTask(task.id, deleteButton);
        });

        li.appendChild(deleteButton);
        taskList.appendChild(li);
    });
}

// Create badges safely using textContent.
function addBadge(container, text, className) {
    const badge = document.createElement("span");
    badge.className = "task-badge " + className;
    badge.textContent = text;
    container.appendChild(badge);
}

// ---------- COMPLETE TASK ----------
async function completeTask(id, button) {
    try {
        button.disabled = true;

        const response = await fetch(`/api/tasks/${id}`, {
            method: "PUT"
        });

        const result = await readResponse(response);

        if (!response.ok) {
            showError(result.error || "Unable to complete task.");
            return;
        }

        await loadTasks();

    } catch (error) {
        console.error("Error completing task:", error);
        showError("Unable to connect to the server.");
    } finally {
        button.disabled = false;
    }
}

// ---------- DELETE TASK ----------
async function deleteTask(id, button) {
    if (!confirm("Are you sure you want to delete this task?")) {
        return;
    }

    try {
        button.disabled = true;

        const response = await fetch(`/api/tasks/${id}`, {
            method: "DELETE"
        });

        const result = await readResponse(response);

        if (!response.ok) {
            showError(result.error || "Unable to delete task.");
            return;
        }

        await loadTasks();

    } catch (error) {
        console.error("Error deleting task:", error);
        showError("Unable to connect to the server.");
    } finally {
        button.disabled = false;
    }
}

// ---------- FILTER BUTTONS ----------
allBtn.addEventListener("click", function () {
    currentFilter = "all";
    renderTasks();
});

pendingBtn.addEventListener("click", function () {
    currentFilter = "pending";
    renderTasks();
});

completedBtn.addEventListener("click", function () {
    currentFilter = "completed";
    renderTasks();
});

// ---------- SEARCH ----------
searchInput.addEventListener("input", renderTasks);

// ---------- INITIAL LOAD ----------
loadTasks();
