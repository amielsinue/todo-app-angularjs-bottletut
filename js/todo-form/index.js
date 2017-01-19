/**
 * Created by ayanez on 1/18/17.
 */
module.exports = function(app){
  require('./todo-edit')(app);
  require('./todo-simple-form')(app);
  require('./todoService')(app);
};