
!function( $ ){
  $('.flag-form').submit(function() {
      var action = $(this).attr('action');
      var that = $(this);
      $.ajax({
          url: action,
          type: 'POST',
          dataType: 'json',
          data: that.serialize()
          ,success: function(data) {
            if(data.object === undefined) {
              $("button", that).text(data.ftype.label);
            }else{
              $("button", that).text(data.ftype.flagged_label);
            }
          }
      });
      return false;
  });
}( window.jQuery );

