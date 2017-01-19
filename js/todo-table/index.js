/**
 * Created by ayanez on 1/18/17.
 */
module.exports = function(app){
  require('./todo-table')(app);
  require('./todoListService')(app);
};