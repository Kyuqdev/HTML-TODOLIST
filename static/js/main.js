var todoItems = [];
let deleteMode = false;

//* puts all of the todos in the list
function renderTodos() {

    //* get the todo list item in html
    const todoList = document.getElementById('todo-list');

    //* clear it of any previous values
    todoList.innerHTML = '';

    //? for each todo item, loop again and make a new list item
    //! (it's like for i in range in python)
    for (let i = 0; i < todoItems.length; i++) {

        //* get the current item of the loop aka our todo item that we'll be adding
        const todo = todoItems[i];

        //* create a new list item in our html list
        const li = document.createElement('li');

        //? add a id to the list item (optional but useful for styling and testing in case you need any later down the road)
        li.id = 'todo-' + i;

        //! set the text of the html item to the text of the todo item (the text set under the "text" parameter in our json)
        li.innerHTML = todo.text;

        //* if the parameter "done" is set to true in our json, add a class to the list item to style it as done
        if (todo.done) {

            //* add the class 'done' to the list item (for styling in css)
            li.classList.add('done');
        }

        //* add the list item to the todo list object in our html
        todoList.appendChild(li);

        //* add an event listener to the list item (I'll send links)
        //! basically just makes it so that the item waits until it's clicked to do something
        li.addEventListener('click', function() {
            if (deleteMode) {
                todoItems.splice(i, 1);
                renderTodos();
            } else if (!deleteMode) {

                //* if the todo is true, make it false, if it's false, make it true (scoliosis legit)
                todoItems[i].done = !todoItems[i].done;

                //* rerender the todos to update our html visuals
                renderTodos();
            }
        });
    }
    if (todoItems.length === 0) {
        const p = document.createElement('p');
        p.innerHTML = 'No todos to show';
        p.id = 'no-todos';
        todoList.appendChild(p);
        if (deleteMode) {
            deleteMode = false;
            document.body.classList.remove('delete-mode');
        }
    }
}

//* gets todos from the flask server
function getTodos() {

    //* fetch via fetch() to the link /api/get (like I sent you in the burger example code snippet)
    fetch('../api/get')
        .then(response => response.json())
        .then(data => {

            //* overwrite our todoItems list with the data we got from the server so that they're synced
            todoItems = data;

            //* rerender the todos to update our html visuals
            renderTodos();
        });
}

//* adds a todo to the list visually on our html
function addTodo() {

    //* get the text value from the input box with the id 'todo-input'
    const todoText = document.getElementById('todo-input').value;
    const todoid = todoItems.length

    if (todoText !== "") {
        //* add the text to our todoItems list via push (it's like list.append in python)
        todoItems.push({ text: todoText, done: false, id: todoid});
        console.log(todoItems)

        //* rerender the todos to update our html visuals
        renderTodos();

        //? clear the input box after adding the todo for user experience :3
        document.getElementById('todo-input').value = '';
    }
    
}

//* updates the todo list on the server
function updateTodo() {

    //* fetch via fetch() to the link /api/update with a POST request
    fetch('../api/update', {
        
        //* set the method to POST
        method: 'POST',

        //* set the headers to json (required since theres other types of data)
        headers: {
            'Content-Type': 'application/json',
        },

        //* set the body of the request to the json of our todoItems list
        body: JSON.stringify(todoItems),
    })
        .then(response => response.json())
        .then(data => {

            //* overwrite our todoItems list with the data we got from the server so that they're synced
            todoItems = data;

            //* rerender the todos to update our html visuals
            renderTodos();
        });
}

function deleteTodo() {

    //* reverse the delete mode
    deleteMode = !deleteMode;

    //* if delete mode is true, add the class 'delete-mode' to the body to style it, if it's false, remove it
    if (deleteMode) {
        document.body.classList.add('delete-mode');
    } else {
        document.body.classList.remove('delete-mode');
    }
}
//* get the todos from the server on page load so that they're displayed
getTodos();

//* add an event listener to the update button to update the todos on the server when clicked
document.getElementById('todo-update').addEventListener('click', function() {
    updateTodo();
});

//* add an event listener to the add button to add a todo when clicked
document.getElementById('todo-add').addEventListener('click', function() {
    addTodo();
});

//* add an event listener to the delete button to toggle delete mode when clicked
document.getElementById('todo-delete').addEventListener('click', function() {
    deleteTodo();
});

