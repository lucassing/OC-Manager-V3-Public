// AJAX POST
var roomName = 'oc_lab';
var roomName

$(document).ready(function(){
  document.querySelector('#sentit').value = monitor_text
  var $myForm = $("#Gcode_form")
  $myForm.submit(function(event){
    event.preventDefault()
    var $formData = $(this).serialize()
    var $endpoint = window.location.href
    $.ajax({
      method: 'POST',
      url:    $endpoint,
      data:   $formData,
      success: handleFormSuccess,
      error: handleFormError,
    })
  })

  function handleFormSuccess(data, textStatus, jqXHR){
      scrollIt()
      console.log(textStatus)
      console.log('O DEDSDE ESTE');
      $myForm[0].reset(); // reset form data
  }

  function handleFormError(jqXHR, textStatus, errorThrown){
  }
})

// Erase button
function erase(){
  event.preventDefault()
  document.getElementById("id_chattext").value = ''
}

// MONITOR CONTROLLER
function scrollIt(){
    document.getElementById('sentit').scrollTop = document.getElementById("sentit").scrollHeight
    document.getElementById('id_chattext').value = ''
    document.getElementById('id_chattext').focus();
}

// Slider
function sliderChange(val,id){
  document.getElementById(id).value = val;
}

// Upload form
document.querySelector('.custom-file-input').addEventListener('change',function(e){
  var fileName = document.getElementById("GFile").files[0].name
  document.getElementById('upload_label').innerHTML = fileName


  // Enable the buttons son you can run or erase empty file
  document.getElementById('play_upload').disabled = false;
  document.getElementById('erase_upload').disabled = false;
  document.getElementById('erase_upload').classList.remove("disabled");
})

function erase_upload(){
  document.getElementById('GFile').value = "";
  document.getElementById('upload_label').innerHTML ='Choose file'

  // Disable the buttons son you can not run or erase empty file
  document.getElementById('play_upload').disabled = true
  document.getElementById('erase_upload').disabled = true;
  document.getElementById('erase_upload').classList.add("disabled");
}

// Buttons move
$(document).ready(function(){
  scrollIt()
  document.querySelector('#sentit').value = monitor_text
  var $myForm = $(".move-form")
  $myForm.submit(function(event){
    button_pressed = document.activeElement.id
    event.preventDefault()
    var $formData = $(this).serialize() + "&button="+button_pressed
    var $endpoint = window.location.href
    var $speedrange = document.getElementById("speedrange").value
    $.ajax({
      method: 'POST',
      url:    $endpoint,
      data:   $formData,
      success: handleFormSuccess,
      error: handleFormError,
    })
  })
  function handleFormSuccess(data, textStatus, jqXHR){
    scrollIt()
  }

  function handleFormError(jqXHR, textStatus, errorThrown){
    scrollIt()
  }

  chatSocket = new WebSocket(
      'ws://' + window.location.host +
      '/ws/monitor/' + roomName + '/');

  // MONITOR FUNCTIONS
  chatSocket.onmessage = function(e) {
      var data = JSON.parse(e.data);
      var message = data['message'];
      document.querySelector('#sentit').value += (message + '\n');
      scrollIt()
  };

  chatSocket.onclose = function(e) {
      console.error('Chat socket closed unexpectedly');
  };

})
