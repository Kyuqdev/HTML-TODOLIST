var todoItems = Array();
let deleteMode = false;

//* parses the cookie into a json object that we can conveniently pull values from
function parseCookie() {

    //* if the cookie is empty, return an empty object
    if (document.cookie === "") 
        return {};

    //* split the cookie into key value pairs
    let valuePairs = document.cookie.split(';');
    let splittedPairs = valuePairs.map(pair => pair.split('='));

    //* reduce the key value pairs into a json object
    const cookieObject = splittedPairs.reduce((obj, value) => {

        //* trim the values to remove any whitespace
        obj[value[0].trim()] = value[1].trim();

        return obj;
    }, {});

    //* return the json object
    return cookieObject;
}

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

        //* if there are no todos, add a paragraph to the todo list saying "No todos to show"
        const p = document.createElement('p');
        p.innerHTML = 'No todos to show';
        p.id = 'no-todos';
        todoList.appendChild(p);
        if (deleteMode) {

            //* if delete mode is true, set it to false and remove the class 'delete-mode' from the body for ux sake
            deleteMode = false;
            document.body.classList.remove('delete-mode');
        }
    }
}

//* gets todos from the flask server
function getTodos() {

    //* fetch via fetch() to the link /api/get (like I sent you in the burger example code snippet)
    fetch('../api/get', {
        method: 'GET',
        headers: {
            'token': parseCookie()['token'],
            'Content-Type': 'application/json',
        }
    })
        .then((res) => {

            //* check the response status
            //* if it's 200 (okay), continue
            if (res.status === 200) {

                //* idfk why we have to pull the value like this but yeah
                res.json().then(data => {

                    //* set our todoItems list to the data we got from the server
                    todoItems = data;

                    //* rerender the todos to update our html visuals
                    renderTodos();
                });
            } else {

                //* if the response status isn't 200, alert the user with the response text and delete our cookie
                document.cookie = 'token=; max-age=0; path=/';
                alert("Corrupted token. Please try logging in again!");
                
                //* return to the login page
                window.location.reload();
            }
        });
}

//* adds a todo to the list visually on our html
function addTodo() {

    //* get the text value from the input box with the id 'todo-input'
    const todoText = document.getElementById('todo-input').value;
    const todoid = todoItems.length;

    if (todoText !== "") {
        //* add the text to our todoItems list via push (it's like list.append in python)
        todoItems.push({ text: todoText, done: false, id: todoid});


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
            'token': parseCookie()['token'],
            'Content-Type': 'application/json',
        },

        //* set the body of the request to the json of our todoItems list
        body: JSON.stringify(todoItems),
    })
        .then(response => {
        if (response.status === 200) {
            response.json().then(data => {

                //* overwrite our todoItems list with the data we got from the server so that they're synced
                todoItems = data;

                //* rerender the todos to update our html visuals
                renderTodos();

                if (deleteMode) {

                    //* if delete mode is true, set it to false and remove the class 'delete-mode' from the body for ux sake
                    deleteMode = false;
                    document.body.classList.remove('delete-mode');
                }
            });
        } else { 

            //* if the response status isn't 200, alert the user with the response text and delete our cookie
            document.cookie = 'token=; max-age=0; path=/';
            alert("Corrupted token. Please try logging in again!");

            //* return to the login page
            window.location.reload();
        }
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

//* add an event listener to the input box to add a todo when enter is pressed
document.getElementById('todo-input').addEventListener('keypress', function(event) {
    //* if the key pressed is enter
    if (event.key === 'Enter') {

        //* get the text value from the input box with the id 'todo-input'
        const todoText = document.getElementById('todo-input').value;
        const todoid = todoItems.length;

        //* if the text isn't empty, add the todo
        if (todoText !== "") {
            todoItems.push({ text: todoText, done: false, id: todoid });
            renderTodos();
            document.getElementById('todo-input').value = '';
        }

        //* add a class to the add button to make it look like it was clicked for 100ms
        const button = document.getElementById('todo-add');
        button.classList.add('active');
        setTimeout(() => {
            button.classList.remove('active');
        }, 100);
    }
});

//* add an event listener to the log out button to delete the token cookie and reload the page
document.getElementById('log-out').addEventListener('click', function() {
    document.cookie = 'token=; max-age=0; path=/';
    window.location.reload();
});

function getUserName() {
    fetch('../account/username', {
        method: 'GET',
        headers: {
            'token': parseCookie()['token'],
            'Content-Type': 'application/json',
        }
    })
        .then((res) => {
            if (res.status === 200) {
                res.text().then(data => {
                    document.getElementById('user-name').innerHTML = data;
                });
            } else {
                document.cookie = 'token=; max-age=0; path=/';
                alert("Corrupted token. Please try logging in again!");
                window.location.reload();
            }
        })
}

getUserName();