$(document).ready(function(){
    Recaptcha.create("{{ RECAPTCHA_PUBLIC_KEY }}", "recaptcha", {
    theme: "clean",
    callback: Recaptcha.focus_response_field
    });
    $("#id_fecha_nacimiento").datepicker({
    changeMonth: true,
    changeYear: true,
    yearRange: "1950:2012"
    });
    $("#id_descripcion").attr('placeholder', 'Cuéntanos un poco sobre ti');
    $("#id_nombre_escuela").attr('data-provide', "typeahead");
    $("#id_nombre_escuela").attr('autocomplete', "off");
    $('#id_nombre_escuela').typeahead({
        source: function(q, p){
            $.ajax({
                'url': 'http://localhost:8000/api/nombres_escuela',
                'type': 'get',
                'data': {
                    'q': q
                },
                'success': function(msg){
                    arr = eval('('+msg+')');
                    p(arr);
                }
            });
        }
    });
});
