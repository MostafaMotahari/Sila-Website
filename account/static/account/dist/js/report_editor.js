// Load report edit form
function loadReports(reportPk) {

    // Show the edit form
    $.ajax({
        url: '/account/update-report/edit/' + reportPk,
        type: 'GET',
        success: function (data) {
            // Handle the response
            $("#match-edit").html(strToHTML(data).getElementById("match-edit").innerHTML);
            document.getElementById("match-detail").style.display = 'none';

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
