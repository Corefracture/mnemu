var selected_id = "0.0.0.0";


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

function set_presets_to_none() {
    in_preset_selector = document.getElementById("preset_in");
    if(in_preset_selector != null)
    {
        in_preset_selector.value = "None"
    }
    out_preset_selector = document.getElementById("preset_out");
    if(out_preset_selector != null)
    {
        out_preset_selector.value = "None"
    }
}

function clear_ip_settings(ip) {
    set_presets_to_none();
    $.get("ip/" + ip + "/clear", function (data) {
        request_ip_data(ip);
    });
}

function set_preset(ip, preset_id, outbound) {
    if(preset_id !== 'None') {
        inorout = outbound ? "out" : "in";
        $.get("ip/" + ip + "/preset/" + preset_id + "/" + inorout, function (data) {
            if (data === "true") {
                request_ip_data(ip);
            }
        });
    }
}

function set_bandwidth(ip, val, outbound) {
    inorout = outbound ? "out" : "in";
    add_to_call = "/" + ip + "/bandwidth/" + val + "/" + inorout;
    $.get(add_to_call);
    set_presets_to_none();
}

function refresh_rules() {
    $.get("/refreshrules");
}

function set_netem_setting(ip, type_id, val, outbound) {
    add_to_call = "/netem/set/" + ip + "?netem_type=" + type_id + "&netem_val=" + val;
    if(outbound === true) {
        add_to_call += "&outbound=true"
    }
    $.get(add_to_call);
    set_presets_to_none();
}

$.getJSON("/me", function (data) {
    ip = data["ip"];
    ipdata = data["ip_data"];

    this_ip_elem = document.getElementById("this_device_ip");
    this_ip_elem.innerHTML = "<a class=\"mdl-navigation__link\" href=\"javascript:request_ip_data(\'" + ip + "\');\" id=\"buff\">"+ ip + "</a>";

    load_ip_data(ip, ipdata);
});

$.getJSON("/presets/get", function(data) {
    in_preset_selector = document.getElementById("preset_in");
    out_preset_selector = document.getElementById("preset_out");
    if(in_preset_selector != null && out_preset_selector != null) {
        opts = "<option>None</option>";
        $.each(data, function (key, val) {
            opts += "<option value='" + key + "'>" + val + "</option>";
        });
        in_preset_selector.innerHTML = opts;
        out_preset_selector.innerHTML = opts;
    }
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




