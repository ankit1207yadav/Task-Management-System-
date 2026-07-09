document.addEventListener("DOMContentLoaded", () => {
    const taskSelect = document.getElementById("task_title");
    const taskIdDisplay = document.getElementById("display-task-id");
    const empNameDisplay = document.getElementById("display-emp-name");
    const empIdDisplay = document.getElementById("display-emp-id");
    const completedSelect = document.getElementById("completed");

    /**
     * Updates UI detail nodes based on the currently selected task title.
     * @param {string} title The selected task title.
     */
    function updateTaskDetails(title) {
        if (!window.taskData) return;
        
        const task = window.taskData[title];
        if (task) {
            if (taskIdDisplay) taskIdDisplay.textContent = task.id || "-";
            if (empNameDisplay) empNameDisplay.textContent = task.emp_name || "None";
            if (empIdDisplay) empIdDisplay.textContent = task.emp_id || "-";
            if (completedSelect) completedSelect.value = task.completed || "false";
        }
    }

    // Attach listener and perform initial render
    if (taskSelect) {
        // Update elements on page load to align with initial selection
        updateTaskDetails(taskSelect.value);

        // Bind update handler to selection changes
        taskSelect.addEventListener("change", (event) => {
            updateTaskDetails(event.target.value);
        });
    }
});
