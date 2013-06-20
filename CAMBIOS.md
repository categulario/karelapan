El nuevo karelapan
================

Aquí las diferencias del nuevo karelapan con el viejo karelapan.

* Naturalmente el lenguaje es una de ellas, se dejó de usar php en favor de python y django suple a codeigniter como framework. Esto permite un más rápido desarrollo de características nuevas.
* Edición. El nuevo karelapan utiliza la interfaz administrativa de django para proveer de formularios de edición y agregado de problemas, concursos, usuarios y otras cosas.
* FAQs. Ahora las faqs también son parte del sistema en vez de una página estática y se pueden modificar desde la administración de django.
* Mundos. Los mundos ahora son un canvas en vez de svg, esto no dará soporte a IE pero sí permite nuevas características relacionadas con el proyecto karel.js entre las cuales se integra el desplazamiento en el mundo.
* Control del perfil. El nuevo karelapan permite a los usuarios cambiar su contraseña, modificar su perfil y darse de baja del sistema.
* Nuevo esquema de evaluación. Aunque esto es transparente para el usuario, resulta una ventaja para el sistema que el nuevo esquema de evaluación ahora usa MongoDB para almacenar los resultados, permitiendo mejor y más rápido control de las evaluaciones por parte de los administradores.
* Aviso de privacidad. Un elemento importante dadas las nuevas políticas de protección de datos.
* Base de datos. El nuevo karelapan ahora usa postgresql para manejar su base de datos, aunque realmente también podría ocupar mysql o sqlite por igual.
* Textos. Algunos textos y formatos cambiaron, aunque en general son cambios menores.
* Cola de evaluación. Se implementa una cola de evaluación para los problemas del evaluador, mientras que los concursos se evalúan en directo.
* Consideraciones y ejemplos. Las consideraciones se editan como parte del problema (pese a seguir siendo una tabla distinta en base de datos) y la tabla de mundos se integró con la tabla de los problemas.
* Integración con el IDE web de karel. Como parte final del proyecto se integró karelapan con karel.js para que los alumnos puedan resolver los problemas directo en el navegador.
* Wiki. EL nuevo karelapan integra la wiki, lugar de documentación sobre karel.
