
function formatDate(d) {
    month = d.getMonth() + 1;
    day = d.getDate();
    formatted_date = d.getFullYear() + '-' +
        (month < 10 ? '0' : '') + month + '-' +
        (day < 10 ? '0' : '') + day;
    return formatted_date;
}

function formatTime(d) {
    var formatted_time = (d.getHours() < 10 ? '0' : '') + d.getHours() + ':' +
        (d.getMinutes() < 10 ? '0' : '') + d.getMinutes();
    return formatted_time;
}

function formatDateTime(d) {
    return formatDate(d) + " " + formatTime(d);
}


function local_to_utc(d) {
    var utc_date = new Date(d.getUTCFullYear(),
        d.getUTCMonth(),
        d.getUTCDate(),
        d.getUTCHours(),
        d.getUTCMinutes());
    return utc_date;
}


function utc_to_local(d) {
    formatted_date = formatDate(d) + "T" + formatTime(d) + 'Z';
    var local_date = new Date(formatted_date);
    return local_date;
}
