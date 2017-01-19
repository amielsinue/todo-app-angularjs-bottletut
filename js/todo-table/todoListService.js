/**
 * Created by ayanez on 1/18/17.
 */
module.exports = function(app){
  app.factory('todoListService', function($http){
      return {
          active: function(){
              return $http.get('/todos?status=1');
          },
          remove: function(_id){
              return $http.delete('/todo/'+_id);
          }
      };
  });
};