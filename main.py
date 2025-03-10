import warnings
warnings.filterwarnings("ignore", category = DeprecationWarning) 

import os
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime

import discord
from discord import app_commands

import traceback

load_dotenv()

GUILD = discord.Object(id = os.getenv('GUILD_ID'))

user_ticket_category = {}

class DiscordClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents = intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild = GUILD)
        await self.tree.sync(guild = GUILD)
        
        self.add_view(TicketCategoryView())
             
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        guild = self.get_guild(payload.guild_id)
        if guild is None:
            return

        reaction_emoji = str(payload.emoji)
        if 'windows' in reaction_emoji or 'android' in reaction_emoji:
            member_role = guild.get_role(int(os.getenv('MEMBER_ROLE')))
            await payload.member.add_roles(member_role)
            
            if 'windows' in reaction_emoji:
                windows_role = guild.get_role(int(os.getenv('WINDOWS_ROLE')))
                await payload.member.add_roles(windows_role)
            
            elif 'android' in reaction_emoji:
                android_role = guild.get_role(int(os.getenv('ANDROID_ROLE')))
                await payload.member.add_roles(android_role)

    async def on_member_join(self, member):
        embed = discord.Embed(
            color = 0x70C05E,
            timestamp = datetime.utcnow()
        )

        embed.set_footer(text = f'{member} (ID: {member.id}) ha ingresado del servidor.', icon_url = member.avatar)
        
        log_channel = client.get_channel(int(os.getenv('LOG_CHANNEL')))
        if log_channel:
            await log_channel.send(embed = embed)

    async def on_member_remove(self, member):
        embed = discord.Embed(
            color = 0xDB4240,
            timestamp = datetime.utcnow()
        )

        embed.set_footer(text = f'{member} (ID: {member.id}) se ha salido del servidor.', icon_url = member.avatar)
        log_channel = client.get_channel(int(os.getenv('LOG_CHANNEL')))
        if log_channel:
            await log_channel.send(embed = embed)

    async def on_message_delete(self, message):
        if message.author.bot:
            return

        embed = discord.Embed(
            title = '🗑️ Mensaje eliminado',
            description = message.content,
            color = 0xDB4240,
            timestamp = datetime.utcnow()
        )

        embed.add_field(name = "Canal", value = f'<#{message.channel.id}> (ID: {message.channel.id}, name: {message.channel})', inline = False)
        embed.set_footer(text = f'{message.author} (ID: {message.author.id})', icon_url = message.author.avatar)

        log_channel = client.get_channel(int(os.getenv('LOG_CHANNEL')))
        if log_channel:
            await log_channel.send(embed = embed)

    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        if before.content == after.content:
            return

        embed = discord.Embed(
            title = '✏️ Mensaje editado',
            color = 0x5D84EC,
            timestamp = datetime.utcnow()
        )

        embed.add_field(name = "Antes", value = before.content, inline = False)
        embed.add_field(name = "Después", value = after.content, inline = False)
        embed.add_field(name = "Canal", value = f'<#{before.channel.id}> (ID: {before.channel.id}, name: {before.channel})', inline = False)

        embed.set_footer(text = f'{before.author} (ID: {before.author.id})', icon_url = before.author.avatar)

        log_channel = client.get_channel(int(os.getenv('LOG_CHANNEL')))
        if log_channel:
            await log_channel.send(embed = embed)

    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(
            title = '💬 Canal creado',
            description = f'<#{channel.id}> (ID: {channel.id}, name: {channel})',
            color = 0x70C05E,
            timestamp = datetime.utcnow()
        )

        log_channel = client.get_channel(int(os.getenv('LOG_CHANNEL')))
        if log_channel:
            await log_channel.send(embed = embed)

    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(
            title = '🗑️ Canal eliminado',
            description = f'<#{channel.id}> (ID: {channel.id}, name: {channel})',
            color = 0xDB4240,
            timestamp = datetime.utcnow()
        )

        log_channel = client.get_channel(int(os.getenv('LOG_CHANNEL')))
        if log_channel:
            await log_channel.send(embed = embed)
        
    async def on_guild_role_create(self, role):
        embed = discord.Embed(
            title = '📜 Rol creado',
            description = f'<@&{role.id}> (ID: {role.id}, name: {role})',
            color = 0x70C05E,
            timestamp = datetime.utcnow()
        )

        log_channel = client.get_channel(int(os.getenv('LOG_CHANNEL')))
        if log_channel:
            await log_channel.send(embed = embed)

    async def on_guild_role_delete(self, role):
        embed = discord.Embed(
            title = '🗑️ Rol eliminado',
            description = f'<@&{role.id}> (ID: {role.id}, name: {role})',
            color = 0xDB4240,
            timestamp = datetime.utcnow()
        )

        log_channel = client.get_channel(int(os.getenv('LOG_CHANNEL')))
        if log_channel:
            await log_channel.send(embed = embed)

