/**
 * @licence
 * Copyright (C) 2018 Corefracture, Chris Coleman. All Rights Reserved.
 * www.corefracture.com - @corefracture
 *
 * Licensed under the MIT License, https://opensource.org/licenses/MIT
 * See LICENSE.md for more details
**/


//cf - LOADS of clean up to do here
//Lots of code to get features up and running but not organized
//or optimized properly.

var selected_id = "0.0.0.0";
var favs = [];
var ignores = [];

//Load the netem data received for the IP
function load_ip_data(ip, data) {
    if (data != null) {
        $.each(data, function (key, val) {
            elem = document.getElementById(key);
            if (elem != null) {
                elem.value = val;
                prnt = elem.parentElement;
                prnt.classList.add("is-dirty");
            }
        });
    }
    selected_id = ip;
    selected_ip_elem = document.getElementById("selected_ip");
    selected_ip_elem.innerText = "IP: " + ip + "  -  ";
}


//Send request for IP netem data
function request_ip_data(ip) {
    str_alert = "";
    $.getJSON("/ip/" + ip, function (data) {
        load_ip_data(ip, data);
    });

    toggle_fav_icon(ip);
    toggle_ignore_icon(ip);
}

function toggle_ignore_icon(ip) {
    ignore_icon_elem = document.getElementById('ignore-icon');
    if (ignores.includes(ip)) {
        ignore_icon_elem.innerText = "visibility_on";
        $('#outbound-rules').find('*').hide();
        $('#inbound-rules').find('*').hide();
    } else {
        ignore_icon_elem.innerText = "visibility_off";
        $('#outbound-rules').find('*').show();
        $('#inbound-rules').find('*').show();
    }
}

function toggle_fav_icon(ip) {
    fav_icon_elem = document.getElementById('fav-icon');
    if (favs.includes(ip)) {
        fav_icon_elem.innerText = "star";
    } else {
        fav_icon_elem.innerText = "star_border";
    }
}

function get_favs() {
    favsCook = Cookies.get("mnemu_favs");
    if (favsCook != null) {
        favs = JSON.parse(favsCook);
    }
    populate_favs();
}

function toggle_ignore_ip(ip) {
    if (!ignores.includes(ip)) {
        $.get("/ip/" + ip + "/ignore", function () {
            refresh_ignored_and_known();
        })
    } else {
        $.get("/ip/" + ip + "/unignore", function () {
            $.getJSON("/ip/" + ip, function (ipdata) {
                load_ip_data(ip, ipdata);
                refresh_ignored_and_known();
            });
        });

    }
}

function refresh_ignored_and_known() {
    get_ignored_ips(() => {
        get_known_ips();
        toggle_ignore_icon(selected_id);
    });
}

function toggle_fav_ip(ip) {
    favsCook = Cookies.get("mnemu_favs");
    if (favsCook != null) {
        favs = JSON.parse(favsCook);
    }

    if (!favs.includes(ip)) {
        favs.push(ip);
    } else {
        if (favs.length > 1) {
            favs.splice(favs.indexOf(ip), 1);
        } else {
            favs = [];
        }

    }

    favsCook = JSON.stringify(favs);
    Cookies.set("mnemu_favs", favsCook);
    toggle_fav_icon(selected_id);
    populate_favs();
}

function populate_favs() {
    elem = document.getElementById('favorite_ips');
    elem.innerText = "";
    favs.forEach(ip => {
        add_ip_to_menu_sec(elem, ip);
    })
}


function set_presets_to_none() {
    in_preset_selector = document.getElementById("preset_in");
    if (in_preset_selector != null) {
        in_preset_selector.value = "None"
    }
    out_preset_selector = document.getElementById("preset_out");
    if (out_preset_selector != null) {
        out_preset_selector.value = "None"
    }
}

function clear_ip_settings(ip) {
    set_presets_to_none();
    $.get("ip/" + ip + "/clear", function () {
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

function collapse_menu_sec(target_elem_id) {
    elem = document.getElementById(target_elem_id);
    if (elem.hidden) {
        elem.hidden = false;
        elem.style.height = "auto";
    } else {
        elem.hidden = true;
        elem.style.height = 0;
    }
}

function set_netem_setting(ip, type_id, val, outbound) {
    add_to_call = "/netem/set/" + ip + "?netem_type=" + type_id + "&netem_val=" + val;
    if(outbound === true) {
        add_to_call += "&outbound=true"
    }
    $.get(add_to_call);
    set_presets_to_none();
}

function add_ip_to_menu_sec(elem, ip) {
    elem.innerHTML += "<a class=\"mdl-navtext__link mdl-navigation__link\" href=\"javascript:request_ip_data(\'" + ip + "\');\" id=\"buff\">" + ip + "</a>";
}

function get_ignored_ips(callback = null) {
    $.getJSON("/ignored", function (data) {
        ignored_ips_elem = document.getElementById("ips_ignored");
        ignored_ips_elem.innerHTML = "";
        ignores = [];
        $.each(data, function (key, val) {
            ignores.push(val);
            add_ip_to_menu_sec(ignored_ips_elem, val);
        });

        if (callback != null) {
            callback();
        }
    });
}

function get_known_ips(callback = null) {
    $.getJSON("/ips/get", function (data) {
        ips_sec_elem = document.getElementById("ips_sec");
        ips_sec_elem.innerHTML = "";
        $.each(data, function (key, val) {
            add_ip_to_menu_sec(ips_sec_elem, val);
        });

        if (callback != null) {
            callback();
        }
    });
}

function fresh_visit() {
    $.getJSON("/me", function (data) {
        ip = data["ip"];
        ipdata = data["ip_data"];
        this_ip_elem = document.getElementById("this_device_ip");
        this_ip_elem.innerText = "";
        add_ip_to_menu_sec(this_ip_elem, ip);
        load_ip_data(ip, ipdata);
    });
}

function get_presets() {
    $.getJSON("/presets/get", function (data) {
        in_preset_selector = document.getElementById("preset_in");
        out_preset_selector = document.getElementById("preset_out");
        if (in_preset_selector != null && out_preset_selector != null) {
            in_opts = "<option>None</option>";
            out_opts = "<option>None</option>";
            in_presets = data["in"];
            out_presets = data["out"];

            $.each(in_presets, function (key, val) {
                in_opts += "<option value='" + key + "'>" + val + "</option>";
            });

            $.each(out_presets, function (key, val) {
                out_opts += "<option value='" + key + "'>" + val + "</option>";
            });

            in_preset_selector.innerHTML = in_opts;
            out_preset_selector.innerHTML = out_opts;
        }
    });

}


fresh_visit();
get_presets();
get_known_ips();
get_ignored_ips();

