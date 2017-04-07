$( document ).ready(function(){
  console.log("ready");

  $('#accept-match').click(function(e){
    var item_id = $('.request-item').attr('id');
    console.log(csrftoken);
    console.log(item_id);
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: '/participate/give/confirm',
      data: {
        'item_id': item_id,
        'csrfmiddlewaretoken':  csrftoken,
      },
      success: function(data, status){
        console.log("Success");
        window.location.href = 'dashboard'
      },
      error: function(status, error){
        console.log("Error:", error);
      }
    })

  })


});
