El nuevo karelapan
================

Aquí las diferencias del nuevo karelapan con el viejo karelapan.

* Naturalmente el lenguaje es una de ellas, se dejó de usar php en favor de python y django suple a codeigniter como framework. Esto permite un más rápido desarrollo de características nuevas.
* Edición. El nuevo karelapan utiliza la interfaz administrativa de django para proveer de formularios de edición y agregado de problemas, concursos, usuarios y otras cosas.
* FAQs. Ahora las faqs también son parte del sistema en vez de una página estática y se pueden modificar desde la administración de django.
* Mundos. Los mundos ahora son un canvas en vez de svg, esto no dará soporte a IE pero sí permite nuevas características relacionadas con el proyecto karel.js entre las cuales se integra el desplazamiento en el mundo.
* Control del perfil. El nuevo karelapan permite a los usuarios cambiar su contraseña, modificar su perfil y darse de baja del sistema.
* Imanen de perfil. Karelapan ahora usa imágenes de perfil de Gravatar.
* Aviso de privacidad. Un elemento importante dadas las nuevas políticas de protección de datos.
* Base de datos. El nuevo karelapan ahora usa postgresql para manejar su base de datos, aunque realmente también podría ocupar mysql o sqlite por igual.
* Textos. Algunos textos y formatos cambiaron, aunque en general son cambios menores.
* Diseño. Cambiaron algunas vistas como la de 'concursos'.
* Cola de evaluación. Se implementa una cola de evaluación para los problemas del evaluador. Los concursos también se evalúan en la cola de evaluación pero con prioridad sobre los envíos normales.
* Consideraciones y ejemplos. Las consideraciones se editan como parte del problema (pese a seguir siendo una tabla distinta en base de datos) y la tabla de mundos se integró con la tabla de los problemas.
* Integración con el IDE web de karel. Como parte final del proyecto se integró karelapan con karel.js para que los alumnos puedan resolver los problemas directo en el navegador.
* Wiki. EL nuevo karelapan integra la wiki, lugar de documentación sobre karel.
* Preguntas durante el examen. Ahora se podrán realizar preguntas durante un examen para los organizadores.
* Los mundos se muestran en Internet Explorer 9+
