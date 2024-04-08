import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='YOUR_CLIENT_ID',
                                                                             client_secret='YOUR_CLIENT_SECRET'))

voiceChannels = [VOICECHANNELS_ID]

playlist_uri = 'YOUR_PLAYLIST_URI'
playlist_tracks = []


@client.event
async def on_ready():
    logger.info('The bot is ready to go')


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel.id in voiceChannels:
        voice_client = discord.utils.get(client.voice_clients, guild=member.guild)
        if not voice_client:
            try:
                voice_client = await after.channel.connect()
            except:
                pass

        def play_next_song(error=None):
            if playlist_tracks:
                track_uri = playlist_tracks.pop(0)
                voice_client.play(discord.FFmpegPCMAudio(source=track_uri, executable="ffmpeg", options="-af volume=0.5"), after=play_next_song)

        play_next_song()

    elif before.channel.id in voiceChannels and after.channel not in voiceChannels:
        if len(before.channel.members) == 1:
            voice_client = discord.utils.get(client.voice_clients, guild=member.guild)
            await voice_client.disconnect()


@client.command()
async def start_playlist(ctx):
    global playlist_tracks
    playlist_tracks = []

    playlist = spotify.playlist_tracks(playlist_uri)
    for item in playlist['items']:
        track_uri = item['track']['uri']
        playlist_tracks.append(track_uri)

    await ctx.send("Playlist started!")


client.run('YOUR_DISCORD_BOT_TOKEN')
