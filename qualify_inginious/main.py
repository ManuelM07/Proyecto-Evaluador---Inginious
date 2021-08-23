import os
import pandas as pd
from selenium import webdriver
from qualify import Qualify
from login_inginious import LoginInginious

NOMBRE_CP = "submissions"
BRAVE_PATH = ""
option = webdriver.ChromeOptions()
option.binary_location = BRAVE_PATH

CHROME_DRIVER_PATH = ""

bot = LoginInginious(CHROME_DRIVER_PATH, option)
bot.login()
name_stundents = bot.information_stundent

qualify = Qualify(name_stundents, NOMBRE_CP)

carpeta_ejercicios = os.listdir(NOMBRE_CP)
dict_ejercicio = {}

for ejercicio in carpeta_ejercicios:
    try:
        dict_ejercicio.update({ejercicio: os.listdir(f"{NOMBRE_CP}/{ejercicio}")})
    except NotADirectoryError:
        pass

dict_notas = {}
for (ejercicio, estudiantes) in sorted(dict_ejercicio.items()):
    dict_notas[ejercicio] = qualify.update_dict(estudiantes, ejercicio)

df = pd.DataFrame(dict_notas)
df = df.fillna(0.0)
df.to_excel("notas.xlsx", sheet_name="Practica 6")    