/**
 * Created by ayanez on 1/18/17.
 */
var angular = require('angular')

var app = angular.module('todo', []);
require('./dialogs/dialogsService')(app);
require('./todo-table')(app);
require('./todo-form')(app);
