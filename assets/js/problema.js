$(document).ready(function(){
    //Creamos los canvas para dibujar
    $("#kworld").css({height:'400px', backgroundColor:'#7F4646'});
    var canvas1 = document.createElement('canvas');
    canvas1.width = $("#kworld").width();
    canvas1.height = $("#kworld").height();
    canvas1.id = 'mundo_ejemplo';
    $("#kworld").html(canvas1);
    $("#ksolution").css({height:'400px', backgroundColor:'#7F4646'});
    var canvas2 = document.createElement('canvas');
    canvas2.width = $("#ksolution").width();
    canvas2.height = $("#ksolution").height();
    canvas2.id = 'mundo_solucion';
    $("#ksolution").html(canvas2);
});
