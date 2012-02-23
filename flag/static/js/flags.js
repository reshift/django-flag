
function flagsAjaxForm(id) {
  $('#' + id).submit(function() {
      var action = $(this).attr('action');
      var that = $(this);
      $.ajax({
          url: '/flags/set_flag',
          type: 'POST',
          dataType: 'json',
          data: that.serialize()
          ,success: function(data) {
            if(data[0] === undefined) {
              $("button", that).text("I dont have this game");
              
            }else{
              $("button", that).text("I got this game");
            }
          }
      });
      return false;
  });
}