intents = discord.Intents.all()
client = DiscordClient(intents = intents)

class TicketCategorySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label = 'Compras', emoji = '<:compras:1239341145075744838>', description = 'Si tienes dudas o problemas relacionados con la compra de productos del servidor.'),
            discord.SelectOption(label = 'Reportar', emoji = '<:reportar:1239341146895810560>', description = 'Si necesitas reportar cualquier comportamiento inapropiado o violación de las reglas.'),
            discord.SelectOption(label = 'Preguntas', emoji = '<:preguntas:1239341143192375307>', description = 'Para dudas generales o aclaraciones sobre cómo funciona el servidor.'),
            discord.SelectOption(label = 'Bug', emoji = '<:bug:1239341141845872650>', description = 'Si tiene dificultades técnicas dentro del servidor.'),
            discord.SelectOption(label = 'Otros', emoji = '<:otros:1239341140415611010>', description = 'Para cualquier tema que no entre en las categorías anteriores.')
        ]
        
        super().__init__(placeholder = 'Seleccione una categoría', custom_id = 'ticket_categories', options = options)
        
    async def callback(self, interaction: discord.Interaction):
        user_ticket_category[interaction.user.id] = self.values[0]
        await interaction.response.send_modal(OpenTicket())

class TicketCategoryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
        self.add_item(TicketCategorySelect())

class OpenTicket(discord.ui.Modal, title = 'Abrir ticket'):
    feedback = discord.ui.TextInput(
        label = 'Cuéntanos lo que necesitas',
        style = discord.TextStyle.long,
        placeholder = '',
        required = True,
        max_length = 512,
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = discord.utils.get(interaction.guild.categories, id = int(os.getenv('TICKET_CATEGORY')))
        staff_role = discord.utils.get(interaction.guild.roles, id = int(os.getenv('STAFF_ROLE')))
        
        channel = await guild.create_text_channel(name = f'❔︲{interaction.user.name}-ticket', category = category)
            
        await channel.set_permissions(interaction.guild.get_role(interaction.guild.id), send_messages = False, read_messages = False)
        await channel.set_permissions(interaction.user, send_messages = True, read_messages = True, add_reactions = True, embed_links = True, attach_files = True, read_message_history = True, external_emojis = True)
        await channel.set_permissions(staff_role, send_messages = True, read_messages = True, add_reactions = True, embed_links = True, attach_files = True, read_message_history = True, external_emojis = True, manage_messages = True)

        file = discord.File('static/ticket.png', filename = 'ticket.png')

        embed = discord.Embed(colour = 0xbd3c3c, title = 'Ticket de soporte', description = 'Espere hasta que sea atendido por un administrador.')
        embed.add_field(name = 'Tipo de ticket', value = f'```{user_ticket_category[interaction.user.id]}```', inline = False)
        embed.add_field(name = 'Descripción', value = f'```{self.feedback.value}```', inline = False)
        
        embed.set_thumbnail(url = 'attachment://ticket.png')
        
        await channel.send(content = f'{interaction.user.mention} {staff_role.mention}', file = file , embed = embed)

        await interaction.response.send_message(f'✅ Tu ticket ha sido creado: <#{channel.id}>', ephemeral = True, delete_after = 5)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('❌ ¡Ups! Algo salió mal. Póngase en contacto con los administradores si el problema persiste.', ephemeral = True, delete_after = 5)
        traceback.print_exception(type(error), error, error.__traceback__)

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = 'hyaxe.com'))
    print(f'Logged in as {client.user} (ID: {client.user.id})')

