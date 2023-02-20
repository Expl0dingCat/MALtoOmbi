"""
Automatically request new anime from MAL to Ombi (to eventually be downloaded onto Plex)

Made by Expl0dingCat

This was originally made for just me and my friend to use which is why its so thrown together.
I might re-write it some day to make it more user friendly, modular, add the ability to request directly to radarr/sonarr, support more anime lists like anilist, and more.

No promises though.




Not even sure if this still works, I haven't used it in a while lol
"""

import time
import pyombi
import re
import asyncio
import discord
from discord import Webhook, Embed, RequestsWebhookAdapter 
from jikanpy import Jikan

webhook_url = ""
ombi_url = ""

def sendwebhook(title, desc, foot, img="", color=0xD29708):
    webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())
    embed=discord.Embed(title=title, description=desc, color=color)
    embed.set_image(url=img)
    embed.set_footer(text=foot, icon_url="https://raw.githubusercontent.com/Ombi-app/Ombi/gh-pages/img/android-chrome-512x512.png")
    webhook.send(embed=embed)


def ombirequest(type, name):
    ombi = pyombi.Ombi( # Ombi Account info
        ssl=False,
        host=ombi_url,
        port="",
        urlbase="",
        username="",
        password="",
        api_key=""
    )

    ombi.authenticate()

    try:
        ombi.test_connection()
    except pyombi.OmbiError as e:
        print(e)
        return

    if type == "TV":
        name2 = re.sub(r"[^a-zA-Z0-9 ]", " ", name)
        tv_search = ombi.search_tv(name2)
        try:
            Title = tv_search[0]['title'] 
            Description = tv_search[0]['overview']
            IdentificationNum = tv_search[0]['id']
            ImageURL = tv_search[0]['banner']
            # Runtime = tv_search[0]['runtime']
            ombi.request_tv(IdentificationNum)
            print("Downloading: " + Title)
            sendwebhook(Title, Description, "Download started", ImageURL)
        except pyombi.OmbiError as e:
            pass
            print("Already have: " + Title)
            sendwebhook(f"We already have `{Title}`", "You can stream it on on Plex", "Request ignored", ImageURL)
        except Exception as e:
            pass
            print(e)
            sendwebhook(f"Something went wrong when trying to get information for `{name2}`", f"The Ombi API cannot find the details of this show, check if its on Plex, if it isnt you can manually request it at {ombi_url}", "Manual download may be required", "", 0xFF0000)
            
        
    elif type == "Movie":
        name2 = re.sub(r"[^a-zA-Z0-9 ]", " ", name)
        movie_search = ombi.search_movie(name2)
        try:
            Title = movie_search[0]['title'] 
            Description = movie_search[0]['overview']
            IdentificationNum = movie_search[0]['id']
            ombi.request_movie(IdentificationNum)
            print("Downloading: " + Title)
            sendwebhook(Title, Description, "Download started", "", 0x2E51A2)
        except pyombi.OmbiError as e:
            pass
            print("Already have: " + Title)
            sendwebhook(f"We already have `{Title}`", "You can stream it on on Plex", "Request ignored", "", 0x2E51A2)
        except Exception as e:
            pass
            print(e)
            sendwebhook(f"Something went wrong when trying to get information for `{name2}`", f"The Ombi API cannot find the details of this movie, check if its on Plex, if it isnt you can manually request it at {ombi_url}", "Manual download may be required", "", 0xFF0000)
            

def getlist():
    jikan = Jikan()

    try: 
        user1 = jikan.user(
            username='user1',
            request='animelist',
            argument='ptw',
        )
        print("Fetched User1")

        time.sleep(1)
        user2 = jikan.user(
            username='user2',
            request='animelist',
            argument='ptw',
        )
        print("Fetched User2")

    # Users can be added and removed, just follow the same format.

    except:
        getlist()
        
    elist = []
    jlist = []

    amt = len(user1['anime'])
    for i in range(amt):
        elist.append(user1['anime'][i]['title'] + "|" + user1['anime'][i]['type'])
    amt = len(user2['anime'])
    for i in range(amt):
        jlist.append(user2['anime'][i]['title'] + "|" + user2['anime'][i]['type'])

    for i in jlist:
        elist.append(i)

    listfull = []
    for item in elist:
        if item not in listfull:
            listfull.append(item)
    
    sendwebhook("The script has been executed.", "Now checking for new items...", "MALtoOmbi", "", 0x000000)

    for i in listfull:
        name, type = i.split('|', 1)
        print(str(name) + "|" + str(type))
        ombirequest(str(type), str(name))



getlist()






