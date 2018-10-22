(function($, window, document){

   $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });

   $('#inlineFormCustomSelect').change(function(){
       var option = $('#inlineFormCustomSelect').val();
       if(option === 'All'){
           $('.clickable-row').show();
       }else{
        $('.clickable-row').show().not('.'+option).hide();
       }
   })

}(window.jQuery, window, document));