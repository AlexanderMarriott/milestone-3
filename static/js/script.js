$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.tooltipped').tooltip();
    $('.modal').modal({
        dismissible: false,
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


    var $profileHeadlineInput = $('#profile_headline');
    var $profileHeadlineCounter = $('#profile_headline-counter');

    $profileHeadlineInput.on('input', function() {
        var currentLength = $profileHeadlineInput.val().length;
        var maxLength = $profileHeadlineInput.attr('maxlength');
        $profileHeadlineCounter.text(currentLength + '/' + maxLength);
    });

    
  });