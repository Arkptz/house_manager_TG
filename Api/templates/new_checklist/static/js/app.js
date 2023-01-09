var taskCounter = 0;
var tasks_count = 0;


function addTask() {
    tasks_count++;
    if (tasks_count > 0) { document.getElementById("tasks").style = "" }
    event.preventDefault();
    taskCounter++;
    let tr = document.createElement("tr");
    tr.id = "tsk" + taskCounter;
    let td1 = document.createElement("td");
    let td2 = document.createElement("td");
    td2.style.width = "50px";
    let new_task_field = document.createElement('input');
    new_task_field.className = "task_input";
    new_task_field.placeholder = "Проверка";
    new_task_field.name = 'task_' + tasks_count;
    let delete_btn = document.createElement("button");
    delete_btn.className = "del_task_btn";
    delete_btn.id = taskCounter;
    delete_btn.innerHTML = "×";
    delete_btn.addEventListener("click", remTask);
    td1.appendChild(new_task_field);
    td2.appendChild(delete_btn);
    tr.appendChild(td1);
    tr.appendChild(td2);
    document.getElementById("tasks").appendChild(tr);
}


function remTask() {
    tasks_count--;
    if (tasks_count == 0) { document.getElementById("tasks").style = "display: none;" }
    event.preventDefault();
    let tr = document.getElementById("tsk" + event.currentTarget.id);
    document.getElementById("tasks").removeChild(tr);
    let inputs = document.getElementsByClassName("task_input");
    for (let i = 0; i < inputs.length; i++)
        inputs[i].name = 'task_' + (i + 1);
}


function verifyFields() {
    if (document.getElementById("home_name").value == "") {
        event.preventDefault();
        document.getElementById("error_text").innerHTML = "Заполните поле \"Название дома\"";
        document.getElementById("error_div").style = "";
        return;
    }
    let checkboxes = document.getElementsByClassName("task_input");
    let checked = true;
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].value == '') {
            checked = false;
            break;
        }
    }
    if (checked == false) {
        event.preventDefault();
        document.getElementById("error_text").innerHTML = "Заполните все поля \"Проверка\"";
        document.getElementById("error_div").style = "";
    }
}

document.getElementById("error_div").addEventListener('click', () => {
    document.getElementById("error_div").style = "display: none;";
});


Telegram.WebApp.ready();
Telegram.WebApp.expand();

const initDataUnsafe = Telegram.WebApp.initDataUnsafe || {};

document.getElementById("id_fld").value = initDataUnsafe.user.id;
