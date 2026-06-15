# TA-update-checker

Chequeador automático de actualizaciones de **Trimble Access**.

Este proyecto monitorea la página oficial de release notes de Trimble Access y envía una notificación por correo electrónico cuando se detecta una nueva versión disponible.

Actualmente está implementado en el laboratorio GPS de GEOCOM para mantener al equipo informado sobre nuevas actualizaciones del software de campo.

## Funcionamiento

El script descarga la página oficial de release notes:

https://help.fieldsystems.trimble.com/trimble-access-release-notes/es/home.htm

Luego extrae el contenido HTML y busca versiones con el formato: `YYYY.X (ej: 2026.10)`


## Comportamiento del script

Si se detecta una nueva versión:

- Se envía un correo electrónico de notificación al equipo
- Se actualiza el archivo de estado `last_version.txt`

Si no hay cambios:

- El script finaliza sin acciones adicionales
