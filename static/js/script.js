$(document).ready(function() {
    $('.sidenav').sidenav();
    $('.tooltipped').tooltip();
    $('.collapsible').collapsible();
    $('.datepicker').datepicker();
    $('.modal').modal({
        dismissible: false,
        onOpenStart: function(modal, trigger) {
            var content = $(modal).find('.modal-content');
            var form = content.find('form');
            form.css('maxHeight', (content.height() - 60) + 'px');
            form.css('overflow', 'auto');
        }
    });
    $('#cancelBtn').click(function(){
        $('.modal').modal('close');
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

    // New code for setting experience to delete
    var experienceToDelete = null;

    window.setExperienceToDelete = function(experienceId) {
        experienceToDelete = experienceId;
    };

    $('#confirm-delete-btn').on('click', function() {
        if (experienceToDelete) {
            $('#delete-form-' + experienceToDelete).submit();
        }
    });

    $('.modal-trigger.delete').on('click', function(e) {
        e.preventDefault();
        var experienceId = $(this).data('id');
        setExperienceToDelete(experienceId);
        $('#delete_experience_modal').modal('open');
    });

    
});



