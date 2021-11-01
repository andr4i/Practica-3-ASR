# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import _thread
import os.path
import time
from os import system
from fpdf import FPDF

from getSNMP import consultaSNMP

def reporte(direccionip):
    #Leemos los valores de nuestro archivo
    with open(direccionip+".txt","r") as f:
        content = f.readlines()
    descripcion = ""
    for x in content:
        descripcion = descripcion + x + "  "
    #Empezamos a crear nuestro PDF
    cadena = "Reporte de consumo de Paquetes. Usted actualmente ha utilizado la siguiente cantidad de paquetes UDP"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.cell(200,10,txt = cadena,ln = 1, align = "a")
    pdf.cell(200, 10, txt=descripcion, ln=1, align="a")
    pdf.output(direccionIP+".pdf")

def actualizah(ip,comunidad):
    # Use a breakpoint in the code line below to debug your script.
    #Leemos el archivo donde tenemos la tarifa y el limite de paquetes
    with open(ip+".txt","r") as f:
        content = f.readlines()
    #Guardamos en un arreglo los datos que leimos sin el salto de linea y sin los identificadores
    reglas = []
    for cadenas in content:
        reglas.append(cadenas.strip("\n"))
    listai = []
    for x in reglas:
        listai.append(x.split(":"))
    listaf = []
    for x in listai:
        listaf.append(x[1])
    # Guardamos los datos en variables locales
    tarifa = float(listaf[0])
    entradapaq = int(listaf[1])
    limitepaq = int(listaf[2])
    costoextra = float(listaf[3])
    # Esta variables contendra los paquetesUDP de una consulta atras
    paqanterior = 0
    while 1 :
        #Actualizamos el contador de paquetes
        paquetesact = int(consultaSNMP(comunidad, direccionIP, '1.3.6.1.2.1.7.1.0'))
        # SI el valor es mayor que nuestro contador calculamos el costo extra
        if (entradapaq > limitepaq):
            tarifa = 0.01
            costoextra = tarifa * (entradapaq - limitepaq)
            entradapaq = paquetesact
        diferencia = paquetesact - paqanterior
        entradapaq = entradapaq + diferencia
        paqanterior = paquetesact
        # Guardamos nuestro archivo con los valores actualizados
        contenido = "Tarifa:" + str(tarifa) + "\nudpi:" + str(entradapaq) + "\nudpil:" + str(
            limitepaq) + "\ncosteextra:" + str(costoextra) + "\n"
        with open(direccionIP + ".txt", "w") as f:
            f.write(contenido)
        time.sleep(1)

if __name__ == '__main__':
    listahilos = []
    inicio = False
    print("Practica 3 - Gestion de Recursos UDP")
    while 1:
        system("clear")
        print("Monitor de recursos SNMP")
        print("Seleccione una opción: ")
        print("1) Agregar un dispositivo para monitorear")
        print("2) Generar reporte de consumo")
        a = int(input())
        print(a)
        if (a == 1):  # Preguntamos la información del nuevo dispositivo
            print("Introduce la dirección IP del dispositivo:")
            direccionIP = input()
            print("Introduce el nombre de la comunidad:")
            comunidad = input()
            try:
                sysinfo = consultaSNMP(comunidad, direccionIP, "1.3.6.1.2.1.1.1.0")
                print("Accediendo a :" + sysinfo)
            except:
                print("Ocurrio un error al tratar de conectar con el dispositivo")
            else:
                # Luego creamos el archivo donde estaremos actualizando los datos del usuario
                contenido = ("Tarifa:0.00\nudpi:0\nudpil:100000\ncosteextra:0\n")
                # Si el archivo existe entonces no lo sobreescribimos
                ruta = "/home/gonzalo/PycharmProjects" + direccionIP + ".txt"
                if(os.path.isfile(ruta)==False):
                    with open(direccionIP + ".txt", "w") as hdlr:
                        hdlr.write(contenido)
                # Verificamos que si existe un hilo con esa dirección ya iniciado
                if(direccionIP not in listahilos):
                    -_thread.start_new_thread(actualizah, (direccionIP,comunidad))
                    listahilos.append(direccionIP)
                    # 1
        if (a==2):
            print("Introduce la dirección IP del dispositivo:")
            direccionIP = input()
            if(direccionIP in listahilos):
                reporte(direccionIP)
                print("Reporte generado")
                input("Presione enter para continuar")
            else:
                print("No se encuentra registros de esa dirección")
                time.sleep(1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
