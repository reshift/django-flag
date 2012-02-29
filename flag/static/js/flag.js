
!function( $ ){
  $(function () {
    
    $('.flag-form input[name="ftypes"]').change(function() {
      $(this).submit();
      return false;
    });
 
    $('.flag-form').submit(function() {
        var action = $(this).attr('action');
        var that = $(this);
        $.ajax({
            url: action,
            type: 'POST',
            dataType: 'json',
            data: that.serialize()
            ,success: function(data) {
              // Nothing yet
            }
        });
        return false;
    });

  });
}( window.jQuery );