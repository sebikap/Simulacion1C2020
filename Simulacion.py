# -*- coding: utf-8 -*-
"""
Created on Sat May 16 16:38:17 2020

@author: Seba
"""

# IMPORTS #
from random import seed
from random import random
from random import randrange
from os import system
import numpy as np
import smtplib

#############################
#   DECLARACION VARIABLES   #
#############################

#### CONDICIONES INCIALES ####
tiempo = 0

# Eventos Futuros
tiempoLlegada = 0
tiempoSalida = []
tiempoProximaReposicionCuadernos = 100
tiempoProximaReposicionPokemon = 400

# Variables datos
intervaloArribos = 0
tiempoAtencion = 0
cantidadElementosComprados = 0

# Variables de control
cantidadCajeras = 0
pedidoCuadernos = 0
pedidoPokemon = 0

# Variables de estado
cantidadPersonasEnElSistema = 0
stockCuadernos = 500
stockPokemon = 500

# Variables de resultado
promedioTiempoEspera = 0
porcentajeArrepentimiento = 0
porcentajeTiempoOcioso = 0
porcentajeVentasPerdidas = 0

# Variables auxiliares del sistema
cantidadTotalPersonas = 0
ventasPerdidas = 0
arrepentidos = 0
inicioTiempoOcioso = []
sumatoriaTiempoLlegada = 0
sumatoriaTiempoSalida = 0
sumatoriaTiempoOcioso = 0
sumatoriaTiempoAtencion = 0
eventos = [[],["tpll","tprc","tprp","tps"]]
puestoActual = 0
running = True
database = list()

destinatarios = ["florenciamacarenalopez@gmail.com", "lucasgabrielvallejos96@gmail.com", "sebikap@gmail.com"]
remitente = "simulacion80@gmail.com"
tiempoFinal = 0

#############################
#   DECLARACION FUNCIONES   #
#############################

def cleanAllVariablesForTheNextSimulation():
    global tiempo
    global tiempoLlegada
    global tiempoSalida
    global tiempoProximaReposicionCuadernos
    global tiempoProximaReposicionPokemon
    global intervaloArribos
    global tiempoAtencion
    global cantidadElementosComprados
    global cantidadCajeras
    global pedidoCuadernos
    global pedidoPokemon
    global cantidadPersonasEnElSistema
    global stockCuadernos
    global stockPokemon
    global promedioTiempoEspera
    global porcentajeArrepentimiento
    global porcentajeTiempoOcioso
    global porcentajeVentasPerdidas
    global cantidadTotalPersonas
    global ventasPerdidas
    global arrepentidos
    global inicioTiempoOcioso
    global sumatoriaTiempoSalida
    global sumatoriaTiempoAtencion
    global sumatoriaTiempoOcioso
    global sumatoriaTiempoLlegada
    global eventos
    global puestoActual
        
    #### CONDICIONES INCIALES ####
    tiempo = 0

    # Eventos Futuros
    tiempoLlegada = 0
    tiempoSalida = []
    tiempoProximaReposicionCuadernos = 100
    tiempoProximaReposicionPokemon = 400

    # Variables datos
    intervaloArribos = 0
    tiempoAtencion = 0
    cantidadElementosComprados = 0

    # Variables de control
    cantidadCajeras = 0
    pedidoCuadernos = 0
    pedidoPokemon = 0

    # Variables de estado
    cantidadPersonasEnElSistema = 0
    stockCuadernos = 100
    stockPokemon = 100

    # Variables de resultado
    promedioTiempoEspera = 0
    porcentajeArrepentimiento = 0
    porcentajeTiempoOcioso = 0
    porcentajeVentasPerdidas = 0

    # Variables auxiliares del sistema
    cantidadTotalPersonas = 0
    ventasPerdidas = 0
    arrepentidos = 0
    inicioTiempoOcioso = []
    sumatoriaTiempoLlegada = 0
    sumatoriaTiempoSalida = 0
    sumatoriaTiempoOcioso = 0
    sumatoriaTiempoAtencion = 0
    eventos = [[],["tpll","tprc","tprp","tps"]]
    puestoActual = 0

def generarIntervaloDeArribo():
    #TODO REEEMPLAZAR POR FUNCION DE PROBABILIDAD
    global intervaloArribos
    #intervaloArribos = randrange(1,10)
    intervaloArribos = np.random.geometric(p=0.03806)
    #print("Intervalo de arribos: " + str(ia))
    return 0

