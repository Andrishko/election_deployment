const dat = document.currentScript.dataset;
// var countDownDate = new Date("Jan 5, 2024 15:37:25").getTime();

// Update the count down every 1 second
var x = setInterval(function () {

  countDownDate = Date.parse(dat.time) + 300000;
  // Get today's date and time
  var now = new Date().getTime();

  // Find the distance between now and the count down date
  var distance = countDownDate - now;

  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the result in the element with id="demo"
  document.getElementById("timer").innerHTML = minutes + "хв " + seconds + "с ";

  // If the count down is finished, write some text
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("timer").innerHTML = "EXPIRED";
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
}, 1000);