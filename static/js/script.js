$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.modal').modal({
        dismissible: true,
        onOpenStart: function(modal, trigger) {
            var content = $(modal).find('.modal-content');
            var form = content.find('form');
            form.css('maxHeight', (content.height() - 60) + 'px');
            form.css('overflow', 'auto');
        }
    });
    $(document).on('click', '.switch-modal', function(e) {
        e.preventDefault();
        var targetModal = $(this).attr('href');
        $('.modal').modal('close');
        setTimeout(function() {
            $(targetModal).modal('open');
        }, 200); 
    });

  });