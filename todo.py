import sqlite3
import os

from functools import wraps
from bottle import route, run, debug, template, request, static_file, error, response, redirect

# only needed when you run Bottle on mod_wsgi
from bottle import default_app


db = "{}/{}".format(os.path.dirname(__file__), 'todo.db')
conn = sqlite3.connect(db)


class TodoException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


def query(sql, params=(), attr_name=None, commmit=False):
    c = conn.cursor()
    c.execute(sql, params)
    result = None
    if attr_name and hasattr(c, attr_name):
        attr = getattr(c, attr_name)
        result = attr if not callable(attr) else attr()
    if commmit:
        conn.commit()
    c.close()
    return result


def auth(func):
    '''
    This method was implemented in task number 6 since was easiest to implement it first
    :param func:
    :return:
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = request.GET.get('username', request.POST.get('username'))
        if not username:
            username = request.get_cookie('username')
        if not username:
            # This task was already implemented on task number 6 since was easiest
            redirect('/login')
        kwargs['username'] = username
        return func(*args, **kwargs)
    return wrapper


def todo_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = dict(data=None, error=None)
        try:
            result['data'] = func(*args, **kwargs)
        except TodoException as e:
            result['error'] = str(e)
        except Exception as e:
            result['error'] = "There was an error on the app: {}".format(e)
        return result
    return wrapper


@route('/todos')
@auth
@todo_response
def todos(**kwargs):
    status = request.GET.get('status')
    sql = "SELECT id, task, status, last_edited_by FROM todo"
    params = []
    if status:
        sql += " WHERE status = {}".format(status)
    return query(sql, params=params, attr_name='fetchall')


@route('/todo', method='POST')
@auth
@todo_response
def add_task(**kwargs):
    _id = kwargs.get('id')
    username = kwargs.get('username')
    new = request.POST.get('task', '').strip()
    if not new:
        raise TodoException("Task must be defined", code=402)
    _id = query("INSERT INTO todo (task,status, last_edited_by) VALUES (?,?,?)", (new, 1, username),
               attr_name='lastrowid', commmit=True)
    return query("SELECT id, task, status, last_edited_by FROM todo WHERE id = :id", (str(_id),), attr_name="fetchone")


@route('/todo/<id:int>', method='POST')
@auth
@todo_response
def edit_task(**kwargs):
    _id = kwargs.get('id')
    username = kwargs.get('username')
    task = request.POST.get('task', '').strip()
    if not task:
        raise TodoException("Task must be defined")
    status = request.POST.get('status', '').strip()
    status = 1 if status == 'open' else 0
    query("UPDATE todo SET task = ?, status = ?, last_edited_by = ? WHERE id = ?", (task, status, username, _id))
    return query("SELECT id, task, status, last_edited_by FROM todo WHERE id = :id", (str(_id),), attr_name="fetchone")


@route('/todo/<id:int>', method='DELETE')
@auth
@todo_response
def delete_task(**kwargs):
    _id = kwargs.get('id')
    data = query("SELECT id, task, status, last_edited_by FROM todo WHERE id = :id", (str(_id),), attr_name="fetchone")
    if not data:
        raise TodoException("Task does not exists")
    query("DELETE FROM todo WHERE id = :id", (str(_id),), commmit=True)
    return data


@route('/')
@auth
def index(**kwargs):
    return template('templates/index.tpl', message=request.GET.get('m'))

@route('/logout')
@auth
def logout(**kwargs):
    response.delete_cookie('username')
    redirect('/')


@route('/login')
def login():
    if request.GET.get('username'):
        username = request.GET.get('username').strip()
        response.set_cookie('username', username, path='/')
        response.body = "Welcome: {}".format(username)
        redirect('/')
    else:
        return template('templates/login.tpl')

@route('/help')
def _help(**kwargs):
    return template('templates/help.tpl')

@route('/js/<path:path>')
def callback(path):
    return static_file(path, root='./js/')\

@route('/node_modules/<path:path>')
def callback(path):
    return static_file(path, root='./node_modules/')

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