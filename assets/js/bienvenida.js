$(document).ready(function(){
    //Creamos los canvas para dibujar
    var canvas1         = $("#mundo_ejemplo")[0];
    canvas1.width       = $("#kworld").width();
    canvas1.height      = $("#kworld").height();
    var context         = canvas1.getContext('2d');
    var wRender         = new WorldRender(context);
    mundo_ejemplo   = {}
    mundo_ejemplo = eval('('+$("#kworldcontent").val()+')');
    mundo_ejemplo.casillas_dict = {};
    for(var i=0;i<mundo_ejemplo.casillas.length;i++){
        mundo_ejemplo.casillas_dict[mundo_ejemplo.casillas[i].fila+','+mundo_ejemplo.casillas[i].columna] = {
            'paredes': mundo_ejemplo.casillas[i].paredes,
            'zumbadores': mundo_ejemplo.casillas[i].zumbadores
        }
    }
    wRender.paint(mundo_ejemplo, canvas1.width, canvas1.height);
    $(window).resize(function(event) {
        $("#mundo_ejemplo").attr('width', $("#kworld").width());
        wRender.paint(mundo_ejemplo, canvas1.width, canvas1.height);
    });
    $("#mundo_ejemplo").click(function(event){
        var x = event.offsetX;
        var y = event.offsetY;
        //Maneja los clicks en el mundo
        if ((canvas1.width-50)<=x && x <=(canvas1.width-20) && 10<=y && y<=40) {
            //NORTE
            if (wRender.primera_fila+wRender.num_filas-2 < 100)
                wRender.primera_fila += 1
        } else if ((canvas1.width-50)<=x && x<=(canvas1.width-20) && 80<=y && y<=110) {
            //SUR
            if (wRender.primera_fila > 1)
                wRender.primera_fila -= 1
        } else if ((canvas1.width-50+17)<=x && x<=(canvas1.width-20+17) && 45<=y && y<=75) {
            //ESTE
            if (wRender.primera_columna+wRender.num_columnas-2 < 100)
                wRender.primera_columna += 1
        } else if ((canvas1.width-50+17-35)<=x && x<=(canvas1.width-20+17-35) && 45<=y && y<=75) {
            //OESTE
            if (wRender.primera_columna > 1)
                wRender.primera_columna -= 1
        }
        wRender.paint(mundo_ejemplo, canvas1.width, canvas1.height);
    });
    $("#mundo_ejemplo")[0].onmousewheel = function(event){
        if(event.wheelDeltaX < 0 && (wRender.primera_columna + wRender.num_columnas)<102) {
            wRender.primera_columna += 1;
        } else if(event.wheelDeltaX > 0 && wRender.primera_columna > 1) {
            wRender.primera_columna -= 1;
        }

        if(event.wheelDeltaY > 0 && (wRender.primera_fila + wRender.num_filas)<102) {
            wRender.primera_fila += 1;
        } else if(event.wheelDeltaY < 0 && wRender.primera_fila > 1) {
            wRender.primera_fila -= 1;
        }

        wRender.paint(mundo_ejemplo, canvas1.width, canvas1.height);
        return false;
    };
});
