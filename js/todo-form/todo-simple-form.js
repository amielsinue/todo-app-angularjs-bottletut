/**
 * Created by ayanez on 1/18/17.
 */
module.exports = function(app){
  app.directive('todoSimpleForm', function($rootScope, todoService){
    return {
      templateUrl: 'js/todo-form/todo-simple-form.html',
      restrice: 'E',
      controller: function($scope){
        $scope.task = '';
        $scope.save = function(){
          if($scope.task != ''){
            todoService.create($scope.task).then(function(task){
              $rootScope.$broadcast('NEW_TASK_ADDED', task);
            });
            $scope.task = '';
          }
        }
      }
    }
  });
};