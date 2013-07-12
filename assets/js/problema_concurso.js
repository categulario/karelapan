$(document).ready(function(){
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
