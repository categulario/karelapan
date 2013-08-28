$(document).ready(function(){
    $(".puntaje-select").click(function(event){
        $("#puntaje-button").html($(this).text() + ' <span class="caret"></span>');
        $("#puntaje-ref").val($(this).attr('data-value'));
    });
    $(".problemas-select").click(function(event){
        $("#problemas-button").html($(this).text() + ' <span class="caret"></span>');
        $("#problemas-ref").val($(this).attr('data-value'));
    });
});
