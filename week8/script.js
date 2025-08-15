
// 本质上是两个数组
// 每次鼠标的点击都会将未完成的移动到已完成里
// 这里不需要任何主动的 render 因为 html 里监听每次操作都会 render
const todoList = [];
const completedList = [];

function addTodo() {
      //这里要把新 todo 置顶
    const todoInput = document.querySelector('.add-button');
    todoList.unshift('');
}

function moveToCompleted(todo) {
    // 移除 todoList 中的 todo
    todoList.splice(todoList.indexOf(todo), 1);
    // 将 todo 添加到 completedList 中
    completedList.unshift(todo);
    // 重新渲染
    renderTodoList();
}


//渲染
function renderTodoList() {
    const todoListElement = document.querySelector('.todo-list');
    todoListElement.innerHTML = '';
    
    // 渲染未完成任务 - 有点击事件
    todoList.forEach((todo, index) => {
        const todoItem = document.createElement('div');
        todoItem.classList.add('todo-item-not-completed');
        todoItem.innerHTML = `
            <input type="checkbox" class="todo-checkbox">
            <input type="text" class="todo-input" value="${todo}" readonly>
        `;
        
        
        todoListElement.appendChild(todoItem);
    });
    
    // 渲染已完成区域 - 无点击事件，纯展示
    const completedSection = document.createElement('div');
    completedSection.classList.add('completed-section');
    completedSection.innerHTML = '<div class="completed-title">已完成</div>';
    
    completedList.forEach(todo => {
        const todoItem = document.createElement('div');
        todoItem.classList.add('todo-item-completed');
        todoItem.innerHTML = `
            <input type="checkbox" class="todo-checkbox" checked disabled>
            <input type="text" class="todo-input" value="${todo}" readonly>
        `;
        // 🔥 注意：没有事件监听器，已完成项不可再次点击
        
        completedSection.appendChild(todoItem);
    });
    
    todoListElement.appendChild(completedSection);
}