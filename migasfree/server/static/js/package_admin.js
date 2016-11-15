function getoptions(endpoint,key,value)
{
    var _options = "";
    $.ajaxSetup({async: false});
    while (endpoint) {
        $.getJSON(endpoint, function(q) {
            var j=q["results"];
            for (var i = 0; i < j.length; i++) {
                _options += "<option value='" + j[i][key] + "'>" + j[i][value] + "</option>";
            }
            endpoint=q["next"]
        });
    }
    $.ajaxSetup({async: true});
    return _options;
}


function changeVersion(defaultValue)
{
    defaultValue = defaultValue || "";
    $("#id_store").html(getoptions("/api/v1/token/stores/?version__id="+$("#id_version").val(), "id", "name"));
    $("#id_store").attr("disabled", false);
    if (typeof defaultValue === "string" && defaultValue !== "")
    {
        $("#id_store option[value=" + defaultValue + "]").attr("selected", true);
    }
    $("#id_version").attr("selected", "selected");
}


$(function() {
        changeVersion($("#id_store").val());
        $("#id_version").change(changeVersion);
    }
);