def generarCantidadDeElementos():
    #TODO REEEMPLAZAR POR FUNCION DE PROBABILIDAD
    global cantidadElementosComprados
    #cantidadElementosComprados = randrange(1, 10)
    cantidadElementosComprados = np.random.binomial(n=1,p=0.77)
    if (cantidadElementosComprados == 0):
        cantidadElementosComprados = 2
    #print("Cantidad de elementos: " + str(ce))
    return 0

def generarTiempoDeAtencion():
    #TODO REEEMPLAZAR POR FUNCION DE PROBABILIDAD
    global tiempoAtencion
    #tiempoAtencion = random() * 100
    tiempoAtencion = np.random.binomial(n=191, p=0.03603)
    #print("Tiempo de atención: " + str(ta))
    return 0

def buscoCajeroLibre():
    global puestoActual
    puestoActual = tiempoSalida.index("H.V")
    #print("Puesto actual: " + str(puestoActual))
    return 0

def definirVariablesControl():
    print("\t**************************************")
    print("\t*  DEFINIR VARIABLES DE CONTROL      *")
    print("\t**************************************")

    global cantidadCajeras
    global inicioTiempoOcioso
    global tiempoSalida
    cantidadCajeras = int(input("\nIngrese la variable de control: Cantidad de Cajeros -> "))
    
    for i in range(0, cantidadCajeras):
        inicioTiempoOcioso.append(0)
        tiempoSalida.append("H.V")

    global pedidoCuadernos
    pedidoCuadernos = int(input("\nIngrese la variable de control: Pedido Cuadernos -> "))
    
    global pedidoPokemon
    pedidoPokemon = int(input("\nIngrese la variable de control: Pedido Pokemones -> "))

def definirTiempoFinal():
    print("\t********************************************")
    print("\t*  DEFINIR TIEMPO FINAL DE LA SIMULACION   *")
    print("\t********************************************")

    global tiempoFinal    
    tiempoFinal = int(input("\nIngrese el Tiempo Final de la Simulacion -> "))

def proximoEvento():
    global puestoActual
    global eventos

    #Obtengo el menor de los tiempos próximos de salida
    tpsi = tiempoFinal + tiempoFinal/2
    vacios = 0
    for i in range(0, len(tiempoSalida)):
        if(tiempoSalida[i] != "H.V"):
            if(tiempoSalida[i] < tpsi):
                puestoActual = i
                tpsi = tiempoSalida[puestoActual]
        else:
            vacios = vacios + 1
    
    if(tiempoLlegada != "H.V"):
        #Limpio y vuelvo a cargar la lista con los tiempos de los eventos
        eventos[0].clear()
        eventos[0].append(tiempoLlegada)
        eventos[0].append(tiempoProximaReposicionCuadernos)    
        eventos[0].append(tiempoProximaReposicionPokemon)
        eventos[0].append(tpsi)
        
        # Itero para encontrar el mínimo tiempo, junto con el indice correspondiente
        evento = ""
        tiempo = min(tiempoLlegada, tiempoProximaReposicionCuadernos, tiempoProximaReposicionPokemon)
        elementos = len(eventos[0])
        if(vacios == len(tiempoSalida)):
            # Todos los puestos están en H.V, entonces asigno por defecto el puesto acutual a 0
            puestoActual = 0
            elementos = elementos - 1
        else:
            # En caso de que hay algún puesto no vacio, comparo el tiempo próximo de salida del puesto con los otros eventos
            # Se hace de esta manera para que en caso de que todos los puestos estén en H.V, no rompa por pasar un str a la función min
            tiempo = min(tiempo, tpsi)

        for i in range(0, elementos):
            if(eventos[0][i] <= tiempo):
                tiempo = eventos[0][i]
                evento = eventos[1][i]
    else:
        evento = "tps"

    return evento

def manejoProximoEvento(evento):
    if(evento == "tpll"):
        llegadaCliente()
    elif(evento == "tps"):
        salidaPuesto()
    elif(evento == "tprc"):
        pedidoDeCuadernos()
    elif(evento == "tprp"):
        pedidoPokemones()
    else:
        print("Finalización de la simulación con error")
        print(evento)
        exit(0)
    return

