/**
 * Created by ayanez on 1/18/17.
 */
module.exports = function(app){
  app.factory('todoService', function($http, $httpParamSerializerJQLike){
        return {
            "create": function(task){
                var data = $httpParamSerializerJQLike({ "task": task});
                return $http.post('/todo', data);
            },
            "update": function(id, task, status){
                var data = $httpParamSerializerJQLike({ "task": task, "status": status});
                return $http.post('/todo/'+ id,data);
            }
        }
  });
};