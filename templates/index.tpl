% rebase('templates/layout.tpl', title='Todo list')
<a href="/logout" class="btn btn-link pull-right">Logout</a>
<a href="/help" class="btn btn-link pull-right">Help</a>
<div class="clearfix"></div>
<div class="row" ng-app="todo">
    <todo-simple-form></todo-simple-form>
    <div class="progress" id="loader">
      <div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 60%;">
        <span class="sr-only">60% Complete</span>
      </div>
    </div>
    <todo-table></todo-table>
</div>
<script src="node_modules/underscore/underscore-min.js"></script>
<script src="js/app.min.js"></script>

