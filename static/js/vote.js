const data = document.currentScript.dataset;
function displayRadioValue() {
  var ele = document.getElementsByTagName('input');



  for (i = 0; i < ele.length; i++) {

    if (ele[i].type = "radio") {

      if (ele[i].checked) {
        if (confirm('Ви впевнені що хочете проголосувати за ' + ele[i].value + '?')) {
          $.ajax({
            type: "PUT",
            url: 'http://127.0.0.1:8000/votetest/',
            data: {
              "candidate": ele[i].value,
              "token": data.token
            },
            success: function (data) {
              $('#output').html(data);

            },
            failure: function () {
              alert("failure");
            }
          });
          return true
        }
        else return true
      }
    }
  }
  if (confirm('Ви впевнені що хочете утриматись від голосування?')) {
    $.ajax({
      type: "PUT",
      url: 'http://127.0.0.1:8000/votetest/',
      data: {
        "candidate": "утримуюсь",
        "token": data.token
      },
      success: function (data) {
        $('#output').html(data);

      },
      failure: function () {
        alert("failure");
      }
    });
  }
  else return true
}

var check1, check2;
function radioClick(c) {
  if (check1 != c) {
    check2 = 0;
    check1 = c
  }
  check2 ^= 1;
  c.checked = check2
}