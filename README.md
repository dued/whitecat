# Whitecat

[![Docker Pulls](https://img.shields.io/docker/pulls/dued/whitecat.svg)](https://hub.docker.com/r/dued/whitecat)
[![Layers](https://images.microbadger.com/badges/image/dued/whitecat.svg)](https://microbadger.com/images/dued/whitecat)
[![Commit](https://images.microbadger.com/badges/commit/dued/whitecat.svg)](https://microbadger.com/images/dued/whitecat)
[![License](https://images.microbadger.com/badges/license/dued/whitecat.svg)](https://microbadger.com/images/dued/whitecat)

Whitecat es una imagen docker como proxy de endpoints con Socat (Socket Cat 🔌😼)

Las tecnologías de lista blanca de red han sido una línea de defensa clave para la seguridad de la red local, y con la mayoría de las organizaciones que mueven rápidamente las cargas de trabajo a la nube, también se requerirán los mismos mecanismos. La lista blanca comienza desde una perspectiva de que casi todo es malo. Y, si eso es cierto, debería ser más eficiente solo definir y permitir a las "buenas entidades" en la red (endpoints).

> Un EndPoint es un dispositivo informático remoto que se comunica con una red a la que está conectado.

## Para que sirve?

resuelve: https://github.com/moby/moby/issues/36174.

 Docker admite redes internas; pero cuando las usa, simplemente no puede abrir puertos desde esos servicios, lo cual no es muy conveniente; tiene aislamiento total o ninguno. Este proxy permite que algunos `endpoints` de la lista blanca tengan conectividad de red. Se puede usar para:

* Permitir la conexión solo a algunas API, pero no al resto del mundo .
* Exponer puertos desde un contenedor sin dejar que el contenedor acceda a la WWW.


## Como lo hacemos?

Usa estas variables de entorno

|   Variable de Entorno   | Tipo  | Descripción|
|---|---|---|
| `TARGET`| Obligatorio |   Es el nombre de host al que se redirigirán las conexiones entrantes.|
| `MODE`     |Opcional| por Default: `tcp`. configura a `udp` para proxy en modo UDP. En general: TCP se usa cuando se requiere trasmision de datos con mucha confiabilidad, es decir, que no se pierda información. UDP se usa cuando se buscan transmisiones con una cantidad de información baja en los paquetes y altas velocidades de transferencia, aunque se puedan
| `NAMESERVERS`|Opcional|Por Default: `208.67.222.222 8.8.8.8 208.67.220.220 8.8.4.4` para usar los servidores de resolución OpenDNS y Google DNS de forma predeterminada. Solo se usa cuando la variable [PRE-RESOLVE](#pre-resolve) esta habilitada (enabled = 1).
| `PORT` | Opcional | Por Default: `80 443`. Si está representando servicios HTTP/S, ¡no necesita especificarlo!. El puerto donde escuchará este servicio y donde se espera que el servicio de destino [TARGET](#target) también escuche.
|`PRE_RESOLVE`|Opcional|Por Default: `0` configure a `1` para forzar el uso de los [NAMESERVERS](#nameservers) de nombres especificados para resolver el [TARGET](#target) antes de la proxy ejecución. Esto es especialmente útil cuando se usa un alias de red para incluir en una lista blanca una API externa.|
|`VERBOSE` | Opcional | Por Default: `0`, configura a `1` para logear todas las conexiones|
