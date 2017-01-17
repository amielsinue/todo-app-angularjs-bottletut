% rebase('index.tpl', title='Editing Task')
<form action="/edit/{{no}}" method="get" id="todo_form">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="task_name">Editing: {{old[0]}}</h4>
      </div>
      <div class="modal-body">
        <div class="form-group">
            <label>Task</label>
            <input class="form-control" name="task" id="task_name" value="{{old[0]}}">
        </div>
        <div class="form-group">
            <label>Status</label>
            <select class="form-control" name="status" id="task_status">
                <option {{ "selected" if old[1] else ""}}>open</option>
                <option {{ "selected" if not old[1] else ""}}>closed</option>
            </select>
        </div>
      </div>
      <div class="modal-footer">
        <a href='/todo' type="button" class="btn btn-default" data-dismiss="modal">Close</a>
        <button type="submit" name="save" value="1" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
  </form>