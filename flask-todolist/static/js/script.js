
// 本质上是两个数组
// 每次鼠标的点击都会将未完成的移动到已完成里
// 这里不需要任何主动的 render 因为 html 里监听每次操作都会 render
let todoList = [];
let completedList = [];

// 从 API 加载所有待办事项
async function loadTodos() {
    try {
        const response = await fetch('/api/todos');
        const data = await response.json();
        
        console.log('API 返回的数据:', data); // 调试信息
        
        // 🚀 存储完整对象而不是只存储文本
        todoList = data.pending;  // 保持原始对象结构
        completedList = data.completed;
        
        // 重新渲染
        renderTodoList();
    } catch (error) {
        console.error('加载待办事项失败:', error);
    }
}

// 添加新的待办事项
async function addTodo() {
    try {
      //这里要把新 todo 置顶
    const todoInput = document.querySelector('.add-button');
    const response = await fetch('/api/todos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task_content:'' })
    });

    if (response.ok) {
        // 2. 成功后重新加载数据
        await loadTodos();
    } else {
        console.error('添加失败');
    }
} catch (error) {
    console.error('添加待办项时出错:', error);
}
}




async function moveToCompleted(todoId) {
    try {
        // 1. 调用 API 更新状态为 completed
        const response = await fetch(`/api/todos/${todoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                status: 'completed'
            })
        });

        if (response.ok) {
            // 2. 成功后重新加载数据
            await loadTodos();
            console.log('标记完成成功！');
        } else {
            console.error('标记完成失败');
        }
    } catch (error) {
        console.error('标记完成时出错:', error);
    }
}

async function updateTodoContent(todoId, newContent) {
    try {
        const response = await fetch(`/api/todos/${todoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                task_content: newContent
            })
        });

        if (response.ok) {
            await loadTodos();
            console.log('编辑成功！');
        } else {
            console.error('编辑失败');
        }
    } catch (error) {
        console.error('编辑时出错:', error);
    }
}


//渲染
function renderTodoList() {
    const todoListElement = document.querySelector('.todo-list');
    todoListElement.innerHTML = '';
    
    // 渲染未完成任务
    todoList.forEach((todo) => {  // todo 现在是对象
        const todoItem = document.createElement('div');
        todoItem.classList.add('todo-item-not-completed');
        todoItem.innerHTML = `
            <input type="checkbox" class="todo-checkbox" data-id="${todo.id}">
            <input type="text" class="todo-input" value="${todo.task_content}" readonly data-id="${todo.id}">
        `;
        todoListElement.appendChild(todoItem);
    });
    
    // 渲染已完成区域
    const completedSection = document.createElement('div');
    completedSection.classList.add('completed-section');
    completedSection.innerHTML = '<div class="completed-title">已完成</div>';
    
    completedList.forEach(todo => {
        const todoItem = document.createElement('div');
        todoItem.classList.add('todo-item-completed');
        todoItem.innerHTML = `
            <input type="checkbox" class="todo-checkbox" checked disabled>
            <input type="text" class="todo-input" value="${todo.task_content}" readonly>
        `;
        completedSection.appendChild(todoItem);
    });
    
    todoListElement.appendChild(completedSection);
}
// 页面加载完成后加载数据
document.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成，开始加载数据...');
    loadTodos(); // 从数据库加载数据
});