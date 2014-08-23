<?php

$entrada = "
Esto es el texto de prueba para una [wiki media truculentísima] que va a
funcionar muy [genial], {realmente} os digo que si, va a hablar sobre
karel el robot y sus magias [burundangas]
";

function urlize($char) {
    /* Convierte una cadena a algo utilizable en una URL
     * solo permite pasar las letras, guiones y guiones bajos
     * el resto desaparece
     */
    $char = strtolower($char);
    switch($char) {
        case "a":
        case "b":
        case "c":
        case "d":
        case "e":
        case "f":
        case "g":
        case "h":
        case "i":
        case "j":
        case "k":
        case "l":
        case "m":
        case "n":
        case "o":
        case "p":
        case "q":
        case "r":
        case "s":
        case "t":
        case "u":
        case "v":
        case "w":
        case "x":
        case "y":
        case "z":
        case "-":
        case "_":
            return $char;
            break;
        case " ":
            return '_';
            break;
        default:
            if($char == 'á') { // a agudo
              return 'a';
            }
            if($char == 'é') {// e agudo
              return 'e';
            }
            if($char == 'í') {// i agudo
              return 'i';
            }
            if($char == 'ó') {// o agudo
              return 'o';
            }
            if($char == 'ú') {// u agudo
              return 'u';
            }
            if($char == 'ñ') {// n tilde
              return 'n';
            }
            if($char == 'ü') {// u dieresis
              return 'u';
            }
            break;
    }
    return '';
}

function reemplaza($texto_original){
    define('ESTADO_TEXTO', 1);
    define('ESTADO_ENLACE', 2);
    define('ESTADO_MEDIO', 3);
    define('ESTADO_ESCAPE', 4);


    $estado = ESTADO_TEXTO;
    $len = strlen($texto_original);
    $salida = '';
    $token = '';
    $original = '';

    $i=0;
    while($i<$len){
        $caracter_actual = $texto_original[$i];
        switch($estado){
            case ESTADO_TEXTO: {
                    if($caracter_actual == '['){
                        $estado = ESTADO_ENLACE;
                    } elseif($caracter_actual == '{') {
                        $estado = ESTADO_MEDIO;
                    } elseif($caracter_actual == '\\'){
                        $estado = ESTADO_ESCAPE;
                    } else {
                        $salida .= $caracter_actual;
                    }
                };
                break;
            case ESTADO_ENLACE: {
                    if($caracter_actual == ']'){
                        $estado = ESTADO_TEXTO;
                        $salida .= '<a href="http://server.com/wiki/'.$token.'">'.$original.'</a>';
                        $token = '';
                        $original = '';
                    } else {
                        $token .= urlize($caracter_actual);
                        $original .= $caracter_actual;
                    }
                };
                break;
            case ESTADO_ESCAPE: { //Omitimos el caracter actual sea cual sea =)
                    $estado = ESTADO_TEXTO;
                };
                break;
            case ESTADO_MEDIO: {
                    if($caracter_actual == '}'){
                        $estado = ESTADO_TEXTO;
                        $salida .= '<img src="http://server.com/wiki/media/'.$token.'">';
                        $token = '';
                    } else {
                        $token .= urlize($caracter_actual);
                    }
                };
                break;
        }
        $i++;
    }

    return $salida;
}

echo reemplaza($entrada);
