const newTask = document.getElementById("newTaskField");
const task = document.getElementById("taskField");
const taskList = document.getElementById("taskList");
const addBtn = document.getElementById("addBtn");
const url = "http://localhost:8000/tasks";

function task_template(task_id, task_name) {
  const taskTemplate = `<div class="input-group mb-3">
                          <button type="button" class="btn btn-secondary" id="finishBtn${task_id}" onclick="renderTasks()">
                              Refresh
                          </button>
                          <input
                              type="text"
                              id="task${task_id}"
                              class="form-control"
                              aria-label="Text input with checkbox"
                              value="${task_name}"
                              readonly
                          />
                          <button type="button" class="btn btn-outline-success" id="finishBtn${task_id}" onclick="toggleTask(${task_id})">
                              Finished?
                          </button>
                          <button type="button" class="btn btn-primary" id="updateBtn${task_id}" onclick="updateTask('updateBtn${task_id}','task${task_id}')">
                              Update
                          </button>
                          <button type="button" class="btn btn-warning" id="expireBtn${task_id}" onclick="expireTask(${task_id}, 'expireBtn${task_id}')">
                              Due in 24H
                          </button>
                          <button type="button" class="btn btn-danger" id="deleteBtn${task_id}" onclick="deleteTask(${task_id})">
                              Delete
                          </button>
                        </div>`;
  return taskTemplate;
}
//NEW TASK: CREATE POOLING/WEBSOCKETS OR ADD REFRESH BUTTON
function checked_task_template(task_id, task_name) {
  const checkedTaskTemplate = `<div class="input-group mb-3">
                          <button type="button" class="btn btn-secondary" id="finishBtn${task_id}" onclick="renderTasks()">
                              Refresh
                          </button>
                          <input
                              type="text"
                              id="task${task_id}"
                              class="form-control"
                              aria-label="Text input with checkbox"
                              value="${task_name}"
                              readonly
                          />
                          <button type="button" class="btn btn-danger" id="finishChecked${task_id}" onclick="deleteTask(${task_id})">
                              Task Finished. Delete?
                          </button>
                          <button type="button" class="btn btn-warning" id="incompleteChecked${task_id}" onclick="toggleTask(${task_id})">
                              Incomplete?
                          </button>
                        </div>`;
  return checkedTaskTemplate;
}

function expired_task_template(task_id, task_name) {
  const expiredTaskTemplate = `<div class="input-group mb-3">
                                <input
                                    type="text"
                                    id="task${task_id}"
                                    class="form-control"
                                    aria-label="Text input with checkbox"
                                    value="${task_name}"
                                    readonly
                                />
                                <button type="button" class="btn btn-danger" id="expiredUpdateBtn${task_id}" onclick="deleteTask(${task_id})">
                                    Task Expired. Delete?
                                </button>
                              </div>`;
  return expiredTaskTemplate;
}

function getTasks() {
  return fetch(url)
    .then((response) => response.json())
    .catch((error) => console.log(error));
}

async function renderTasks() {
  let tasks = await getTasks();
  let html = "";
  tasks.forEach((task) => {
    if (task.task_status == "Task Expired") {
      let htmlSegments = expired_task_template(
        task.task_id,
        task.task_name + " (Expired)"
      );
      html += htmlSegments;
    } else if (task.checked) {
      let htmlSegments = checked_task_template(task.task_id, task.task_name);
      html += htmlSegments;
    } else {
      let htmlSegments = task_template(task.task_id, task.task_name);
      html += htmlSegments;
    }
  });
  taskList.innerHTML = html;
}

renderTasks();

addBtn.addEventListener("click", function () {
  if (newTask.value.length == 0) {
    alert("Enter a task");
  } else {
    renderTasks();
    add_task(newTask.value);
  }
});

function add_task(task_name) {
  const data = { task_name: task_name };
  fetch(url, {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "http://localhost:8000",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then(
      (data) => (taskList.innerHTML += task_template(data.task_id, data.value))
    )
    .catch((error) => {
      console.error("Error:", error);
    });
}

function updateTask(id, task) {
  const child = document.getElementById(id);
  const taskInput = document.getElementById(task);
  const task_id = child.id.match(/(\d+)/);
  if (child.innerText == "Update") {
    child.innerText = "Done";
    taskInput.readOnly = false;
  } else {
    child.innerText = "Update";
    taskInput.readOnly = true;
    const data = { task_name: taskInput.value };
    fetch(url + `/${task_id[0]}`, {
      method: "PUT",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "http://localhost:8000",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}

function toggleTask(task_id) {
  fetch(url + `/${task_id}/toggle`, {
    method: "POST",
  }).then(renderTasks);
}

function expireTask(task_id, expire) {
  const expireBtn = document.getElementById(expire);
  const data = { expire_after: 60 };
  fetch(url + `/${task_id}/expire`, {
    method: "PUT",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "http://localhost:8000",
    },
    body: JSON.stringify(data),
  }).then(() => renderTasks, (expireBtn.innerText = "Expiring"));
}

function deleteTask(task_id) {
  fetch(url + `/${task_id}`, {
    method: "DELETE",
  }).then(renderTasks);
}
