$(document).ready(function(){
    $(".responde-consulta").submit(function(event){
        data = $(this).serialize();
        div_mensaje = $(this).closest('.consulta-bad');
        respuesta = $(this).closest('.consulta-bad').find('textarea').val();
        componentes = $(this).closest('.consulta-bad').find('.components');
        $.ajax({
            'url': 'http://'+$("#host").val()+'/api/responde_consulta/',
            'type': 'post',
            'data': data,
            'success': function(msg) {
                if(msg === 'ok'){
                    $("#mensajes")
                        .removeClass('alert-error')
                        .addClass('alert-success')
                        .text('Respuesta enviada')
                        .slideDown('slow')
                        .delay(2000)
                        .slideUp('slow');
                    $(div_mensaje)
                        .removeClass('consulta-bad')
                        .addClass('consulta');
                    $(componentes).remove();
                    $(div_mensaje).append(respuesta);
                } else if (msg === 'consulta rechazada') {
                    $("#mensajes")
                        .removeClass('alert-success')
                        .addClass('alert-error')
                        .text('Consulta rechazada')
                        .slideDown('slow')
                        .delay(2000)
                        .slideUp('slow');
                    $(componentes).remove();
                    $(div_mensaje).append('<span class="text-error">Rechazada</span>');
                } else {
                    $("#mensajes")
                        .removeClass('alert-success')
                        .addClass('alert-error')
                        .text(msg)
                        .slideDown('slow')
                        .delay(2000)
                        .slideUp('slow');
                }
            }
        });
        return false;
    });
    $(".rechazar-consulta").click(function(event){
        $(this).closest('form').find('.rechazar-hidden').val('1');
        $(this).closest('form').submit();
    });
});

var busca_consultas = function(){
    $.ajax({
        'url': 'http://'+$("#host").val()+'/api/busca_consultas/'+$("#id_concurso").val()+'/',
        'type': 'get',
        'success': function(msg){
            var consultas = eval('('+msg+')');
            console.log(consultas);
        }
    })
}

interval = setInterval(busca_consultas, 1000);
