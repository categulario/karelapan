var karelize = function(contenedor, fila_inicio, fila_fin, columna_inicio, columna_fin, mundo, base_url){
    /* Construye el mundo de karel
     */
    console.log(fila_inicio+','+fila_fin+','+columna_inicio+','+columna_fin);
    if(!base_url)
        base_url = '';
    if(!fila_inicio)
        fila_inicio=1
    if(!fila_fin)
        fila_fin=11
    if(!columna_inicio)
        columna_inicio=1
    if(!columna_fin)
        columna_fin=15
    if(!mundo){
        mundo = {
            "karel": {
                "posicion": [1, 1],
                "orientacion": "norte"
            },
            "casillas":[]
        }
    }
    fila = mundo.karel.posicion[0];
    columna = mundo.karel.posicion[1];
    orientacion = mundo.karel.orientacion;
    casillas = mundo.casillas;
    //Lo primero es verificar los datos usados
    if(fila_inicio>fila_fin || columna_inicio>columna_fin){
        console.log('Las columnas o filas de inicio y fin no son congruentes')
        return false;
    }
    if(100<fila_inicio || fila_inicio<1 || 100<columna_inicio || columna_inicio<1 || 100<fila_fin || fila_fin<1 || 100<columna_fin || columna_fin<1){
        console.log('Las filas o columnas de inicio o fin están fuera de los márgenes')
        return false;
    }
    if(fila<fila_inicio || fila>fila_fin || columna<columna_inicio || columna>columna_fin){
        console.log('Karel está fuera del área mostrada')
        return false;
    }
    if(orientacion != 'norte' && orientacion != 'este' && orientacion != 'oeste' && orientacion != 'sur'){
        console.log('La orientación no está dentro de las permitidas')
        return false;
    }

    //Se limpia el contenedor
    document.getElementById(contenedor).innerHTML = "";

    var filas = fila_fin-fila_inicio+1;
    var columnas = columna_fin-columna_inicio+1;
    //Calculo de valores
    var ancho = columnas*20 + 20*(columna_inicio ==1) + 20*(columna_fin==100);
    var alto = filas*20 + 20*(fila_inicio == 1) +20*(fila_fin == 100);
    var R = Raphael(contenedor, ancho, alto);
    //El fondo gris
    R.rect(0, 0, ancho, alto).attr({fill: "#ccc", "fill-opacity": 1, "stroke": "none"});
    //Cuadro blanco
    R.rect(20*(columna_inicio == 1), 20*(fila_fin == 100), ancho-(20*(columna_inicio==1) + 20*(columna_fin==100)), alto-(20*(fila_inicio==1) + 20*(fila_fin==100)))
        .attr({fill: "#fff", "fill-opacity": 1, "stroke": "none"});
    //Cuadritos de las esquinas
    for(i=0 ; i<=columnas ; i++){
        for(j=0 ; j<=filas ; j++){
            R.rect(-2+i*20 + 20*(columna_inicio==1), -4+j*20 + 20*(fila_fin==100), 6, 6)
                .attr({fill: "#808080", "fill-opacity": 1, "stroke": "none"});
        }
    }
    //Numeros de fila
    if(columna_inicio == 1){
        //Significa que hay que poner numeros de fila
        for(i=fila_inicio ; i<=fila_fin; i++){
            R.text(10, (filas-1)*20+10 - (i-fila_inicio)*20+(fila_fin==100)*20, String(i)).attr({fill: "#fff", "fill-opacity": 1, "stroke": "1"});
        }
    }
    if(columna_fin == 100){
        //Significa que hay que poner numeros de fila al final
        for(i=fila_inicio ; i<=fila_fin; i++){
            R.text(columnas*20+10+20*(columna_inicio==1), (filas-1)*20+10 - (i-fila_inicio)*20 + 20*(fila_fin==100), String(i)).attr({fill: "#fff", "fill-opacity": 1, "stroke": "1"});
        }
    }
    if(fila_inicio == 1){
        //Significa que hay que poner numeros de columna
        for(i=columna_inicio ; i<=columna_fin; i++){
            R.text(10 + (i-columna_inicio)*20 + 20*(columna_inicio==1), filas*20+10+20*(fila_fin==100), String(i)).attr({fill: "#fff", "fill-opacity": 1, "stroke": "1"});
        }
    }
    if(fila_fin == 100){
        //Significa que hay que poner numeros de columna hasta arriba
        for(i=columna_inicio ; i<=columna_fin; i++){
            R.text(10 + (i-columna_inicio)*20 + 20*(columna_inicio==1), 10, String(i)).attr({fill: "#fff", "fill-opacity": 1, "stroke": "1"});
        }
    }
    //Los zumbadores del mundo
    console.log(fila_inicio+','+fila_fin+','+columna_inicio+','+columna_fin);
    casillas.forEach(function(casilla){
        if(casilla.fila <= fila_fin && casilla.fila>=fila_inicio && casilla.columna <= columna_fin && casilla.columna>=columna_inicio){
            //Sí está en el margen de visión, podemos pintarla
            //Los zumbadores
            if(casilla.zumbadores){
                if(casilla.zumbadores == -1){ //Infinitos
                    R.image(base_url+"img/zumbadores/bkarel_inf.png", (casilla.columna-columna_inicio)*20 + (columna_inicio==1)*20, (filas-casilla.fila)*20 + 20*(fila_fin == 100), 20, 20);
                } else {
                    R.image(base_url+"img/zumbadores/bkarel_"+String(casilla.zumbadores)+".png", (casilla.columna-columna_inicio)*20 + (columna_inicio==1)*20, (filas-casilla.fila)*20 + 20*(fila_fin == 100), 20, 20);
                }
            }
        } else {
            console.log('fuera del area ('+casilla.fila+', '+casilla.columna+')');
        }
    });
    //La posición de Karel
    if(orientacion=='norte'){
        R.path("m "+String((columna-columna_inicio)*20 + (columna_inicio==1)*20)+","+String((filas-fila)*20 + 20*(fila_fin == 100)+10)+" 10,-10 10,10 -6,0 0,10 -8,0 0,-10 z").attr({"stroke":"#1A19E1", "stroke-width": 2});
    } else if (orientacion=='sur'){
        R.path("m "+String((columna-columna_inicio)*20 + (columna_inicio==1)*20+20)+","+String((filas-fila)*20 + 20*(fila_fin == 100)+10)+" -10,10 -10,-10 6,0 0,-10 8,0 0,10").attr({"stroke":"#1A19E1", "stroke-width": 2});
    } else if(orientacion=='este'){
        R.path("m "+String((columna-columna_inicio)*20 + (columna_inicio==1)*20+10)+","+String((filas-fila)*20 + 20*(fila_fin == 100))+" 10,10 -10,10 0,-6 -10,0 0,-8 10,0 z").attr({"stroke":"#1A19E1", "stroke-width": 2});
    } else {
        R.path("m "+String((columna-columna_inicio)*20 + (columna_inicio==1)*20+10)+","+String((filas-fila)*20 + 20*(fila_fin == 100)+20)+" -10,-10 10,-10 0,6 10,0 0,8 -10,0 z").attr({"stroke":"#1A19E1", "stroke-width": 2});
    }
    //Las paredes del mundo
    casillas.forEach(function(casilla){
        if(casilla.fila <= fila_fin && casilla.fila>=fila_inicio && casilla.columna <= columna_fin && casilla.columna>=columna_inicio){
            //Sí está en el margen de visión, podemos pintarla
            casilla.paredes.forEach(function(pared){
                if(pared == 'norte'){
                    R.rect(1+(casilla.columna-columna_inicio)*20 + (columna_inicio==1)*20, (filas-casilla.fila)*20 + 20*(fila_fin == 100)-3, 20, 4).attr({fill: "#000", "fill-opacity": 1, "stroke": "none"})
                }
                if(pared == 'sur'){
                    R.rect(1+(casilla.columna-columna_inicio)*20 + (columna_inicio==1)*20, (filas-casilla.fila)*20 + 20*(fila_fin == 100)+17, 20, 4).attr({fill: "#000", "fill-opacity": 1, "stroke": "none"})
                }
                if(pared == 'este'){
                    R.rect(19+(casilla.columna-columna_inicio)*20 + (columna_inicio==1)*20, (filas-casilla.fila)*20 + 20*(fila_fin == 100)-1, 4, 20).attr({fill: "#000", "fill-opacity": 1, "stroke": "none"})
                }
                if(pared == 'oeste'){
                    R.rect((casilla.columna-columna_inicio)*20 + (columna_inicio==1)*20-1, (filas-casilla.fila)*20 + 20*(fila_fin == 100)-1, 4, 20).attr({fill: "#000", "fill-opacity": 1, "stroke": "none"})
                }
            });
        }
    });
    //La mochila
    R.rect(ancho-100, 1, 100, 18).attr({fill: "#4cf", "fill-opacity": .5, "stroke": "none"});
    if(mundo.karel.mochila != -1){
        R.text(ancho-60, 10, 'mochila: '+mundo.karel.mochila).attr({fill: "#000", "fill-opacity": 1, "stroke": "1", "font-size": 16});
    } else {
        R.text(ancho-60, 10, 'mochila: inf').attr({fill: "#000", "fill-opacity": 1, "stroke": "1", "font-size": 16});
    }
}