def stockDisponible():
    global stockCuadernos
    global stockPokemon

    generarCantidadDeElementos()
    rand = random()
    if(rand < 0.65):
        print("Compra cuadernos")
        if(stockCuadernos < cantidadElementosComprados):
            print("SIN STOCK")
            sinStock()
            return False
        else:
            print("HAY STOCK")
            stockCuadernos = stockCuadernos - cantidadElementosComprados
            return True
    else:
        print("Compra pokemones")
        if(stockPokemon < cantidadElementosComprados):
            print("SIN STOCK")
            sinStock()
            return False
        else:
            print("HAY STOCK")
            stockPokemon = stockPokemon - cantidadElementosComprados
            return True
    return False

def seLiberoPuesto():
    global inicioTiempoOcioso
    global tiempoSalida
    print("INICIO TIEMPO OCIOSO PUESTO " + str(puestoActual))
    inicioTiempoOcioso[puestoActual] = tiempo
    tiempoSalida[puestoActual] = "H.V"
    return 1

def buscoCliente():
    if(not stockDisponible()):
        if (cantidadPersonasEnElSistema >= cantidadCajeras):
            print("Se fue un cliente por falta de stock, busco otro. Quedan: " + str(cantidadPersonasEnElSistema))
            buscoCliente()
        else:
            print("Todos los clientes de la fila se fueron por falta de stock")
            seLiberoPuesto()
            return False
    return True

def llegadaCliente():
    global tiempoLlegada
    global cantidadTotalPersonas
    global cantidadPersonasEnElSistema
    global stockCuadernos
    global stockPokemon
    global tiempoSalida
    global sumatoriaTiempoOcioso
    global sumatoriaTiempoLlegada
    global sumatoriaTiempoAtencion
    global tiempo

    print("LLEGADA CLIENTE")
    tiempo = tiempoLlegada
    generarIntervaloDeArribo()
    tiempoLlegada = tiempo + intervaloArribos
    cantidadTotalPersonas = cantidadTotalPersonas + 1
    arrep = arrepentimiento()
    if (not arrep):
        print("No se arrepintió")
        cantidadPersonasEnElSistema = cantidadPersonasEnElSistema + 1
        if(cantidadPersonasEnElSistema <= cantidadCajeras):
            if(stockDisponible()):
                buscoCajeroLibre()
                print("Atiende el cajero " + str(puestoActual))
                sumatoriaTiempoOcioso = sumatoriaTiempoOcioso + (tiempo - inicioTiempoOcioso[puestoActual])
                sumatoriaTiempoLlegada = sumatoriaTiempoLlegada + tiempo
                generarTiempoDeAtencion()
                sumatoriaTiempoAtencion = sumatoriaTiempoAtencion + tiempoAtencion
                tiempoSalida[puestoActual] = tiempo + tiempoAtencion
                print("El tiempo de atención será de: " + str(tiempoAtencion))
                print("El cliente sale a las: " + str(tiempoSalida[puestoActual]))
    return 1

def salidaPuesto():
    global sumatoriaTiempoSalida
    global sumatoriaTiempoAtencion
    global cantidadPersonasEnElSistema
    global tiempoSalida
    global inicioTiempoOcioso
    global tiempo

    print("SE LIBERA PUESTO " + str(puestoActual))
    tiempo = tiempoSalida[puestoActual]
    sumatoriaTiempoSalida = sumatoriaTiempoSalida + tiempo
    cantidadPersonasEnElSistema = cantidadPersonasEnElSistema - 1
    print("Ahora, NS = " + str(cantidadPersonasEnElSistema))
    if(cantidadPersonasEnElSistema >= cantidadCajeras):
        print("ATIENDO CLIENTE")
        buscoCliente()
        if(cantidadPersonasEnElSistema>=cantidadCajeras):
            generarTiempoDeAtencion()
            tiempoSalida[puestoActual] = tiempo + tiempoAtencion
            print("El tiempo de atención será de: " + str(tiempoAtencion))
            print("El cliente sale a las: " + str(tiempoSalida[puestoActual]))
            sumatoriaTiempoAtencion = sumatoriaTiempoAtencion + tiempoAtencion
    else:
        seLiberoPuesto()
    print("Después del manejo del evento salida, NS = " + str(cantidadPersonasEnElSistema))
    return 1

