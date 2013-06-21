/* Cosas para dibujar el canvas del mundo */

var WorldRender = function(context){
    this.should_draw = true;
    this.context = context;

    this.primera_fila = 1;
    this.primera_columna = 1;

    this.num_filas = 1
    this.num_columnas = 1

    this.paint = function(world, mundo_ancho, mundo_alto, track_karel) {

        function dibuja_karel(context, world, origen){ //Dibujar a Karel

            context.fillStyle = '#0000FF';
            context.beginPath();
            if (world.karel.orientacion == 'oeste') { // oeste
                context.moveTo( origen.x, origen.y+15 );
                context.lineTo( origen.x+13, origen.y );
                context.lineTo( origen.x+13, origen.y+7 );
                context.lineTo( origen.x+27, origen.y+7 );
                context.lineTo( origen.x+27, origen.y+23 );
                context.lineTo( origen.x+13, origen.y+23 );
                context.lineTo( origen.x+13, origen.y+30 );
            } else if (world.karel.orientacion == 'norte') { // norte
                context.moveTo ( origen.x, origen.y+13 );
                context.lineTo ( origen.x+15, origen.y );
                context.lineTo ( origen.x+30, origen.y+13 );
                context.lineTo ( origen.x+23, origen.y+13 );
                context.lineTo ( origen.x+23, origen.y+27 );
                context.lineTo ( origen.x+7, origen.y+27 );
                context.lineTo ( origen.x+7, origen.y+13 );
            } else if (world.karel.orientacion == 'este') { // este
                context.moveTo ( origen.x+3, origen.y+7 );
                context.lineTo ( origen.x+17, origen.y+7 );
                context.lineTo ( origen.x+17, origen.y );
                context.lineTo ( origen.x+30, origen.y+15 );
                context.lineTo ( origen.x+17, origen.y+30 );
                context.lineTo ( origen.x+17, origen.y+23 );
                context.lineTo ( origen.x+3, origen.y+23 );
            } else if (world.karel.orientacion == 'sur') { // sur
                context.moveTo ( origen.x+7, origen.y+3 );
                context.lineTo ( origen.x+23, origen.y+3 );
                context.lineTo ( origen.x+23, origen.y+17 );
                context.lineTo ( origen.x+30, origen.y+17 );
                context.lineTo ( origen.x+15, origen.y+30 );
                context.lineTo ( origen.x, origen.y+17);
                context.lineTo ( origen.x+7, origen.y+17);
            }
            context.closePath();
            context.fill();
        }

        context.clearRect(0, 0, mundo_ancho, mundo_alto);
        context.fillStyle="#959595";
        context.fillRect(0, 0, mundo_ancho, mundo_alto);

        var tamanio_lienzo = {x:(mundo_ancho-30), y:(mundo_alto-30)}
        var tamanio_mundo = {x:mundo_ancho, y:mundo_alto}

        context.fillStyle="#FFFFFF"
        context.fillRect(30, 0, tamanio_lienzo.x, tamanio_lienzo.y)

        //IMPORTANTE
        var origen = {x:30, y:mundo_alto-60} //Coordenada para dibujar la primera casilla

        this.num_columnas = (tamanio_lienzo.x/30 + Math.ceil((tamanio_lienzo.x%30)/30.))*1
        this.num_filas = (tamanio_lienzo.y/30 + Math.ceil((tamanio_lienzo.y%30)/30.))*1

        //Cuadrados de las esquinas
        for(var i=0;i<this.num_columnas;i++){
            for(j=0;j<this.num_columnas;j++) {
                x = origen.x+30*i
                y = origen.y-30*j
                context.fillStyle="#656565";
                context.fillRect(x-2, y+26, 6, 6);
            }
        }

        //Dibujar las cosas que pertenecen al mundo por cada casilla
        num_fila = 1 //Posicion relativa a la pantalla
        num_columna = 1 //Posicion relativa a la pantalla
        for(var fila=this.primera_fila;fila<(this.primera_fila+this.num_filas);fila++){
            num_columna = 1
            for(var columna=this.primera_columna;columna<this.primera_columna+this.num_columnas;columna++){
                //Dibujar a karel

                if (world.karel.posicion[0] == fila && world.karel.posicion[1] == columna) {
                    var referencia = {x: origen.x+(num_columna-1)*30, y: origen.y-(num_fila-1)*30};

                    dibuja_karel(context, world, referencia);
                }

                //Paredes
                var casilla = world.casillas_dict[fila+','+columna];
                if(casilla){
                    context.fillStyle="#191919";
                    if (casilla.paredes.indexOf('oeste')!=-1 || columna==1) { // oeste
                        context.fillRect(origen.x+(num_columna-1)*30-1, origen.y-(num_fila-1)*30, 4, 30);
                    }
                    if (casilla.paredes.indexOf('norte')!=-1 || fila==100) { // norte
                        context.fillRect(origen.x+(num_columna-1)*30+1, origen.y-(num_fila-1)*30+27-30, 30, 4);
                    }
                    if (casilla.paredes.indexOf('este')!=-1 || columna==100) { // este
                        context.fillRect(origen.x+(num_columna-1)*30-1+30, origen.y-(num_fila-1)*30, 4, 30);
                    }
                    if (casilla.paredes.indexOf('sur')!=-1 || fila==1) { // sur
                        context.fillRect(origen.x+(num_columna-1)*30+1, origen.y-(num_fila-1)*30+27, 30, 4);
                    }

                    //Zumbadores
                    var zumbadores = casilla.zumbadores;
                    if (zumbadores == -1 || zumbadores > 0) {
                        if (zumbadores == -1) {
                            context.fillStyle = '#00FF00';
                            context.fillRect(origen.x+(num_columna-1)*30+8, origen.y-(num_fila-1)*30+8, 16, 12);

                            context.font = '25px monospace';
                            context.fillStyle = '#000000';
                            context.fillText('∞', origen.x+(num_columna-1)*30+9, origen.y-(num_fila-1)*30+23);
                        } else if (zumbadores < 10) {
                            context.fillStyle = '#00FF00';
                            context.fillRect(origen.x+(num_columna-1)*30+9, origen.y-(num_fila-1)*30+8, 12, 14);

                            context.font = '12px monospace';
                            context.fillStyle = '#000000';
                            context.fillText(String(zumbadores), origen.x+(num_columna-1)*30+11, origen.y-(num_fila-1)*30+20);
                        } else {
                            context.fillStyle = '#00FF00';
                            context.fillRect(origen.x+(num_columna-1)*30+7, origen.y-(num_fila-1)*30+8, 16, 14);

                            context.font = '12px monospace';
                            context.fillStyle = '#000000';
                            context.fillText(String(zumbadores), origen.x+(num_columna-1)*30+8, origen.y-(num_fila-1)*30+20);
                        }
                    }
                } else {
                    context.fillStyle="#191919";
                    if (columna==1) { // oeste
                        context.fillRect(origen.x+(num_columna-1)*30-1, origen.y-(num_fila-1)*30, 4, 30);
                    }
                    if (fila==100) { // norte
                        context.fillRect(origen.x+(num_columna-1)*30+1, origen.y-(num_fila-1)*30+27-30, 30, 4);
                    }
                    if (columna==100) { // este
                        context.fillRect(origen.x+(num_columna-1)*30-1+30, origen.y-(num_fila-1)*30, 4, 30);
                    }
                    if (fila==1) { // sur
                        context.fillRect(origen.x+(num_columna-1)*30+1, origen.y-(num_fila-1)*30+27, 30, 4);
                    }
                }
                num_columna += 1
            }
            num_fila += 1
        }
        this.should_draw = !this.should_draw;
        //Numeros de fila
        var a = 1
        for (i=this.primera_fila;i<this.primera_fila+this.num_filas;i++){
            context.font = "14px monospace"
            context.fillStyle = '#000000'
            context.fillText(""+i,10, mundo_alto-(10+a*30));
            a += 1
        }

        //Numeros de colummna
        a = 1
        for(i=this.primera_columna;i<this.primera_columna+this.num_columnas;i++){
            context.font = '14px monospace'
            context.fillStyle = '#000000'
            context.fillText(""+i,10+30*a, mundo_alto-10);
            a += 1
        }

        $('#mochila').val(world.bagBuzzers);

        //Pad de control
        context.fillStyle = '#305881'
        context.beginPath();
        context.moveTo(tamanio_mundo.x-70+35, 5)
        context.lineTo(tamanio_mundo.x-70+69, 5+55)
        context.lineTo(tamanio_mundo.x-70+35, 5+110)
        context.lineTo(tamanio_mundo.x-70+1, 5+55)
        context.closePath()
        context.fill()


        //Controles de movimiento
        context.fillStyle = '#60b151'
        context.beginPath();
        context.moveTo(mundo_ancho-40-10, 40)
        context.lineTo(mundo_ancho-10-10, 40)
        context.lineTo(mundo_ancho-25-10, 10)
        context.closePath()
        context.fill()

        context.beginPath();
        context.moveTo(mundo_ancho-40-10, 10+70) //Sur
        context.lineTo(mundo_ancho-10-10, 10+70)
        context.lineTo(mundo_ancho-25-10, 40+70)
        context.closePath()
        context.fill()

        context.beginPath();
        context.moveTo(mundo_ancho-25-8, 45) //Este
        context.lineTo(mundo_ancho-25+30-8, 45+15)
        context.lineTo(mundo_ancho-25-8, 45+30)
        context.closePath()
        context.fill()

        context.beginPath();
        context.moveTo(mundo_ancho-25-50+30+8, 45) //Oeste
        context.lineTo(mundo_ancho-25-50+8, 45+15)
        context.lineTo(mundo_ancho-25-50+30+8, 45+30)
        context.closePath()
        context.fill()
        //Mochila

        context.fillStyle = '#A8D9F3';
        context.fillRect(32, 12, 150, 25);

        context.font = '14px monospace';
        context.fillStyle = '#000000';
        if(world.karel.mochila != -1)
            context.fillText('mochila: '+world.karel.mochila, 35, 20);
        else
            context.fillText('mochila: infinito', 35, 30);
    }
}
