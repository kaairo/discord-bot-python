# Discord Bot

Este es un bot de Discord diseñado para gestionar roles, registrar eventos en el servidor y manejar un sistema de tickets de soporte.

## Características
- **Gestión de roles**: Asigna roles automáticamente basados en reacciones.
- **Registro de eventos**: Notifica eventos como la entrada/salida de miembros, edición/eliminación de mensajes, creación/eliminación de canales y roles.
- **Sistema de tickets**: Permite a los usuarios abrir tickets según diferentes categorías.
- **Comandos administrativos**:
  - `/welcome_message`: Envía el mensaje de bienvenida en un canal específico.
  - `/ticket_message`: Envía el mensaje para abrir tickets en un canal específico.

## Requisitos
- Python 3.x
- Discord.py
- dotenv

## Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/kaairo/discord-bot-python.git
   cd discord-bot-python
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Crea un archivo `.env` con las siguientes variables:
   ```env
   TOKEN=tu_token_aqui
   GUILD_ID=tu_guild_id
   LOG_CHANNEL=id_del_canal_log
   MEMBER_ROLE=id_del_rol_miembro
   WINDOWS_ROLE=id_del_rol_windows
   ANDROID_ROLE=id_del_rol_android
   TICKET_CATEGORY=id_de_la_categoria_de_tickets
   STAFF_ROLE=id_del_rol_staff
   ```
4. Ejecuta el bot:
   ```bash
   python main.py
   ```

## Uso
- Al iniciar el bot, sincronizará los comandos de la aplicación y estará listo para gestionar roles y tickets.
- Para enviar el mensaje de bienvenida o el mensaje de tickets, usa los comandos `/welcome_message` y `/ticket_message`.

## Contacto
Si tienes dudas o problemas, abre un ticket en Hyaxe Roleplay o contáctanos en Discord.

