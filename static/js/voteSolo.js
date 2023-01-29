const data = document.currentScript.dataset;
function displayRadioValue() {
  var ele = document.getElementsByTagName('input');

  for (i = 0; i < ele.length; i++) {

    if (ele[i].type = "radio") {

      if (ele[i].checked) {
        
        $.ajax({
          type: "PUT",
          url: 'http://127.0.0.1:8000/votesolo/',
          data: {
          
            "candidate": data.candidate,
            "vote": ele[i].value,
            "token": data.token
          },
          success: function (data) {
            console.log(data);
            $('#output').html(data);

          },
          failure: function () {
            alert("failure");
          }
        });
        return true
      }
    }
  }
  $.ajax({
    type: "PUT",
    url: 'http://127.0.0.1:8000/votetest/',
    data: {
      "candidate": data.abstain,
      "token": data.token
    },
    success: function (data) {
      console.log(data);
      $('#output').html(data);

    },
    failure: function () {
      alert("failure");
    }
  });
}

var check1, check2;
function radioClick(c) {
  console.log('click');
  if (check1 != c) {
    check2 = 0;
    check1 = c
  }
  check2 ^= 1;
  c.checked = check2
}