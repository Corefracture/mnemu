function get_ips() {

}

function report_ip_clicked_on(e) {
    alert(e)
}

$.getJSON("ips/get", function (data) {
    var items = [];
    bod = document.getElementById("ips_sec");

    $.each(data, function (key, val) {
        bod.innerHTML += "<a class=\"mdl-navigation__link\" href=\"javascript:report_ip_clicked_on(\'" + val + "\');\" id=\"buff\">" +
            "<i class=\"mdl-color-text--blue-grey-400 material-icons\" role=\"presentation\"></i>" + val + "</a>";
    });


});
