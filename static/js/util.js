function esCorreo(valor) {
    // Determina si es un correo valido
    re=/^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,3})$/
    if(re.exec(valor)){
        return true;
    } else {
        return false;
    }
}

function urlize(str) {
    /* Convierte una cadena a algo utilizable en una URL
     * solo permite pasar las letras, guiones y guiones bajos
     * el resto desaparece
     */
    str=str.toLowerCase();
    news="";
    for(i=0;i<str.length;i++) {
        switch(str.charAt(i)) {
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
                news+=str.charAt(i);
                break;
            case " ":
                news+="_";
                break;
            default:
                if(str.charCodeAt(i)==225) { // a agudo
                  news+="a";
                }
                if(str.charCodeAt(i)==233) {// e agudo
                  news+="e";
                }
                if(str.charCodeAt(i)==237) {// i agudo
                  news+="i";
                }
                if(str.charCodeAt(i)==243) {// o agudo
                  news+="o";
                }
                if(str.charCodeAt(i)==250) {// u agudo
                  news+="u";
                }
                if(str.charCodeAt(i)==241) {// n tilde
                  news+="n";
                }
                if(str.charCodeAt(i)==252) {// u dieresis
                  news+="u";
                }
                break;
        }
    }
    return news;
}
