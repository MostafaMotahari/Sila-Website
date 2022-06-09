function confirmPage(pk) {
    if (window.confirm("Do you want to register in this tournamet?")) {
        $.ajax({
        url: '/account/tours/register/' + pk,
        type: 'GET',
        success: function (data) {
            $("#register-span-" + pk).prop('class', 'info-box-icon bg-info');
            $("#register-box-" + pk).attr('onclick', 'alreadyRegistred();');
        }
        });
    }
}

function alreadyRegistred(){
alert("You are already registered in this tournament");
}