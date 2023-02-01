const data = document.currentScript.dataset;
function displayRadioValue() {
  var ele = document.getElementsByTagName('input');

  for (i = 0; i < ele.length; i++) {

    if (ele[i].type = "radio") {

      if (ele[i].checked) {
        $.ajax({
          type: "PUT",
          url: 'https://obscure-bastion-38165.herokuapp.com/votetest/',
          data: {
            "candidate": ele[i].value,
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
    url: 'https://obscure-bastion-38165.herokuapp.com/votetest/',
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