$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.tooltipped').tooltip();
    $('.collapsible').collapsible();
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

      // Initially disable the edit icon
      $('.fas.fa-edit').closest('a').addClass('disabled');

      // Function to check and update icons based on selection
      $('.portfolio .selectable-item').click(function() {
          // Toggle selected state
          var isSelected = $(this).data('selected');
          $(this).data('selected', !isSelected);
          $(this).toggleClass('selected');
  
          // Check if any item is selected
          var anySelected = $('.portfolio .selectable-item').is(function() {
              return $(this).data('selected');
          });
  
          // Update icons based on selection
          if (anySelected) {
              $('#actionIcon i').removeClass('fa-plus').addClass('fa-trash').css('color', 'red');
              $('#editIcon').removeClass('disabled').addClass('highlighted');
          } else {
              $('#actionIcon i').removeClass('fa-trash').addClass('fa-plus').removeAttr('style');
              $('#editIcon').addClass('disabled').removeClass('highlighted');
          }
      });
  });