def pedidoDeCuadernos():
    global tiempo    
    global stockCuadernos    
    global tiempoProximaReposicionCuadernos    

    print("RECIBO CUADERNOS")
    tiempo = tiempoProximaReposicionCuadernos
    tiempoProximaReposicionCuadernos = tiempo + (14 * 8 * 60) #TODO REVISAR UNIDADES
    stockCuadernos = stockCuadernos + pedidoCuadernos
    return 1

def pedidoPokemones():
    global tiempo    
    global stockPokemon    
    global tiempoProximaReposicionPokemon
    
    print("RECIBO POKEMONES")
    tiempo = tiempoProximaReposicionPokemon
    tiempoProximaReposicionPokemon = tiempo + (30 * 8 * 60) #TODO REVISAR UNIDADES
    stockPokemon = stockPokemon + pedidoPokemon
    return 1

def arrepentimiento():
    global arrepentidos
    print("Chequeo arrepentimiento con ns = " + str(cantidadPersonasEnElSistema))
    if(cantidadPersonasEnElSistema > 15):
        arrepentidos = arrepentidos + 1
        return True
    elif (cantidadPersonasEnElSistema > 10):
        rand = random()
        if(rand > 0.4):
            arrepentidos = arrepentidos + 1
            return True
    return False

def sinStock():
    global ventasPerdidas
    global cantidadPersonasEnElSistema

    ventasPerdidas = ventasPerdidas + 1
    cantidadPersonasEnElSistema = cantidadPersonasEnElSistema - 1

    return 1

def vaciamiento():
    print("VACIAMIENTO")
    global tiempoLlegada
    global tiempoProximaReposicionCuadernos
    global tiempoProximaReposicionPokemon

    print("CANTIDAD DE PERSONAS EN EL SISTEMA")
    print(cantidadPersonasEnElSistema)
    print("")
    cantVaciamiento = 1
    while(cantidadPersonasEnElSistema != 0):  
        print("VACIAMIENTO " + str(cantVaciamiento))
        cantVaciamiento = cantVaciamiento + 1

        tiempoLlegada = "H.V"
        tiempoProximaReposicionCuadernos = "H.V"
        tiempoProximaReposicionPokemon = "H.V"
        
        proxEvent = proximoEvento()
        manejoProximoEvento(proxEvent)

        print("TERMINA VACIAMIENTO - t: " + str(tiempo))
        print("NS: " + str(cantidadPersonasEnElSistema))
        for i in range(0,cantidadCajeras):
            print("TPS" + str(i) + ": " + str(tiempoSalida[i]))
        print("")
        print("------------------------------------------")
        print("")


    return 1

def calculoDeResultados():   
    global promedioTiempoEspera    
    global porcentajeArrepentimiento
    global porcentajeTiempoOcioso
    global porcentajeVentasPerdidas
    
    if(cantidadTotalPersonas != 0):
        promedioTiempoEspera = (sumatoriaTiempoSalida - sumatoriaTiempoLlegada - sumatoriaTiempoAtencion) / cantidadTotalPersonas
        porcentajeArrepentimiento = (arrepentidos/cantidadTotalPersonas) * 100
        porcentajeTiempoOcioso = (sumatoriaTiempoOcioso/(tiempo*cantidadCajeras)) * 100
        porcentajeVentasPerdidas = (ventasPerdidas/cantidadTotalPersonas) * 100

        print("SSAL: " + str(sumatoriaTiempoSalida))
        print("SLL: " + str(sumatoriaTiempoLlegada))
        print("STA: " + str(sumatoriaTiempoAtencion))
        print("STO: " + str(sumatoriaTiempoOcioso))
        print("T: " + str(tiempo))
        print("VP: " + str(ventasPerdidas))
    else:
        print("No ingresó nadie al sistema")
    return 1

def impresionDeResultados():
    print("-------------RESULTADOS--------------")
    
    print("Variable de control - Cantidad de puestos: " + str(cantidadCajeras))

    print("Variable de control - Pedido de cuadrenos: " + str(pedidoCuadernos))
    
    print("Variable de control - Pedido de pokemones: " + str(pedidoPokemon))

    print("Cantidad total de clientes: " + str(cantidadTotalPersonas))

    print("Promedio de tiempo de espera: " + str(promedioTiempoEspera))
    
    print("Porcentaje de arrepentimiento: " + str(porcentajeArrepentimiento))
    
    print("Porcentaje de tiempo ocioso general: " + str(porcentajeTiempoOcioso))
    
    print("Porcentaje de ventas perdidas por falta de stock: " + str(porcentajeVentasPerdidas))
    
    print("-------------------------------------")
    
    addNewHistorialResultados()

    return 1

