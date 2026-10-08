# Simulador de mundo — Maxocracia

Este es un pequeño juego de terminal para experimentar con decisiones y consecuencias.

Empiezas con 11 personas. Tú decides por Max. Las demás personas siguen tomando decisiones por su cuenta.

El tablero muestra varias señales a la vez:

- SDV promedio y mínimo
- bienestar y paz
- comida, salud, conocimiento y ambiente
- confianza y productividad
- personas dentro, en riesgo y fuera
- R (crecimiento), K (capacidad), VHV (huella) y Maxo
- comunidades nuevas y comunidades perdidas
- violaciones y señales de deriva

La idea es que el juego no te diga una respuesta. Tú haces cambios, observas el mundo y descubres qué funciona y qué se rompe.

## Probar

Desde esta carpeta:

~~~bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
./build/maxocracia
~~~

En Windows también puedes abrir el proyecto generado por CMake o ejecutar el binario desde la carpeta `build`.

## Comandos

~~~text
mundo
personas
historia
avanzar 10

max cooperar
max explorar
max descansar
max ayudar 4
max hablar 4
max salir

ayuda
salir
~~~

Una orden de Max se programa para el siguiente ciclo. El comando `avanzar` hace que el mundo siga viviendo.

## Semilla

La partida de prueba usa la semilla 42 para que podamos reproducir una historia y comparar decisiones entre mundos.

## Estado del proyecto

Es un prototipo experimental. Las métricas de Maxocracia están simplificadas para poder jugar y observar el sistema; todavía no son la formalización definitiva de la teoría.
