from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import re

USERNAME = ""
PASSWORD = ""


class LoginInginious:

    def __init__(self, driver_path, option):
        self.driver = webdriver.Chrome(executable_path=driver_path, options=option)
        self.information_stundent = {}


    def login(self):
        "Se encarga de iniciar sesión en la plataforma INGInious M-IDEA."
        try:
            with open("data_students.json") as data_students:
                self.information_stundent = json.load(data_students)
        except:
            self.driver.get("http://ingini.ddns.net/signin")
            username = self.driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/form/div[1]/input')
            username.send_keys(USERNAME)
            password = self.driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/form/div[2]/input')
            password.send_keys(PASSWORD)
            password.send_keys(Keys.ENTER)
            self.copy_stundets()
        self.driver.close()


    def copy_stundets(self):
            "Hace una copia de los nombres, correos e intentos de los estundiantes."
            time.sleep(3)
            course = self.driver.find_element_by_xpath('//*[@id="content"]/div[1]/a[1]/div[2]')
            course.click()
            self.driver.find_element_by_xpath('//*[@id="tasks-list"]/a[1]/div[1]').click()
            self.driver.find_element_by_xpath('//*[@id="sidebar_inner"]/div[2]/a[1]').click()
            students = self.driver.find_elements_by_class_name('success')
            self.save_information(students)
        

    def save_information(self, students):
        "Guarda los nombres y correos de los estudiantes antes copiados."

        for student in students:
            data = str(student.text)

            pattern="""
                (?P<name>[\w\s]*)
                (\( )
                (?P<email>[\w\.\-]*)
                (.*)
            """

            for item in re.finditer(pattern,data,re.VERBOSE):
                item = item.groupdict()
                self.information_stundent[item["email"]] = item["name"]

        with open("data_students.json", "w") as data_students:
            json.dump(self.information_stundent, data_students, indent=4)