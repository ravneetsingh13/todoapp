// API endpoints
const API_ENDPOINTS = {
    CREATE: '/tasks',
    LIST: '/tasks',
    COMPLETED: '/tasks/completed',
    DELETE: (id) => `/tasks/${id}`,
    UPDATE: (id) => `/tasks/${id}`,
};

// Current view state
let currentTab = 'active';

// Utility functions
const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

const formatDateTime = (dateString) => {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

const formatDateForInput = (date) => {
    return date.toISOString().split('T')[0];
};

const showError = (message) => {
    alert(`Error: ${message}`);
};

// Deadline setting function
const setDeadline = (type) => {
    const deadlineInput = document.getElementById('taskDeadline');
    const today = new Date();
    
    if (type === 'today') {
        deadlineInput.value = formatDateForInput(today);
    } else if (type === 'tomorrow') {
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        deadlineInput.value = formatDateForInput(tomorrow);
    }
};

// Task management functions
async function createTask(taskData) {
    try {
        const response = await fetch(API_ENDPOINTS.CREATE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to create task');
        }

        await loadTasks();
        return true;
    } catch (error) {
        showError(error.message);
        return false;
    }
}

async function loadTasks() {
    try {
        let response;
        if (currentTab === 'completed') {
            response = await fetch(API_ENDPOINTS.COMPLETED);
        } else {
            response = await fetch(`${API_ENDPOINTS.LIST}?completed=false`);
        }

        if (!response.ok) {
            throw new Error('Failed to load tasks');
        }

        const data = await response.json();
        displayTasks(data.tasks);
    } catch (error) {
        showError(error.message);
    }
}

async function deleteTask(taskId) {
    try {
        const response = await fetch(API_ENDPOINTS.DELETE(taskId), {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error('Failed to delete task');
        }

        await loadTasks();
    } catch (error) {
        showError(error.message);
    }
}

async function updateTaskStatus(taskId, completed) {
    try {
        const response = await fetch(API_ENDPOINTS.UPDATE(taskId), {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ completed }),
        });

        if (!response.ok) {
            throw new Error('Failed to update task');
        }

        await loadTasks();
    } catch (error) {
        showError(error.message);
    }
}

// UI functions
function displayTasks(tasks) {
    const taskList = document.getElementById(
        currentTab === 'completed' ? 'completedTaskList' : 'activeTaskList'
    );
    taskList.innerHTML = '';

    if (tasks.length === 0) {
        taskList.innerHTML = '<p>No tasks found</p>';
        return;
    }

    tasks.forEach(task => {
        const taskElement = document.createElement('div');
        taskElement.className = `task-item ${task.completed ? 'completed' : ''}`;
        
        let completionInfo = '';
        if (task.completed && task.completed_at) {
            completionInfo = `<div class="completion-date">Completed on: ${formatDateTime(task.completed_at)}</div>`;
        }

        taskElement.innerHTML = `
            <div class="task-info">
                <h3>${task.name}</h3>
                <p>${task.description || 'No description'}</p>
                <p>Deadline: ${formatDate(task.deadline)}</p>
                ${completionInfo}
            </div>
            <div class="task-actions">
                ${currentTab === 'active' ? `
                    <input type="checkbox" 
                           ${task.completed ? 'checked' : ''} 
                           onchange="updateTaskStatus(${task.id}, this.checked)">
                ` : ''}
                <button class="delete" onclick="deleteTask(${task.id})">Delete</button>
            </div>
        `;
        
        taskList.appendChild(taskElement);
    });
}

function switchTab(tab) {
    currentTab = tab;
    
    // Update UI
    document.querySelectorAll('.tab').forEach(t => {
        t.classList.toggle('active', t.textContent.toLowerCase().includes(tab));
    });
    
    document.getElementById('activeTasks').style.display = 
        tab === 'active' ? 'block' : 'none';
    document.getElementById('completedTasks').style.display = 
        tab === 'completed' ? 'block' : 'none';
    
    // Load appropriate tasks
    loadTasks();
}

// Set default deadline to today when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Set default deadline to today
    const today = new Date();
    document.getElementById('taskDeadline').value = formatDateForInput(today);
    
    // Switch to active tab
    switchTab('active');
});

// Event Listeners
document.getElementById('taskForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const taskData = {
        name: document.getElementById('taskName').value,
        deadline: document.getElementById('taskDeadline').value,
        description: document.getElementById('taskDescription').value,
    };

    const success = await createTask(taskData);
    if (success) {
        e.target.reset();
        // Reset deadline to today after form submission
        setDeadline('today');
    }
});