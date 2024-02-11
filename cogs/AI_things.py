import base64
import io
import random
import time

import discord
from discord.ext import commands
from discord import Option

import AIIO
import Data
import utils


class AI_things(commands.Cog):
    ''' AI_things | BOT COG'''
    name = "AI_things"
    author = ""

    def __init__(self, bot):
        self.bot = bot

    # AI_cooldown = commands.CooldownMapping.from_cooldown(1, 30, commands.BucketType.user)
    @commands.cooldown(1, 30, commands.BucketType.member)
    @commands.command(aliases=["ИИ", "гигачат", "gigachat"])
    async def askGigachat(self, ctx, *, prompt: str = "Привет!"):
        bannedIDs = []
        if ctx.author.id in bannedIDs:
            await ctx.reply("Вам запрещено использовать эту команду!")
            return
        async with ctx.typing():
            payload = [{"role": "system", "content": "Не выдавай одни и те же фразы много раз подряд."},
                       # Если в ответе ты начинаешь повторять одно и то же, перкрати ответ.
                       {"role": "user", "content": prompt}]
            # print(payload)
            response = await AIIO.askLLM(payload, AIIO.LLMs.GIGACHAT, 3, AIIO.gigachat_temptoken)
            print(response)
            if response == "No token":
                response = await AIIO.askLLM(payload, AIIO.LLMs.GIGACHAT, 3, AIIO.gigachat_temptoken)
                print(response)

            resp = response[0]
            tokens = response[1]['total_tokens']
            tokenInfo = "\n" + f"||Использовано {tokens} токен(ов/а)||"
            output = resp + tokenInfo
            # embed = discord.Embed(title="Информация о генерации",description=f"",colour=Data.getEmbedColor(Data.EmbedColor.Neutral))
            outputs = utils.split_string(output, 2000, len(tokenInfo))
            for content in outputs:
                await ctx.reply(content)

    # @commands.cooldown(1, 35, commands.BucketType.member)
    # @commands.command(aliases=["атк", "аткгпт", "atk", "ATK", "АТК", "atkgpt"])
    async def askATKGPT(self, ctx, *, prompt: str = "Привет!"):
        bannedIDs = []
        if ctx.author.id in bannedIDs:
            await ctx.reply("Вам запрещено использовать эту команду!")
            return
        async with ctx.typing():
            payload = [
                {"role": "system",
                 "content": "Ты ATK GPT. Искуственный интеллект, задача которого - помогать людям.\nЕсли в ответе ты начинаешь повторять одно и то же, перкрати ответ."},
                {"role": "user", "content": prompt}]
            # print(payload)
            response = await AIIO.askLLM(payload, AIIO.LLMs.GIGACHAT, 3, AIIO.gigachat_temptoken)
            print(response)
            if response == "No token":
                response = await AIIO.askLLM(payload, AIIO.LLMs.GIGACHAT, 3, AIIO.gigachat_temptoken)
                print(response)

            resp = response[0]
            tokens = response[1]['total_tokens']
            tokenInfo = "\n" + f"||Использовано {tokens} токен(ов/а)||"
            output = resp + tokenInfo
            # embed = discord.Embed(title="Информация о генерации",description=f"",colour=Data.getEmbedColor(Data.EmbedColor.Neutral))
            outputs = utils.split_string(output, 2000, len(tokenInfo))
            for content in outputs:
                await ctx.reply(content)

    @commands.cooldown(1, 15, commands.BucketType.member)
    @commands.command(aliases=["кандинский"])
    async def kandinsky(self, ctx, *, prompt: str):
        time_start = time.time()
        async with ctx.typing():





            embed = discord.Embed(title="Запуск генерации...",
                                  description=f"**Запрос:** {prompt}\n\n***Генерация может занять немного времени...***",
                                  colour=Data.getEmbedColor(Data.EmbedColor.Neutral))
            embed.add_field(name="Запросил генерацию", value=f"<@{ctx.author.id}>", inline=False)
            # embed.add_field(name="Подсказка",value="Используйте !: что бы начать вводить негативный промпт (делайте это после обычного)",inline=False)
            await ctx.reply(embed=embed)




            gen = await AIIO.askT2I(prompt, AIIO.Text2Imgs.KANDINSKY)
            if gen['censored']:
                embed = discord.Embed(title="Ошибка генерации!",
                                      description="NSFW изображения не разрешены этой моделью!",
                                      colour=Data.getEmbedColor(Data.EmbedColor.Error))
                await ctx.reply(embed=embed)
            else:
                if gen["image"] == "Error":
                    embed = discord.Embed(title="Ошибка генерации!",
                                          description="Время ожидания истекло!",
                                          colour=Data.getEmbedColor(Data.EmbedColor.Error))
                    await ctx.reply(embed=embed)
                    return
                file_content = io.BytesIO(base64.b64decode(gen["image"]))

                file = discord.File(filename=f"gen_kandinsky_{random.randint(0, 35565)}.png", fp=file_content)
                embed = discord.Embed(title="Генерация завершена!", description=f"**Запрос:** {prompt}",
                                      colour=Data.getEmbedColor(Data.EmbedColor.Success))
                embed.add_field(name="Запросил генерацию", value=f"<@{ctx.author.id}>", inline=False)
                embed.add_field(name="Время генерации", value=f"{round(time.time() - time_start, 2)} сек.",
                                inline=False)

                await ctx.reply(embed=embed)
                await ctx.reply(file=file)


def setup(bot):
    bot.add_cog(AI_things(bot))
