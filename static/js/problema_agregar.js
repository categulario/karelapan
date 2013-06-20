$(document).ready(function(){
    $("#nombre").keyup(function(event){
        $("#nombre_administrativo").val(urlize($('#nombre').val()));
    });
});
