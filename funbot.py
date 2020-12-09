import discord
import asyncio
import os
from dotenv import load_dotenv
import ranstr
import requests
import datetime
import random
import json
from sid import gt32
from sid import gt64
from discord.ext import commands
from discord.ext.commands import has_permissions

load_dotenv()

Token = os.getenv('token')
TRN_Key = os.getenv('TRN_key')
stkey = os.getenv('Steam_Key')
gifkey = os.getenv('gif_api')
cov_key = os.getenv('covid_api')

kommand = commands.Bot(command_prefix="!!")
client = discord.Client()

ver = "v1.0"

@kommand.event
async def on_ready():
    await kommand.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(ver))
    print("Bot ready")


@kommand.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(file=discord.File('permission_denied.png'))


@kommand.command()
async def hello(ctx, *arg):
    if len(arg) == 0:
            await ctx.send("Hello " + ctx.message.author.name + "!!!")
    for i in arg:
        await ctx.send('Hello ' + i + ' !!')


@kommand.command(aliases=['pong'])
async def ping(ctx):
    await ctx.send(f'Ping : {round(kommand.latency * 1000)}ms (Wrong)')


@kommand.command()
async def kill(ctx, *args):
    if len(args) == 0:
        await ctx.send("You have killed youself, dumbass.")
    for i in args:
        await ctx.send(i + " is slain and the princess is safe.")


@kommand.command()
async def pat(ctx, *arg):
    if len(arg) == 0:
            await ctx.send("Pat Pat Pat !! " + ctx.message.author.name + " has been patted very well and now, is happy")
    for i in arg:
        if i == 'me':
            await ctx.send("Pat Pat Pat !!! You have been patted very well and now, is happy")
        else:
            await ctx.send("Pat Pat Pat !!! " + i + " has been patted very well and now, is happy")


@kommand.command()
@has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick()
    await ctx.send(f"```Kicked : {member}\nReason : {reason}```")


@kommand.command()
@has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"```Banned : {member}\nReason : {reason}```")


@kommand.command()
@has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'`Unbanned :{user.name}#{user.discriminator}`')
            return


@kommand.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)


