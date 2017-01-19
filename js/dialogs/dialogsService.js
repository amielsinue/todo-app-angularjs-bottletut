/**
 * Created by ayanez on 1/18/17.
 */
module.exports = function(app){

  app.factory('dialogsService', function(){
    return {
			prompt: prompt,
            confirm: confirm
		};
		function prompt(text, validation) {
			return swal({
					title: "Todo",
					text: text,
                    input: 'text',
                    preConfirm: function(_value){
						var deferred = $q.defer();
						if( typeof validation != "undefined"){
							validation.apply(deferred, [_value]);
						}else{
							deferred.resolve();
						}
						return deferred.promise;
					},
					showCancelButton: true,
					showLoaderOnConfirm: true,
					animation: "slide-from-top",
					inputPlaceholder: "Write something"
				});
		}

		function confirm(text){
		  return swal({
            title: "Todo",
            text: text,
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes!'
          });
        }
  });
};