def addNewHistorialResultados():

    nuevoResultado = {
        "CantidadCajeros": cantidadCajeras, 
        "PedidoCuadernos": pedidoCuadernos, 
        "PedidoPokemon": pedidoPokemon,
        "TiempoFinal": tiempoFinal,
        "TotalClientes": cantidadTotalPersonas,
        "PromedioTiempoDeEspera": promedioTiempoEspera,
        "PorcentajeArrepentimiento": porcentajeArrepentimiento,
        "PorcentajeTiempoOcioso": porcentajeTiempoOcioso,
        "PorcentajeVentasPerdidas": porcentajeVentasPerdidas
    }
    database.append(nuevoResultado)

def verUltimosResultados():
    tamañoBase = len(database)
    print("\t**************************************")
    print("\t*       LISTADO DE RESULTADOS        *")
    print("\t**************************************")

    for x in range(tamañoBase):
        print("\n\tSimulacion N°: ", x+1)
        print("\n*CANTIDAD CAJERAS   ---> ", database[x]["CantidadCajeros"])
        print("\n*PEDIDO CUADERNOS   ---> ", database[x]["PedidoCuadernos"])
        print("\n*PEDIDO POKEMON     ---> ", database[x]["PedidoPokemon"])
        print("\n*TIEMPO FINAL SIMULACION ---> ", database[x]["TiempoFinal"])
        print("\n*TOTAL CLIENTES ---> ", database[x]["TotalClientes"])
        print("\n*PROMEDIO TIEMPO ESPERA ---> ", database[x]["PromedioTiempoDeEspera"])
        print("\n*PORCENTAJE ARREPENTIMIENTOS ---> ", database[x]["PorcentajeArrepentimiento"])
        print("\n*PORCENTAJE TIEMPO OCIOSO ---> ", database[x]["PorcentajeTiempoOcioso"])
        print("\n*PORCENTAJE VENTAS PERDIDAS ---> ", database[x]["PorcentajeVentasPerdidas"])


def imprimirEstado():
    print("")
    print("--------ESTADO--------")

    print("T: " + str(tiempo))

    # Eventos Futuros
    print("TPLL: " + str(tiempoLlegada))
    print("TPRC: " + str(tiempoProximaReposicionCuadernos))
    print("TPRP: " + str(tiempoProximaReposicionPokemon))
    print("TPS: ")
    print(tiempoSalida)

    # Variables datos
    print("IA: " + str(intervaloArribos))
    print("TA: " + str(tiempoAtencion))
    print("CE: " + str(cantidadElementosComprados))

    # Variables de control
    #cc
    #pc
    #pp

    # Variables de estado
    print("NS: " + str(cantidadPersonasEnElSistema))
    print("SC: " + str(stockCuadernos))
    print("SP: " + str(stockPokemon))
    
    print("NT: " + str(cantidadTotalPersonas))
    print("VP: " + str(ventasPerdidas))
    print("ARR: " + str(arrepentidos))
    print("SLL: " + str(sumatoriaTiempoLlegada))
    print("SSAL: " + str(sumatoriaTiempoSalida))
    print("STO: " + str(sumatoriaTiempoOcioso))
    print("STA: " + str(sumatoriaTiempoAtencion))
    print("Puesto Actual: " + str(puestoActual))

    print("ITO: ")
    print(inicioTiempoOcioso)
    
    print("--------FIN ESTADO--------")
    print("")
    return 1

#########################
#   Programa Principal  #
#########################

def simulation():
    print("\t**************************************")
    print("\t*      COMIENZO DE LA SIMULACION     *")
    print("\t**************************************")
    
    #Seteo el seed para el random del arrepentimiento
    seed(1)
        
    while(tiempo < tiempoFinal):  
        #imprimirEstado()
        print("ARRANCA VUELTA - t: " + str(tiempo))
        print("NS: " + str(cantidadPersonasEnElSistema))
        proxEvent = proximoEvento()
        manejoProximoEvento(proxEvent)
        print("TERMINA VUELTA - t: " + str(tiempo))
        print("NS: " + str(cantidadPersonasEnElSistema))
        for i in range(0,cantidadCajeras):
            print("TPS" + str(i) + ": " + str(tiempoSalida[i]))
        print("\n------------------------------------------\n")
    
    vaciamiento()
    calculoDeResultados()
    impresionDeResultados()
    cleanAllVariablesForTheNextSimulation()
    print("\n\t**************************************")
    print("\t*   FINALIZACION DE LA SIMULACION    *")
    print("\t**************************************")