@kommand.command()
async def stats(ctx, game, accid):
    ctx.send('`Use your custom url name for CSGO`')
    if game == 'dota2':
        s32 = gt32(accid)
        pid = requests.get('https://api.opendota.com/api/players/' + str(s32))
        mid = requests.get('https://api.opendota.com/api/players/{0}/matches'.format(s32))
        y = pid.json()
        m = mid.json()
        lbr = y["leaderboard_rank"]
        mmr = y["mmr_estimate"]["estimate"]
        cr = y["competitive_rank"]
        name = y["profile"]["personaname"]
        rt = y["rank_tier"]
        scr = y["solo_competitive_rank"]
        await ctx.send(
            "```Ingame Name : {0}\nLeaderboard : {1}\nMMR Estimate : {2}\nCompetitve Rank : {3}\nRank Tier : {4}\nSolo Competitve Rank : {5}```".format(
                name, lbr, mmr, cr, rt, scr))
        await ctx.send("```Do you want to check 5 previous match status(choose wihtin 10 seconds)[y/n] ?\n```")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['y', 'n']

        try:
            mesg = await kommand.wait_for("message", check=check, timeout=10)
        except asyncio.TimeoutError:
            await ctx.send(":confused: You didn't chose anything")
        if mesg.content == 'y':
            await ctx.send("Match details coming right up!!:partying_face:")
            for i in range(5):
                mi = m[i]['match_id']
                tm = datetime.datetime.fromtimestamp(m[i]['start_time']).strftime('%H:%M:%S')
                dt = datetime.datetime.fromtimestamp(m[i]['start_time']).strftime('%d-%m-%Y')
                k = m[i]['kills']
                d = m[i]['deaths']
                a = m[i]['assists']
                kd = round(((k + a) / d), 2)
                du = m[i]['duration']
                du = round((du / 60), 2)
                await ctx.send(
                    "```Time : {0}\nDate : {1}\nMatch ID : {2}\nKills : {3}\nDeaths : {4}\nAssists : {5}\nK/D : {6}\nDuration : {7} minutes```".format(
                        tm, dt, mi, k, d, a, kd, du))
        else:
            if mesg.content == 'n':
                await ctx.send("Okayyyyyy!! :thumbsup:")
            else:
                await ctx.send("Choose 'y' or 'n', what's so hard about it ?:man_shrugging:")

    elif game == 'r6s':
        await ctx.send("This feature is temporarily taken down , hope it restores soon :')")
        '''sta = 0
        def check(m):
            return ... and m.channel == ctx.channel
        await ctx.send("Do you the stats in DM(y/n)?")
        try:
            msg = await kommand.wait_for('message', check=check,  timeout=10)
            if msg.content in ['Y', 'y']:
                sta = 1
                await ctx.send("`Stats coming up in DM, boi or gal`")
            elif msg.content in ['N', 'n']:
                sta = 0
                await ctx.send("`Stats coming up in this Channel, boi or gal`")
        except asyncio.TimeoutError as e:
            sta = 0
            await ctx.send("`You here , Snail ? Get embarrassed in front of everyone !!`:smiling_imp:")

        pd = requests.get('https://r6.apitab.com/search/uplay/' + accid, headers={'apiKey' : "aadacasd"})
        print(pd)
        y = pd.json()
        print(y)
        pid = str(next(iter(y['players'])))
        det = requests.get('https://r6.apitab.com/player/' + pid)
        det = det.json()
        s = 'stats'
        lvl = det[s]['level']
        cskl = det[s]['casualpvp_kills']
        urkl = det[s]['unrankedpvp_kills']
        rkl = det[s]['rankedpvp_kills']
        total_kills = cskl + urkl + rkl
        csd = det[s]['casualpvp_death']
        urd = det[s]['unrankedpvp_death']
        rd = det[s]['rankedpvp_death']
        td = csd + urd + rd
        cskd = det[s]['casualpvp_kd']
        cswl = det[s]['casualpvp_wl']
        cshp = det[s]['casualpvp_hoursplayed']
        rkd = det[s]['rankedpvp_kd']
        rwl = det[s]['rankedpvp_wl']
        rhp = det[s]['rankedpvp_hoursplayed']
        gkd = det[s]['generalpvp_kd']
        gwl = det[s]['generalpvp_wl']
        ghp = det[s]['generalpvp_hoursplayed']
        hsp = det[s]['generalpve_hsrate']
        gmk = det[s]['generalpvp_meleekills']
        gpk = det[s]['generalpvp_penetrationkills']
        mao = det["op_main"]["attacker"]
        mdo = det["op_main"]["defender"]
        maow = det['operators'][mao]['overall']['wins']
        maok = det['operators'][mao]['overall']['kills']
        maod = det['operators'][mao]['overall']['deaths']
        maokd = det['operators'][mao]['overall']['kd']
        maotp = det['operators'][mao]['overall']['timeplayed']
        maotp = maotp / 3600
        maotp = round(maotp, 2)
        maowr = det['operators'][mao]['overall']['winrate']
        mmr = det['ranked']['mmr']
        mmrname = det['ranked']['rankname']
        maxname = det['ranked']['maxrankname']
        mdow = det['operators'][mdo]['overall']['wins']
        mdok = det['operators'][mdo]['overall']['kills']
        mdod = det['operators'][mdo]['overall']['deaths']
        mdokd = det['operators'][mdo]['overall']['kd']
        mdotp = det['operators'][mdo]['overall']['timeplayed']
        mdotp = mdotp / 3600
        propic = f'https://ubisoft-avatars.akamaized.net/{pid}/default_256_256.png'
        mdotp = round(mdotp, 2)
        mdowr = det['operators'][mdo]['overall']['winrate']
        maodet = f"Details: https://www.ubisoft.com/en-gb/game/rainbow-six/siege/game-info/operators/{mao}"
        mdodet = f"Details: https://www.ubisoft.com/en-gb/game/rainbow-six/siege/game-info/operators/{mdo}"
        if sta == 0:
            await ctx.send(propic)
            await ctx.send(f"**{accid}**")
            await ctx.send("***GENERAL :***")
            await ctx.send(
            f"```Level               : {lvl}\nGeneral K/D         : {gkd}\nGeneral W/L         : {gwl}\nTotal Kills         : {total_kills}\nTotal Deaths        : {td}\nHeadshot Percentage : {hsp} \nMelee Kills         : {gmk}\nPenetration Kills   : {gpk}\nHours Played        : {ghp} hours```")
            await ctx.send("***CASUAL :***")
            await ctx.send(
            f"```K/D          : {cskd}\nW/L          : {cswl}\nKills        : {cskl}\nDeaths       : {csd}\nHours Played : {cshp} hours```")
            await ctx.send("***RANKED :***")
            await ctx.send(
            f"```MMR          : {mmr}\nRank         : {mmrname}\nMax Rank     : {maxname}\nK/D          : {rkd}\nW/L          : {rwl}\nKills        : {rkl}\nDeaths       : {rd}\nHours Played : {rhp} hours```")
            await ctx.send("***Main Attacker :***")
            await ctx.send(file=discord.File(f'icons/{mao.lower()}.png'))
            await ctx.send(f"       **{mao}**")
            await ctx.send(
            f'```Wins        : {maow}\nKills       : {maok}\nDeaths      : {maod}\nK/D         : {maokd}\nTime Played : {maotp} hours\nWinrate     : {maowr} %\n```')
            await ctx.send(maodet)
            await ctx.send("***Main Defender :***")
            await ctx.send(file=discord.File(f'icons/{mdo.lower()}.png'))
            await ctx.send(f"       **{mdo}**")
            await ctx.send(
            f'```Wins        : {mdow}\nKills       : {mdok}\nDeaths      : {mdod}\nK/D         : {mdokd}\nTime Played : {mdotp} hours\nWinrate     : {mdowr} %\n```')
            await ctx.send(mdodet)

            await ctx.send(f"For more details :\n ")
            await ctx.send(f"https://r6.tracker.network/profile/pc/{accid}")
        elif sta == 1:
            await ctx.author.send(propic)
            await ctx.author.send(f"**{accid}**")
            await ctx.author.send("***GENERAL :***")
            await ctx.author.send(
                f"```Level               : {lvl}\nGeneral K/D         : {gkd}\nGeneral W/L         : {gwl}\nTotal Kills         : {total_kills}\nTotal Deaths        : {td}\nHeadshot Percentage : {hsp} \nMelee Kills         : {gmk}\nPenetration Kills   : {gpk}\nHours Played        : {ghp} hours```")
            await ctx.author.send("***CASUAL :***")
            await ctx.author.send(
                f"```K/D          : {cskd}\nW/L          : {cswl}\nKills        : {cskl}\nDeaths       : {csd}\nHours Played : {cshp} hours```")
            await ctx.author.send("***RANKED :***")
            await ctx.author.send(
                f"```MMR          : {mmr}\nRank         : {mmrname}\nMax Rank     : {maxname}\nK/D          : {rkd}\nW/L          : {rwl}\nKills        : {rkl}\nDeaths       : {rd}\nHours Played : {rhp} hours```")
            await ctx.author.send("***Main Attacker :***")
            await ctx.author.send(file=discord.File(f'icons/{mao.lower()}.png'))
            await ctx.author.send(f"       **{mao}**")
            await ctx.author.send(
                f'```Wins        : {maow}\nKills       : {maok}\nDeaths      : {maod}\nK/D         : {maokd}\nTime Played : {maotp} hours\nWinrate     : {maowr} %\n```')
            await ctx.author.send(maodet)
            await ctx.author.send("***Main Defender :***")
            await ctx.author.send(file=discord.File(f'icons/{mdo.lower()}.png'))
            await ctx.author.send(f"       **{mdo}**")
            await ctx.author.send(
                f'```Wins        : {mdow}\nKills       : {mdok}\nDeaths      : {mdod}\nK/D         : {mdokd}\nTime Played : {mdotp} hours\nWinrate     : {mdowr} %\n```')
            await ctx.author.send(mdodet)

            await ctx.author.send(f"For more details :\n ")
            await ctx.author.send(f"https://r6.tracker.network/profile/pc/{accid}")
            '''
    elif game == 'csgo':
        s64 = gt64(accid)
        pd = requests.get(
            f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={stkey}&steamid={s64}")
        print(pd)
        y = pd.json()
        tk = y['playerstats']['stats'][0]['value']
        td = y['playerstats']['stats'][1]['value']
        thp = y['playerstats']['stats'][2]['value']
        kd = round(tk / td, 2)
        thp = round(thp / 3600, 2)
        hs = 1
        tsh = 1
        tsf = 1
        lim = len(y['playerstats']['stats'])
        for i in range(lim):
            if y['playerstats']['stats'][i]['name'] == 'total_kills_headshot':
                hs = y['playerstats']['stats'][i]['value']
                break
        for i in range(lim):
            if y['playerstats']['stats'][i]['name'] == 'total_shots_hit':
                tsh = y['playerstats']['stats'][i]['value']
                break
        for i in range(lim):
            if y['playerstats']['stats'][i]['name'] == 'total_shots_fired':
                tsf = y['playerstats']['stats'][i]['value']
                break
        acc = round((tsh / tsf * 100), 2)
        hsp = round((hs / tsh * 100), 2)
        await ctx.send(
            f'```Name                : {accid}\nTotal Kills         : {tk}\nTotal Deaths        : {td}\nK/D                 : {kd}\nTotal Hours Played  : {thp} hours\nHeadshot Percentage : {hsp}%\nAccuracy Percentage : {acc}%\n```')
    elif game == 'fort':
        pd = requests.get(f"https://api.fortnitetracker.com/v1/profile/kbm/{accid}",
                          headers={"TRN-Api-Key":TRN_Key})
        pd = pd.json()
        t5 = pd['lifeTimeStats'][0]['value']
        t3 = pd['lifeTimeStats'][1]['value']
        t6 = pd['lifeTimeStats'][2]['value']
        t10 = pd['lifeTimeStats'][3]['value']
        t12 = pd['lifeTimeStats'][4]['value']
        t25 = pd['lifeTimeStats'][5]['value']
        tscore = pd['lifeTimeStats'][6]['value']
        tmp = pd['lifeTimeStats'][7]['value']
        tw = pd['lifeTimeStats'][8]['value']
        twp = pd['lifeTimeStats'][9]['value']
        tk = pd['lifeTimeStats'][10]['value']
        tkd = pd['lifeTimeStats'][11]['value']
        await ctx.send(pd['avatar'])
        await ctx.send(f"**{accid}**")
        await ctx.send(
            f"```Kills                : {tk}\nK/D                  : {tkd}\nTotal Score          : {tscore}\nTotal Matches Played : {tmp}\nTotal Wins           : {tw}\nWin Percentage       : {twp}\nTop 3s               : {t3}\nTop 5s               : {t5}\nTop 6s               : {t6}\nTop 10s              : {t10}\nTop 12s              : {t12}\nTop 25s              : {t25}```")

    else:
        await ctx.send(
            "Enter an available game:\nDOTA 2 - dota2\nRainbow Six Siege - r6s\nCSGO - csgo\nFortnite - fort\nExample : !!stats dota2 name\nNote: Enter your custom url name for csgo")


@kommand.command(aliases=['corona'])
async def covid(ctx):
    def check(m):
        return ... and m.channel == ctx.channel

    await ctx.send("Enter the Country Name\n")
    try:
        msg = await kommand.wait_for('message', check=check, timeout=10)
        country = msg.content

        url = "https://covid-19-data.p.rapidapi.com/country"

        querystring = {"format": "json", "name": country}

        headers = {
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
            'x-rapidapi-key': cov_key
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = response.json()
        name = response[0]['country']
        conf = response[0]['confirmed']
        recv = response[0]['recovered']
        crtc = response[0]['critical']
        dead = response[0]['deaths']
        fatr = dead / (conf + recv + crtc) * 100
        fatr = round(fatr, 2)
        await ctx.send(
            f"```Country         : {name}\nConfirmed cases : {conf}\nRecovered Cases : {recv}\nCritical Cases  : {crtc}\nDeaths          : {dead}\nFatality Rate   : {fatr} %```")

    except asyncio.TimeoutError as e:
        print(e)
        await ctx.send("You have taken too long to respond")


@kommand.command()
async def gif(ctx, *search):
    lmt = 6
    r = requests.get("https://api.tenor.com/v1/search?key=%s&q=%s&limit=%s" % (gifkey, search, lmt))

    if r.status_code == 200:
        picker = random.randint(0, lmt-1)
        res = json.loads(r.content)['results']
        await ctx.send(res[picker]['url'])
        print(res)


@kommand.command()
async def randoms(ctx):
    await ctx.send("Choose from the following :")
    await ctx.send("url, email, word, sentence, paragraph")
    def check(m):
        return ... and m.channel == ctx.channel
    try:
        msg = await kommand.wait_for('message', check=check, timeout=10)
        msg = msg.content.lower()
        await ctx.send(msg+" = "+ranstr.generate(msg))
    except asyncio.TimeoutError as e:
        print(e)
        await ctx.send("Oopsie!! You too slow.\nBe faster next time")

@kommand.command()
async def about(ctx):
    await ctx.send("`Created by W.A.R#4670`\n`Special thanks to Terisa Chan and\n periya_pussy_ponpensiero`")
    await ctx.send(f"`Version : {ver}`")


kommand.run(Token)
