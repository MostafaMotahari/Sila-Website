// Custom Js

var defaultOptions = {
    color: "primary",
    dateFormat: "yyyy-MM-dd"
};

// Load match edit form
function loadMatch(matchPk) {

    // Show the edit form
    $.ajax({
        url: '/account/match-manager/edit/' + matchPk,
        type: 'GET',
        success: function (data) {
            // Handle the response
            $("#match-edit").html(strToHTML(data).getElementById("match-edit").innerHTML);
            document.getElementById("match-detail").style.display = 'none';

            // Set Calendars
            $(function () {
                $('#datetimepicker1').datetimepicker({
                    format : "YYYY-MM-DD HH:mm",
                });
            });

        }
    }
    );
}

// Convert str to html
function strToHTML(str) {
    var parser = new DOMParser();
    var doc = parser.parseFromString(str, "text/html");
    return doc;
}
