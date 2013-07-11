$(document).ready(function(){
    $("#id_fecha_nacimiento").datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: "1950:2012",
        dateFormat: "dd/mm/yy"
    });
    $("#id_descripcion").attr('placeholder', 'Cuéntanos un poco sobre ti');
    $("#id_nombre_escuela").attr('data-provide', "typeahead");
    $("#id_nombre_escuela").attr('autocomplete', "off");
    $('#id_nombre_escuela').typeahead({
        source: function(q, p){
            $.ajax({
                'url': 'http://'+$("#host").val()+'/api/nombres_escuela',
                'type': 'get',
                'data': {
                    'q': q
                },
                'success': function(msg){
                    arr = eval('('+msg+')');
                    p(arr);
                }
            });
        }
    });
    $("#id_fecha_nacimiento").attr("placeholder", 'dd/mm/yyyy');
    $("#id_correo").popover({
        'trigger': 'focus',
        'content': 'Indica una dirección de correo electrónico'
    });
    $("#id_nivel_estudios").popover({
        'trigger': 'focus',
        'content': '¿Que nivel de estudios concluidos tienes?'
    });
    $("#id_grado_actual").popover({
        'trigger': 'focus',
        'content': '¿Que nivel estás estudiando actualmente?'
    });
    $("#id_subsistema").popover({
        'trigger': 'focus',
        'content': '¿A qué subsistema pertenece tu escuela? Si no sabes vale la pena preguntar'
    });
    $("#id_grupo").popover({
        'trigger': 'focus',
        'content': '¿Te identificas con alguno de estos grupos? Si no, simplemente elige "usuarios". Puedes elegir más de uno usando la tecla Ctrl del teclado'
    });
    $("#id_asesor").popover({
        'trigger': 'focus',
        'title': '¿Alguien te asesora?',
        'content': 'Es necesario que tu asesor se haya registrado antes, aunque también lo puedes indicar posteriormente'
    });
    $("#id_nombre_escuela").popover({
        'trigger': 'focus',
        'title': '¿Cómo se llama tu escuela?',
        'content': 'Trata de usar el nombre completo de tu escuela, como "Escuela Secundaria General No. 2 Julio Zárate"'
    });
    $("#id_descripcion").popover({
        'trigger': 'focus',
        'content': 'Cuéntanos en breves letras qué te gusta hacer'
    });
    $("#id_ultima_omi").popover({
        'trigger': 'focus',
        'title': '¿Cuál es el último año en que puedes participar en la olimpiada de informática?',
        'content': 'Los alumnos pueden competir hasta cuarto semestre del bachillerato, si no sabes escoge 1512'
    });
});
