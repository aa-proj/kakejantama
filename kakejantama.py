# discord ライブラリをインポート
import discord
from discord.app_commands import Choice

# requestライブラリをインポート
import requests
import typing
import enum

# インテント(discordに何の情報が欲しいのかログインの時に伝える変数)
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

# Discordクライアントを準備 インテントを引数に渡してる
client = discord.Client(intents=intents)


# コマンドツリーをログイン後に取得してる
tree = discord.app_commands.CommandTree(client)

# ギルド変数(鯖IDを変数に入れておく)
guild_target = discord.Object(id=606109479003750440)




#コマンドで順位ごとに点棒を入力
@tree.command(name='jantama', description='麻雀のポイントを計算', guild=guild_target)
async def jantama(interaction: discord.Interaction, no1:int, no2:int, no3:int, no4:int = None):
    #1位がもらえるポイント
    No1Points = (no1 - 25000) / 100
    #2位がもらえるポイント
    No2Points = (no2 - 25000) / 100 
    #3位がもらえるポイント
    No3Points = (no3 - 25000) / 100 
    #4位がもらえるポイント
    No4Points = (no4 - 25000) / 100 

    if no4 is None:
        if not no1 + no2 + no3 == 35000*3:
            await interaction.response.send_message(f"たぶん点数がおかしいにゃ!")
            return
        if not no1 >= no2 >= no3:
            await interaction.response.send_message(f"点数と順位が一致しないにゃ!")
            return
        if no2 < 35000:
            await interaction.response.send_message(f"【1位{no1}点,2位{no2}点,3位{no3}点】\n3位の人は{-No3Points}P、2位の人は{-No2Points}Pを1位に支払うにゃ!")
            return
        else:
            await interaction.response.send_message(f"【1位{no1}点,2位{no2}点,3位{no3}点】\n3位の人は、2位の人に{No2Points}P、1位の人に{No1Points}P支払うにゃ!")
            return

    
    if not no1 + no2 + no3 + no4 == 25000*4:
        await interaction.response.send_message(f"たぶん点数がおかしいにゃ!")
        return
    if no1 < 25000:
        await interaction.response.send_message(f"1位の点数が25000点未満にゃ!")
        return
    if no4 > 25000:
        await interaction.response.send_message(f"4位の点数が25000点より多いにゃ!")
        return
    if not no1 >= no2 >= no3 >= no4:
        await interaction.response.send_message(f"点数と順位が一致しないにゃ!")
        return
    if No3Points >= 0: #3位がプラスの時は4位が全員に支払う
        await interaction.response.send_message(f"【1位{no1}点,2位{no2}点,3位{no3}点,4位{no4}点】\n4位の人は1位に{No1Points}P、2位に{No2Points}P、3位に{No3Points}Pを支払うにゃ!")
        return
    if No2Points < 0: #2位がマイナスの時は1位が総取り
        await interaction.response.send_message(f"【1位{no1}点,2位{no2}点,3位{no3}点,4位{no4}点】\n4位の人は{-No4Points}P、3位の人は{-No3Points}P、2位の人は{-No2Points}Pを1位に支払うにゃ!")
        return
    if No2Points >= 0 and No3Points <0: #1，2位がプラスで3，4位がマイナス
        if No1Points <= -No4Points: #4位のマイナスが1位のプラスより大きい時
            await interaction.response.send_message(f"【1位{no1}点,2位{no2}点,3位{no3}点,4位{no4}点】\n4位の人は1位に{No1Points}P、2位に{-No4Points - No1Points}P、3位の人は2位に{-No3Points}Pを支払うにゃ!")
            return
        if No1Points > -No4Points: #4位のマイナスが1位のプラスより小さい時
            await interaction.response.send_message(f"【1位{no1}点,2位{no2}点,3位{no3}点,4位{no4}点】\n4位の人は1位に{-No4Points}P、3位の人は1位に{No1Points + No4Points}P、2位に{No2Points}Pを支払うにゃ!")
            return



    print(No1Points,No2Points,No3Points,No4Points)

# ライブラリにイベントを登録 "on_ready"
# readyの時にDiscord側から実行される
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    # コマンドツリーをシンク(同期する)
    await tree.sync(guild=guild_target)

# DiscordにTokenでログインする
client.run('Token')