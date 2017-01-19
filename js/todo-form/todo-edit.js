/**
 * Created by ayanez on 1/18/17.
 */
module.exports = function (app){
    app.directive('todoEdit', function(todoService){
        return {
            templateUrl:"js/todo-form/todo-edit.html",
            restrice: 'E',
            controller: function($scope,$rootScope){
                $scope.list_status = ["open", "closed"];
                $scope.status = $scope.row[2] == 1 ? "open":"closed";
                $scope.save = function(task){
                  if(task[1] != ''){
                    todoService.update(task[0], task[1], $scope.status).then(function(response){
                      $rootScope.$broadcast('TASK_UPDATED', response);
                    });
                  }
                  $('#todo-edit-modal-'+task[0]).modal('hide');
                }
            }
        }
    });
};