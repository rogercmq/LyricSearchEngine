(function($) {
    $(document).ready(function() { 
		var fields = $('.contact-form input[type="text"], .contact-form textarea');
		fields.each(function(){
			var this_field = $(this);
			var default_value = this_field.val();
			this_field.focus(function(){
		 		if(this_field.val() == default_value){
					this_field.val("");
				}
			 });
			 this_field.blur(function(){
			 	if(this_field.val() == ""){
					this_field.val(default_value);
				}
			 });
        });

        fields = $('.submit-form input[type="text"]');
        fields.each(function () {
            var this_field = $(this);
            var default_value = this_field.val();
            this_field.focus(function () {
                if (this_field.val() == default_value) {
                    this_field.val("");
                }
            });
            this_field.blur(function () {
                if (this_field.val() == "") {
                    this_field.val(default_value);
                }
            });
        });
    });
})(jQuery);