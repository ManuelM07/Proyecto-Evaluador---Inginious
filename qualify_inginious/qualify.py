import json
import pyparsing
import re
import os

RESTRICTIONS = ["while", "for"]


class Qualify:

    def __init__(self, name_stundents, nombre_cp) -> None:
        self.name_stundents = name_stundents
        self.nombre_cp = nombre_cp
        

    def update_dict(self, estudiantes, ejercicio):
        """Esta función se encarga de calificar a cada uno de los estudiantes
            y retorna un diccionario con las notas de los estudiantes, si un estudiante
            tiene -1 significa una alerta de trampa."""
        self.dict_nota_estudiante = {}

        for (_, name) in self.name_stundents.items():
            self.dict_nota_estudiante[name] = None

        for estudiante in estudiantes:
            try:
                carpeta_estudiante = os.listdir(f"{self.nombre_cp}/{ejercicio}/{estudiante}")[0]
                with open(f"{self.nombre_cp}/{ejercicio}/{estudiante}/{carpeta_estudiante}/submission.test") as file:
                    data = str(file.readlines())
                    
                    try:
                        comment = pyparsing.nestedExpr("/*", "*/").suppress()
                        text_i = pyparsing.nestedExpr("_id", "|").suppress()
                        text_f = pyparsing.nestedExpr(f"{ejercicio}/input", f"{estudiante}").suppress()

                        data = comment.transformString(data)
                        data = text_i.transformString(data)
                        data = text_f.transformString(data)

                        ignore_comment = r"(//.*)"
                        myex = re.compile(ignore_comment)
                        data = re.sub(myex, "",data)
                    except:
                        print(f"{carpeta_estudiante} - {ejercicio} - {estudiante}")
                        break
                                        
                values = [x for x in RESTRICTIONS if x in data]
                if len(values):
                    self.dict_nota_estudiante[self.name_stundents[estudiante]] = -1.0
                else:
                    try:
                        with open(f"{self.nombre_cp}/{ejercicio}/{estudiante}/{carpeta_estudiante}/archive/__feedback.json") as file:
                            data = json.load(file)
                            if int(data["grade"]) == 100:
                                self.dict_nota_estudiante[self.name_stundents[estudiante]] = 5.0
                            else:
                                self.dict_nota_estudiante[self.name_stundents[estudiante]] = 1.0
                    except:
                        pass
            except NotADirectoryError:
                pass
        return self.dict_nota_estudiante