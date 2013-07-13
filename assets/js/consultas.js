envia_respuesta = function(self){
    data = $(self).serialize();
    div_mensaje = $(self).closest('.consulta-bad');
    respuesta = $(self).closest('.consulta-bad').find('textarea').val();
    componentes = $(self).closest('.consulta-bad').find('.components');
    $.ajax({
        'url': 'http://'+$("#host").val()+'/api/responde_consulta/',
        'type': 'post',
        'data': data,
        'success': function(msg) {
            if(msg === 'ok'){
                $(div_mensaje)
                    .removeClass('consulta-bad')
                    .addClass('consulta');
                $(componentes).remove();
                $(div_mensaje).append(respuesta);
            } else if (msg === 'consulta rechazada') {
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
}

rechaza_respuesta = function(self){
    $(self).closest('form').find('.rechazar-hidden').val('1');
    $(self).closest('form').submit();
}

$(document).ready(function(){
    //~ $(".responde-consulta").submit(envia_respuesta);
    //~ $(".rechazar-consulta").click(rechaza_respuesta);
    consultas_existentes = []
    $(".consulta-id").each(function(i, elem){
        consultas_existentes.push(parseInt($(elem).val()));
    });
    $("#aclaracion-general").submit(function(event){
        data = $(this).serialize();
        $.ajax({
            'url': 'http://'+$("#host").val()+'/api/aclaracion/'+$("#id_concurso").val()+'/',
            'type': 'post',
            'data': data,
            'success': function(msg){
                if(msg==='ok'){
                    $("#reset-aclaracion").click();
                    $("#mensajes")
                        .removeClass('alert-error')
                        .addClass('alert-success')
                        .text('Aclaración enviada a todos los alumnos')
                        .slideDown('slow')
                        .delay(2000)
                        .slideUp('slow');
                    history.go(0);
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
});

var busca_consultas = function(){
    $.ajax({
        'url': 'http://'+$("#host").val()+'/api/busca_consultas/'+$("#id_concurso").val()+'/',
        'type': 'get',
        'success': function(msg){
            var consultas = eval('('+msg+')');
            for(i=0;i<consultas.length;i++){
                if(consultas_existentes.indexOf(consultas[i].id) == -1){
                    //Quiere decir que no la tenemos
                    $("#mensajes").after('<div class="consulta-bad"><input type="hidden" class="consulta-id" value="'+consultas[i].id+'"><h5>'+consultas[i].mensaje+' <span class="muted">Problema: '+consultas[i].problema+', Usuario: '+consultas[i].usuario+'</span> '+consultas[i].hora+'</h5><form class="responde-consulta" method="post" onsubmit="return envia_respuesta(this);"><div class="components"><textarea class="input-xxlarge" rows="3" name="respuesta"></textarea> <input type="hidden" name="consulta" value="'+consultas[i].id+'"><input type="hidden" name="rechazar" class="rechazar-hidden"><input type="submit" value="Enviar" class="btn"> <input type="button" value="Rechazar" class="rechazar-consulta btn btn-danger" onclick="rechaza_respuesta(this);"></div></form></div>');
                    consultas_existentes.push(consultas[i].id);
                }
            }
        }
    });
}

interval = setInterval(busca_consultas, 1000);
