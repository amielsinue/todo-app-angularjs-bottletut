import sqlite3

from functools import wraps
from bottle import route, run, debug, template, request, static_file, error, response

# only needed when you run Bottle on mod_wsgi
from bottle import default_app

def auth(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        username = request.GET.get('username')
        if not username:
            username = request.get_cookie('username')
        if not username:
            return 'Invalid credentials'
        kwargs['username'] = username
        return func(*args, **kwargs)
    return wrapper


@route('/login')
def login():
    if request.GET.get('username'):
        username = request.GET.get('username').strip()
        response.set_cookie('username', username, path='/')
        response.body = "Welcome: {}".format(username)
        return response
    else:
        return template('login.tpl')




@route('/todo')
def todo_list():

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task, status FROM todo WHERE status LIKE '1';")
    result = c.fetchall()
    c.close()

    output = template('make_table', rows=result, user="")
    return output

@route('/new', method='GET')
@auth
def new_item(**kwargs):
    user = kwargs.get('username')
    if request.GET.get('save','').strip():
        new = request.GET.get('task', '').strip()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new,1))
        new_id = c.lastrowid

        conn.commit()
        c.close()

        return '<p>The new task was inserted into the database, the ID is %s</p>' % new_id

    else:
        return template('new_task.tpl', user=user)

@route('/edit/<no:int>', method='GET')
@auth
def edit_item(no, **kwargs):
    user = kwargs.get('username')
    if request.GET.get('save','').strip():
        edit = request.GET.get('task','').strip()
        status = request.GET.get('status','').strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit,status,no))
        conn.commit()

        return '<p>The item number %s was successfully updated</p>' %no

    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task, status FROM todo WHERE id LIKE ?", (str(no)))
        cur_data = c.fetchone()

        return template('edit_task', old = cur_data, no = no, user=user)

@route('/item<item:re:[0-9]+>')
def show_item(item):
        json = True if request.GET.get('format','').strip() == 'json' else False
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (item))
        result = c.fetchall()
        c.close()

        if not result:
            error_message = 'This item number does not exist!'
            return error_message if not json else {'task': error_message}
        else:
            task = result[0]
            return 'Task: %s' % task if not json else {'Task': task}

@route('/delete/<no:int>', method='GET')
@auth
def delete_item(no, **kwargs):
    user = kwargs.get('username')
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM todo where id LIKE ?", (str(no)))
    try:
        conn.commit()
    except Exception as e:
        return 'There was an error trying to remove this task {}'.format(e)
    finally:
        c.close()
    return 'Task {} was successfully removed'.format(no)



@route('/help')
def help():

    static_file('help.html', root='.')


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


debug(True)
run(reloader=True)
#remember to remove reloader=True and debug(True) when you move your application from development to a productive environment