@client.tree.command(description = 'Envía el mensaje de bienvenida')
@app_commands.checks.has_permissions(administrator = True)
@app_commands.describe(dest_channel = 'Canal de destino')
async def welcome_message(interaction: discord.Interaction, dest_channel: discord.TextChannel):
    file = discord.File('static/welcome.png', filename = 'welcome.png')
    embed = discord.Embed()

    embed = discord.Embed(colour = 0x2a2c31, description = '<:discord_logo:1239345181912727633> **¡Bienvenido a Hyaxe Roleplay!**\n\nNuestro servidor Hyaxe está diseñado para ofrecerte una **experiencia simple, divertida y de alta calidad técnica**, tanto en PC como en dispositivos móviles. Cada detalle se ha pensado meticulosamente para garantizar tu satisfacción.\n\nPara una experiencia sin problemas, te invitamos a revisar nuestras <#674089059756539905>. Si necesitas asistencia o tienes preguntas, nuestro equipo está disponible en cualquier momento. ¡Solo abre un ticket en nuestro canal <#1238623208433909841> y te ayudaremos de inmediato!\n\nPara acceder al servidor reacciona con al menos un emoji de las opciones:\n<:android:1239310004398461078> Android\n<:windows:1239309861288939592> Windows')
    embed.set_image(url = 'attachment://welcome.png')
    
    message = await dest_channel.send(file = file, embed = embed)
    await message.add_reaction('<:android:1239310004398461078>')
    await message.add_reaction('<:windows:1239309861288939592>')
    
    await interaction.response.send_message(content = f'✅ Mensaje de bienvenida enviado al canal <#{dest_channel.id}>')

@client.tree.command(description = 'Envía el mensaje para abrir los tickets')
@app_commands.checks.has_permissions(administrator = True)
@app_commands.describe(dest_channel = 'Canal de destino')
async def ticket_message(interaction: discord.Interaction, dest_channel: discord.TextChannel):
    file = discord.File('static/open_ticket.png', filename = 'open_ticket.png')
    embed = discord.Embed()

    embed = discord.Embed(colour = 0x2a2c31, description = '<:discord_logo:1239345181912727633> **Hyaxe Roleplay | Sistema de soporte**\n\nSi necesita ayuda o desea informar algo en el servidor, ¡estamos aquí para ayudarlo! Para abrir un ticket, simplemente selecciona la opción correspondiente a tu necesidad:\n\n<:compras:1239341145075744838> **Compras:** Si tienes dudas o problemas relacionados con la compra de productos del servidor.\n<:reportar:1239341146895810560> **Reportar:** Si necesitas reportar cualquier comportamiento inapropiado o violación de las reglas.\n<:preguntas:1239341143192375307> **Preguntas:** Para dudas generales o aclaraciones sobre cómo funciona el servidor.\n<:bug:1239341141845872650> **Bug:** Si tienes dificultades técnicas dentro del servidor.\n<:otros:1239341140415611010> **Otros:** Para cualquier tema que no entre en las categorías anteriores.')
    embed.set_image(url = 'attachment://open_ticket.png')
    
    await dest_channel.send(file = file, embed = embed, view = TicketCategoryView())
    
    await interaction.response.send_message(content = f'✅ Mensaje de ticket enviado al canal <#{dest_channel.id}>')

client.run(os.getenv('TOKEN'))