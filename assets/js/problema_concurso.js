var busca_consultas = function(){
    $.ajax({
        'url': 'http://'+$("#host").val()+'/api/consultas/'+$("#id_concurso").val()+'/problema/'+$("#id_problema").val()+'/',
        'type': 'get',
        'success': function(msg){
            var consultas = eval('('+msg+')');
            for(i=0;i<consultas.length;i++){
                if(consultas_existentes.indexOf(consultas[i].id) == -1){
                    //Quiere decir que no la tenemos
                    if(consultas[i].descartado){
                        $("#consultas").prepend('<div class="consulta-bad"><h5>'+consultas[i].mensaje+'</h5><span class="text-error">Rechazada</span></div>');
                    } else {
                        $("#consultas").prepend('<div class="consulta"><h5>'+consultas[i].mensaje+'</h5>'+consultas[i].respuesta+'</div>');
                    }
                    consultas_existentes.push(consultas[i].id);
                }
            }
        }
    });
}

$(document).ready(function(){
    consultas_existentes = []
    $(".consulta-id").each(function(i, elem){
        consultas_existentes.push(parseInt($(elem).val()));
    });
    $("#consulta-form").submit(function(event){
        var data = $(this).serialize();
        $.ajax({
            'url': 'http://'+$("#host").val()+'/api/hacer_consulta/',
            'type': 'post',
            'data': data,
            'success': function(msg){
                if(msg === 'ok'){
                    $("#reset-form").click();
                    $("#mensajes")
                        .removeClass('alert-error')
                        .addClass('alert-success')
                        .text('Consulta enviada, espera la respuesta')
                        .slideDown('slow')
                        .delay(2000)
                        .slideUp('slow');
                } else{
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

intervalo = setInterval(busca_consultas, 1000);
