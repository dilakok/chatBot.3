var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    fakeMessage();
  }, 100);
  function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  }
  
  console.log(uuidv4());
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  setTimeout(function() {
  }
  //, 1000 + (Math.random() * 20) * 100
  );
}

$('.message-submit').click(function() {

  $.ajax({
    type: 'post',
    url: "http://127.0.0.1:7201/check",
    data: {'param1': $('.message-input').val()},
    async: false,
    success: function (response) {
        //alert(response.param1);
    }
}).done(function (data) {
  //alert(data);
  fakeMessage(data)
});
let MessageContent = $(".message-input").val();
  insertMessage();
});

$(window).on('keydown', function(e) {
  if(e.key.toLowerCase() == "enter") {
    $.ajax({
      type: 'post',
      url: "http://127.0.0.1:7201/check",
      data: {'param1': $('.message-input').val()},
      async: false,
      success: function (response) {
          //alert(response.param1);
      }
  }).done(function (data) {
    //alert(data);
    fakeMessage(data)
  });

    let MessageContent = $(".message-input").val();
    insertMessage();
  }
})

var Fake = [
  'Nasıl yardımcı olabilirim?',
]
function fakeMessage(msg) {

  if(msg == null){
    msg = Fake[0]
  }


  $('<div class="message loading new"><figure class="avatar"><img src="https://www.locopoco.com/ProductImages/156336/original/43937_silverlit-maze-breaker-robot-yesil_1.jpg" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function() {
    $('.message.loading').remove();
    $('<div class="message new"><figure class="avatar"><img src="https://www.locopoco.com/ProductImages/156336/original/43937_silverlit-maze-breaker-robot-yesil_1.jpg" /></figure>' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
    i++;
  }
  //, 1000 + (Math.random()*20) * 100
  );

}