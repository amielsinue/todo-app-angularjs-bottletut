/**
 * Created by ayanez on 1/18/17.
 */
module.exports = function(app){
  app.directive('todoTable', function(todoListService, dialogsService){
     return {
         templateUrl: 'js/todo-table/todo-table.html',
         restrice: 'E',
         controller: function($scope){
             $scope.tasks = [];
             $scope.delete = function(_id){
                 dialogsService.confirm("Are you sure you want to delete task [" + _id + "]?").then(function() {
                     todoListService.remove(_id).then(function (response) {
                         var {data} = response;
                         if (!data.error) {
                             toastr.success('Task [' + data.data[1] + '] has been removed!');
                             $scope.tasks = _.filter($scope.tasks, function (task) {
                                 return task[0] != _id;
                             });
                         } else {
                             toastr.error(data.error);
                         }
                     });
                 });
             };
             var loadTasks = function() {
                 todoListService.active().then(function (response) {
                     var {data} = response.data;
                     $scope.tasks = data;
                     $('#loader').hide();
                 });
             }
             $scope.$on('NEW_TASK_ADDED', function(event, response){
                 var { data } = response;
                 if(!data.error){
                     $scope.tasks.push(data.data);
                     toastr.success('Task [' + data.data[1] + '] has been added!');
                 }else{
                     toastr.error(data.error);
                 }
             });
             $scope.$on('TASK_UPDATED', function(event, response){
                 var { data } = response;
                 if(!data.error){
                     var task = data.data;
                     // $scope.tasks.push(data.data);
                     toastr.success('Task [' + task[1] + '] has been updated!');
                     if( task[2] == 0){
                         $scope.tasks = _.filter($scope.tasks, function (_task) {
                             return _task[0] != task[0];
                         });
                     }
                 }else{
                     toastr.error(data.error);
                 }
             });
             loadTasks()
         }
     }
  });
};