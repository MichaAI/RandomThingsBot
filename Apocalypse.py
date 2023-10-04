import json
import random
# import random
import sqlite3

# import numpy as np
# import matplotlib.pyplot as plt
import discord
from discord.ext import commands
# import perlin_noise
from discord import Option
from random import *

import utils


class Apocalypse(commands.Cog):
    currentDLC="Самый странный апокалипсис⁶™"
    def __init__(self, bot):
        self.bot = bot
        self.items = sqlite3.connect("ApocalypseData/ApocalypseItems.db")
        self.itemsCursor = self.items.cursor()
    @commands.slash_command(name="создать-список",description="Создаёт список предметов и заданий.")
    async def getList(self, ctx):
        # Выполнение запроса на выборку 10 случайных значений столбца ItemNameRu из таблицы items
        self.itemsCursor.execute("SELECT ItemNameRu FROM items ORDER BY RANDOM() LIMIT 10")
        # Получение результатов запроса
        results = self.itemsCursor.fetchall()
        # Вывод 10 случайных значений
        result_ds = ""
        for result in results:
            print(result[0])
            result_ds+="1. "+ result[0]+"\n"
        print("Выбор таска")
        with open('ApocalypseData/MainApocalypseData.json', encoding="utf-8") as f:
            ap_values = json.load(f)
        print(ap_values)
        taskTypes = ap_values["taskTypes"]
        task = choice(taskTypes)
        extras = ap_values["extraTasks"]
        ex_tasks_out=""
        ex_tasks = choices(extras, k=randint(0, 3))
        for i in ex_tasks:
            ex_tasks_out+="- "+i
        await ctx.respond("Отправка...",ephemeral=True)
        guide = f"\n\nЭто список предметов для игры {self.currentDLC}. \n" \
                f"Правила игры - У Вас есть список предметов. Можно гипертрофировать их смысл, использовать мемный или прямой смысл. " \
                f"\nПо умолчанию Вы не можете использовать предметы не из списка. Обычно цель - уничтожить планету/мир/человечество, однако могут быть другие типы заданий.\n" \
                f"Так же есть дополнительные эффекты, изменяющие правила игры.\n" \
                f"# ИГРА ЕЩЁ В РАЗРАБОТКЕ! \n### В планах сделать автоотправку и ИИ ответы автоматические."
        await utils.sendMessageWithhook(ctx, f"# Список слов:\n{result_ds}\n"
                          f"# Условие: \n{task}\n"
                          f"# Дополнительные условия:\n{ex_tasks_out}"
                                             f"\n{guide}", "", None)

        # await ctx.respond(f"# Список слов:\n{result_ds}\n"
        #                   f"# Условие: \n{task}\n"
        #                   f"# Дополнительные условия:\n{ex_tasks_out}")

