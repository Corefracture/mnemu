var selected_id = "0.0.0.0";

function get_ips() {

}

function report_ip_clicked_on(e) {
    alert(e)
}

function load_ip_data(ip, data) {
        $.each(data, function (key, val) {
            elem = document.getElementById(key);
            if(elem != null) {
                elem.value = val;
                prnt = elem.parentElement;
                prnt.classList.add("is-dirty");
            }});
        selected_id = ip;
        selected_ip_elem = document.getElementById("selected_ip");
        selected_ip_elem.innerText = "IP: " + ip;
}

function request_ip_data(ip) {
    str_alert = "";
    $.getJSON("/ip/" + ip, function (data) {
            load_ip_data(ip, data);
        });
}

function set_bandwidth(ip, val, outbound) {
    inorout = outbound ? "out" : "in";

    add_to_call = "/" + ip + "/bandwidth/" + val + "/" + inorout;

    $.get(add_to_call)
}

function set_netem_setting(ip, type_id, val, outbound) {
    add_to_call = "/netem/set/" + ip + "?netem_type=" + type_id + "&netem_val=" + val;
    if(outbound === true) {
        add_to_call += "&outbound=true"
    }
    $.get(add_to_call)
}

$.getJSON("/me", function (data) {
    ip = data["ip"];
    ipdata = data["ip_data"];

    this_ip_elem = document.getElementById("this_device_ip");
    this_ip_elem.innerHTML = "<a class=\"mdl-navigation__link\" href=\"javascript:request_ip_data(\'" + ip + "\');\" id=\"buff\">"+ ip + "</a>";

    load_ip_data(ip, ipdata);
});

$.getJSON("ips/get", function (data) {
    var items = [];
    known_ips_elem = document.getElementById("ips_sec");
    known_ips_elem.innerHTML = "";
    $.each(data, function (key, val) {
        //bod.innerHTML += "<a class=\"mdl-navigation__link\" href=\"javascript:report_ip_clicked_on(\'" + val + "\');\" id=\"buff\">"+ val + "</a>";
        known_ips_elem.innerHTML += "<a class=\"mdl-navigation__link\" href=\"javascript:request_ip_data(\'" + val + "\');\" id=\"buff\">"+ val + "</a>";
    });
});


