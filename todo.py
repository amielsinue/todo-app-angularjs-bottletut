import sqlite3

from functools import wraps
from bottle import route, run, debug, template, request, static_file, error, response, redirect

# only needed when you run Bottle on mod_wsgi
from bottle import default_app


def auth(func):
    '''
    This method was implemented in task number 6 since was easiest to implement it first
    :param func:
    :return:
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = request.GET.get('username')
        if not username:
            username = request.get_cookie('username')
        if not username:
            # This task was already implemented on task number 6 since was easiest
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
    username = request.get_cookie('username')
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task, status, last_edited_by FROM todo WHERE status LIKE '1';")
    result = c.fetchall()
    c.close()

    output = template('make_table', rows=result, user=username, message=request.GET.get('m'), message_class="success")
    return output


@route('/new', method='GET')
@auth
def new_item(**kwargs):
    username = kwargs.get('username')
    if request.GET.get('save', '').strip():
        new = request.GET.get('task', '').strip()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("INSERT INTO todo (task,status, last_edited_by) VALUES (?,?,?)", (new, 1, username))
        new_id = c.lastrowid
        conn.commit()
        c.close()
        redirect('/todo?m=The new task was inserted into the database, the ID is {}'.format(new_id))
    else:
        base = template('new_task.tpl')
        return template('index.tpl', base=base, title="New Task")


@route('/edit/<no:int>', method='GET')
@auth
def edit_item(no, **kwargs):
    username = kwargs.get('username')
    if request.GET.get('save', '').strip():
        edit = request.GET.get('task', '').strip()
        status = request.GET.get('status', '').strip()
        status = 1 if status == 'open' else 0
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ?, last_edited_by = ? WHERE id = ?", (edit, status, username, no))
        conn.commit()
        redirect('/todo?m=The item number {} was successfully updated'.format(no))
    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task, status FROM todo WHERE id = :id", (str(no),))
        cur_data = c.fetchone()
        return template('edit_task', old=cur_data, no=no, user=username)


@route('/item<item:re:[0-9]+>')
def show_item(item):
        json = True if request.GET.get('format', '').strip() == 'json' else False
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id = ?", (item,))
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
def delete_item(no):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM todo where id = :id", (str(no),))
    try:
        conn.commit()
        message = 'Task {} was successfully removed'.format(no)
    except Exception as e:
        message = 'There was an error trying to remove this task {}'.format(e)
    finally:
        c.close()

    redirect('/todo?m={}'.format(message))


@route('/help')
def _help():
    static_file('help.html', root='.')


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


debug(True)
run(reloader=True)
# remember to remove reloader=True and debug(True) when you move your application
# from development to a productive environment