def validateResponde(response):
    #validamos que la eleccion del usuario sea la correcta. Por defecto suponemos que no.
    validate = False
    resp = 0
    msg = "\nEleccion incorrecta. Intente nuevamente.\n"

    if response.isdigit():
        resp = int(response)
        if resp>=1 and resp <=6:
            msg = ""
            validate = True
    return validate, resp, msg

def validatePreviousSimulation():
    if(cantidadCajeras == 0 or pedidoCuadernos == 0 or pedidoPokemon == 0 or tiempoFinal == 0):
        print("\t**************************************")
        print("\t*      ACLARACION - CUIDADO          *")
        print("\t**************************************")
        print("\nSe deben inicializar las variables de control y el Tiempo Final antes de realizar la simulacion.")
        print("Muchas gracias\n")
        return 1
    simulation()

def enviarPorMail():
    destinatario = input("Ingrese el mail del destinatario -> ")
    destinatarios.append(destinatario)
    tamañoBase = len(database)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(remitente,"FlorSebasLucas")

        subject = 'Resultados de las Simulaciones'

        body = ''
        
        for x in range(tamañoBase):
            numSimulacion = ("Simulacion N: ", str(x+1))
            body += numSimulacion[0] + numSimulacion[1]
            var1 = (" CANTIDAD CAJERAS    ---> ", str(database[x]["CantidadCajeros"]))
            body += var1[0] + var1[1]
            var2 = (" PEDIDO CUADERNOS    ---> ", str(database[x]["PedidoCuadernos"]))
            body += var2[0] + var2[1]
            var3 = (" PEDIDO POKEMON      ---> ", str(database[x]["PedidoPokemon"]))
            body += var3[0] + var3[1]
            var4 = (" TIEMPO FINAL SIMULACION ---> ", str(database[x]["TiempoFinal"]))
            body += var4[0] + var4[1]
            var5 = (" TOTAL CLIENTES      ---> ", str(database[x]["TotalClientes"]))
            body += var5[0] + var5[1]
            var6 = (" PROMEDIO TIEMPO ESPERA  ---> ", str(database[x]["PromedioTiempoDeEspera"]))
            body += var6[0] + var6[1]
            var7 = (" PORCENTAJE ARREPENTIMIENTOS ---> ", str(database[x]["PorcentajeArrepentimiento"]))
            body += var7[0] + var7[1]
            var8 = (" PORCENTAJE TIEMPO OCIOSO ---> ", str(database[x]["PorcentajeTiempoOcioso"]))
            body += var8[0] + var8[1]
            var9 = (" PORCENTAJE VENTAS PERDIDAS ---> ", str(database[x]["PorcentajeVentasPerdidas"]))
            body += var9[0] + var9[1]      
            body += "**************************************************"
        
        body = body.encode('utf-8')
        msg = f'Subject: {subject}\n\n{body}'
        
        smtp.sendmail(remitente, destinatarios, msg)   

    print("\nMail Enviado Con Exito!")

def salir():
    global running
    running = False
    print ("Esperemos que haya disfrutado el sistema, hasta la proxima!.\n")

def showMenu():
    global running
    running = True
    print("\n\t1. Definir las Variables de Control.")
    print("\t2. Definir el Tiempo Final.")
    print("\t3. Empezar la Simulacion.")
    print("\t4. Ver Resultados de las Últimas Simulaciones.")
    print("\t5. Enviar Resultados por Mail.")
    print("\t6. Salir.")
    print("\t~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n")
    response = input("Seleccione el numero de opcion -> ")
    system('CLS')
    return response 

print("\tBienvenido al Sistema de Simulacion de Librerias\n")

#   **************************
#   *   LOOP PRINCIPAL       *
#   **************************
while(running):
    menuOptions = {1: definirVariablesControl, 2:definirTiempoFinal, 3:validatePreviousSimulation, 4:verUltimosResultados, 5:enviarPorMail, 6:salir}    
    response = showMenu()
    validate, resp, msg = validateResponde(response)
    if(validate):
        funcion = menuOptions.get(resp)
        funcion()
    else:
        print(msg)