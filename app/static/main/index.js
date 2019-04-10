/* global NProgress */

(function($, window, document){

    var $content = $('a').not('.stay');
    var displayProgress = $(window).width() >= 992;

    NProgress.configure({ showSpinner: false });
    if(displayProgress) {
        NProgress.set(0.6);
    }

    $(function(){

        if(displayProgress) {
            NProgress.done();

            $content.on('click', function () {
                NProgress.start();
            });

            $(window).bind('beforeunload', function () {
                NProgress.start();
            });
        }

    });

    $('.disabled').click(function(e) {
        e.preventDefault();
    });

}(window.jQuery, window, document));