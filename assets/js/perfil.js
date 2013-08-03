$(document).ready(function(){
    nombres_dict = {};
    $.ajax({
        'url': '/api/obten_nombre_asesor/'+$("#id_asesor").val()+'/',
        'type': 'get',
        'success': function(msg){
            nombres_dict[msg] = $("#id_asesor").val();
            $("#id_nombre_asesor").val(msg);
        }
    })
    $("#id_asesor").closest('.control-group').hide();
    $("#id_nombre_asesor").attr('autocomplete', "off");
    $('#id_nombre_asesor').typeahead({
        source: function(query, process){
            $.ajax({
                'url': '/api/nombres_asesores/',
                'type': 'get',
                'data': {
                    'q': query
                },
                'success': function(msg){
                    var arr = eval('('+msg+')');
                    var nombres = [];
                    nombres_dict={};
                    for(var i=0;i<arr.length;i++){
                        nombres_dict[arr[i].nombre] = arr[i].id;
                        nombres.push(arr[i].nombre);
                    }
                    process(nombres);
                }
            });
        },
        updater: function(item){
            $("#id_asesor").val(nombres_dict[item]);
            return item;
        }
    });
    $('#id_nombre_asesor').keyup(function(event){
        if($(this).val() == ''){
            $("#id_asesor").val('');
        }
    });
    $("#id_fecha_nacimiento").attr("placeholder", 'dd/mm/yyyy');
    $("#id_nombre_asesor").popover({
        'trigger': 'focus',
        'title': '¿Alguien te asesora?',
        'content': 'Es necesario que tu asesor se haya registrado antes, aunque también lo puedes indicar posteriormente'
    });
});
