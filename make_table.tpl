%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
% include('new_task.tpl')
<p>The open items are as follows:</p>
<table border="1">
 <thead>
    <th>Id</th>
    <th>Task</th>
    <th>Status</th>
    <th></th>
  </thead>
%for row in rows:
  <tr>
    <td>{{row[0]}}</td>
    <td>{{row[1]}}</td>
    <td>{{row[2]}}</td>
    <td>
        <a href="/edit/{{row[0]}}">Edit</a>
        <a href="/delete/{{row[0]}}"
        onclick="return confirm('Do you really want to delete this task [{{row[1]}}]?')">Delete</a></td>
  </tr>
%end
</table>
