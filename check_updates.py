import subprocess
import os
from time import sleep
from generar_plots import generar_todos_los_plots
from parameters import INFO_DATOS, PATH_COVID


class CheckData:
    def __init__(self, ruta_covid, INFO_DATOS):
        self.ruta_covid = ruta_covid
        self.info_datos = INFO_DATOS
    
    def check_nueva_data(self):
        # Fetch to check new data
        subprocess.run(f"git -C {self.ruta_covid} fetch",shell=True) # fetch changes
        output = subprocess.run(f"git -C {self.ruta_covid} status",shell=True,capture_output=True,text=True).stdout

        print("Cheking update ...")

        if "Tu rama está detrás" in output:
            
            # git pull
            os.system(f"git -C {self.ruta_covid} pull")


            datosUpdated = self.check_update_por_tipo()
            if len(datosUpdated)==0:
                return False, []

            generar_todos_los_plots()
            ## Excecute python or julia scripts to create graphs
            return True, datosUpdated
        else:
            return False, []


    def check_update_por_tipo(self):
        # Check that the wanted that was updated and not other
        time_now = datetime.datetime.now()
        updatedDatos = []
        for dato in self.info_datos:

            try:
                nombre_dato = dato[1]
                filedir = dato[2]
                file_time = datetime.datetime.fromtimestamp(os.path.getmtime(filedir))

                minutes_passed = (time_now - file_time).total_seconds()/60

                if minutes_passed < 10: # 
                    updatedDatos.append(nombre_dato)

            except:
                pass
        
        return updatedDatos



if __name__ == "__main__":

    d = CheckData(PATH_COVID, INFO_DATOS)
    a,b = d.check_nueva_data()

    print(a,b)
    #while True:
    #    checkNewData()
    #    sleep(10)

