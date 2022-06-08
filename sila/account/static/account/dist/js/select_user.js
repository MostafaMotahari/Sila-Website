$(function () {
  //Initialize Select2 Elements
  $('.select2').select2()

  //Initialize Select2 Elements
  $('.select2bs4').select2({
    theme: 'bootstrap4'
  })

})

// Custom Js

var defaultOptions = {
  color: "primary",
  dateFormat: "yyyy-MM-dd"
};

function loadUser() {
  var user_pk = document.getElementById("user-list").selectedOptions[0].value;

  $.ajax({
      url: '/account/user-control/update-user/' + user_pk.split(":")[0],
      type: 'GET',
      success: function (data) {
        $("#infos").html(strToHTML(data).getElementById("infos").innerHTML);

        // Hide select user section
        document.getElementById("select-user").style.display = "none";

        // Set Calendars
        $(function () {
          $('#datetimepicker1').datetimepicker({
            format: 'YYYY-MM-DD'
          });
          $('#datetimepicker2').datetimepicker({
            format: 'YYYY-MM-DD'
          });
        });

      }
  });
}

function strToHTML(str) {
  var parser = new DOMParser();
  var doc = parser.parseFromString(str, "text/html");
  return doc;
}

function cancelUpdateUser(){
  selectUserElement = document.getElementById("select-user")
  selectUserElement.style.display = "block";
  selectUserElement.style.width = "100%";
  document.getElementById("infos").innerHTML = "";
}
