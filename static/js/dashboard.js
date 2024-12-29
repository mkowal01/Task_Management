// Funkcja obsługująca otwieranie modala
function openTaskDetailsModal(taskId) {
    // Pobranie modala i ustawienie go jako widoczny
    const modal = document.getElementById("task-details-modal");
    modal.style.display = "block";

    // Pobranie zawartości szczegółów zadania
    fetch(`/tasks/${taskId}/details/`) // Przyjmuje URL endpointa Django
        .then(response => response.json())
        .then(data => {
            // Wypełnienie szczegółów zadania w modalnym oknie
            modal.querySelector("h2").innerText = `Task: ${data.name}`;
            modal.querySelector("p.description").innerText = `Description: ${data.description}`;

            // Wypełnienie kroków zadania
            const stepsList = modal.querySelector("ul.steps-list");
            stepsList.innerHTML = ""; // Czyszczenie listy przed załadowaniem nowych danych

            if (data.steps.length > 0) {
                data.steps.forEach(step => {
                    const listItem = document.createElement("li");
                    const checkbox = document.createElement("input");
                    checkbox.type = "checkbox";
                    checkbox.checked = step.is_completed;
                    checkbox.dataset.stepId = step.id;

                    // Obsługa zmiany stanu kroku
                    checkbox.addEventListener("change", function () {
                        toggleStepCompletion(step.id, this.checked);
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
}

// Funkcja do zmiany stanu kroku
function toggleStepCompletion(stepId, isCompleted) {
    fetch(`/tasks/step/${stepId}/toggle/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(), // Pobieranie CSRF tokena z ciasteczka
        },
        body: JSON.stringify({ is_completed: isCompleted })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to update step status");
            }
        })
        .catch(error => {
            console.error("Error updating step status:", error);
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

// Dodanie nasłuchu na kliknięcia przycisków "View Details"
document.querySelectorAll(".details-btn").forEach(button => {
    button.addEventListener("click", function () {
        const taskId = this.dataset.taskId;
        openTaskDetailsModal(taskId);
    });
});

// Dodanie nasłuchu na zamykanie modala
document.querySelector(".close-btn").addEventListener("click", closeTaskDetailsModal);

// Obsługa zamykania modala po kliknięciu poza nim
window.addEventListener("click", function (event) {
    const modal = document.getElementById("task-details-modal");
    if (event.target === modal) {
        closeTaskDetailsModal();
    }
});
