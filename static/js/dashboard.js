// Funkcja obsługująca otwieranie modala
function openTaskDetailsModal(taskId) {
    const modal = document.getElementById("task-details-modal");
    modal.style.display = "block";

    fetch(`/tasks/${taskId}/details/`)
        .then(response => response.json())
        .then(data => {
            modal.querySelector("h2").innerText = `Task: ${data.name}`;
            modal.querySelector("p.description").innerText = `Description: ${data.description}`;

            const stepsList = modal.querySelector("ul.steps-list");
            stepsList.innerHTML = "";

            if (data.steps.length > 0) {
                data.steps.forEach(step => {
                    const listItem = document.createElement("li");
                    const checkbox = document.createElement("input");
                    checkbox.type = "checkbox";
                    checkbox.checked = step.is_completed;
                    checkbox.dataset.stepId = step.id;

                    // Obsługa zmiany stanu kroku
                    checkbox.addEventListener("change", function () {
                        toggleStepCompletion(step.id, this.checked, taskId);
                    });

                    listItem.appendChild(checkbox);
                    listItem.appendChild(document.createTextNode(` ${step.name}`));
                    stepsList.appendChild(listItem);
                });
            } else {
                stepsList.innerHTML = "<li>No steps added yet for this task.</li>";
            }
        })
        .catch(error => {
            console.error("Error fetching task details:", error);
        });
}

// Funkcja zamykająca modal
function closeTaskDetailsModal() {
    const modal = document.getElementById("task-details-modal");
    modal.style.display = "none";

    // Odśwież pasek postępu na głównym dashboardzie
    refreshProgressBars();
}

// Funkcja do zmiany stanu kroku
function toggleStepCompletion(stepId, isCompleted, taskId) {
    fetch(`/tasks/step/${stepId}/toggle/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ is_completed: isCompleted })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to update step status");
            }
            return response.json();
        })
        .then(data => {
            // Odśwież pasek postępu w modalnym oknie
            const modalProgress = document.querySelector("#modal-progress-bar");
            if (modalProgress) {
                modalProgress.style.width = `${data.progress}%`;
            }
        })
        .catch(error => {
            console.error("Error updating step status:", error);
        });
}

// Funkcja odświeżania pasków postępu na głównym dashboardzie
function refreshProgressBars() {
    fetch(`/tasks/progress/`)
        .then(response => response.json())
        .then(data => {
            data.forEach(task => {
                const progressBar = document.querySelector(`#progress-bar-${task.id}`);
                if (progressBar) {
                    progressBar.style.width = `${task.progress}%`;
                }
                const progressText = document.querySelector(`#progress-text-${task.id}`);
                if (progressText) {
                    progressText.textContent = `${task.progress}% Complete`;
                }
            });
        })
        .catch(error => {
            console.error("Error refreshing progress bars:", error);
        });
}


// Pobranie CSRF tokena
function getCSRFToken() {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split("=");
        if (name === "csrftoken") {
            return value;
        }
    }
    return null;
}

// Nasłuch na przycisk "View Details"
document.querySelectorAll(".details-btn").forEach(button => {
    button.addEventListener("click", function () {
        const taskId = this.dataset.taskId;
        openTaskDetailsModal(taskId);
    });
});

// Nasłuch na zamknięcie modala
document.querySelector(".close-btn").addEventListener("click", closeTaskDetailsModal);

// Zamknięcie modala po kliknięciu poza nim
window.addEventListener("click", function (event) {
    const modal = document.getElementById("task-details-modal");
    if (event.target === modal) {
        closeTaskDetailsModal();
    }
});
