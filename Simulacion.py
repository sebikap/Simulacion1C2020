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

#### CONDICIONES INCIALES ####
t = 0

# Eventos Futuros
tpll = 0
tps = []
tprc = 100
tprp = 400

# Variables datos
ia = 0
ta = 0
ce = 0

# Variables de control
cc = 0
pc = 0
pp = 0

# Variables de estado
ns = 0
sc = 100
sp = 100

# Variables de resultado
pte = 0
pa = 0
pto = 0
pvp = 0

# Variables auxiliares del sistema
nt = 0
vp = 0
arr = 0
ito = []
sll = 0
ssal = 0
sto = 0
sta = 0
eventos = [[],["tpll","tprc","tprp","tps"]]
puestoActual = 0

#TODO VER CÓMO SE DEFINE
tf = 0

def generarIntervaloDeArribo():
    #TODO REEEMPLAZAR POR FUNCION DE PROBABILIDAD
    global ia
    ia = randrange(1,10)
    #print("Intervalo de arribos: " + str(ia))
    return 0

def generarCantidadDeElementos():
    #TODO REEEMPLAZAR POR FUNCION DE PROBABILIDAD
    global ce
    ce = randrange(1, 10)
    #print("Cantidad de elementos: " + str(ce))
    return 0

def generarTiempoDeAtencion():
    #TODO REEEMPLAZAR POR FUNCION DE PROBABILIDAD
    global ta
    ta = random() * 100
    #print("Tiempo de atención: " + str(ta))
    return 0

def buscoCajeroLibre():
    global puestoActual
    puestoActual = tps.index("H.V")
    #print("Puesto actual: " + str(puestoActual))
    return 0

def variablesDeControl():
    print("Ingrese la variable de control: Cantidad de Cajeros")
    global cc
    global ito
    global tps

    cc = int(input())
    
    for i in range(0, cc):
        ito.append(0)
        tps.append("H.V")

    print("Ingrese la variable de control: Pedido Cuadernos")
    global pc
    pc = int(input())
    
    print("Ingrese la variable de control: Pedido Pokemones")
    global pp
    pp = int(input())

    #TODO REVISAR
    print("Ingrese el tiempo final de la simulación")
    global tf
    tf = int(input())
    
    return 0

def proximoEvento():
    global puestoActual
    global eventos

    #Obtengo el menor de los tiempos próximos de salida
    tpsi = tf + tf/2
    vacios = 0
    for i in range(0, len(tps)):
        if(tps[i] != "H.V"):
            if(tps[i] < tpsi):
                puestoActual = i
                tpsi = tps[puestoActual]
        else:
            vacios = vacios + 1
    
    if(tpll != "H.V"):
        #Limpio y vuelvo a cargar la lista con los tiempos de los eventos
        eventos[0].clear()
        eventos[0].append(tpll)
        eventos[0].append(tprc)    
        eventos[0].append(tprp)
        eventos[0].append(tpsi)
        
        # Itero para encontrar el mínimo tiempo, junto con el indice correspondiente
        evento = ""
        tiempo = min(tpll, tprc, tprp)
        elementos = len(eventos[0])
        if(vacios == len(tps)):
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
        pedidoCuadernos()
    elif(evento == "tprp"):
        pedidoPokemones()
    else:
        print("Finalización de la simulación con error")
        print(evento)
        exit(0)
    return

def stockDisponible():
    global sc
    global sp

    generarCantidadDeElementos()
    rand = random()
    if(rand < 0.65):
        print("Compra cuadernos")
        if(sc < ce):
            print("SIN STOCK")
            sinStock()
            return False
        else:
            print("HAY STOCK")
            sc = sc - ce
            return True
    else:
        print("Compra pokemones")
        if(sp < ce):
            print("SIN STOCK")
            sinStock()
            return False
        else:
            print("HAY STOCK")
            sp = sp - ce
            return True
    return False

def seLiberoPuesto():
    global ito
    global tps
    print("INICIO TIEMPO OCIOSO PUESTO " + str(puestoActual))
    ito[puestoActual] = t
    tps[puestoActual] = "H.V"
    return 1

def buscoCliente():
    if(not stockDisponible()):
        if (ns >= cc):
            print("Se fue un cliente por falta de stock, busco otro. Quedan: " + str(ns))
            buscoCliente()
        else:
            print("Todos los clientes de la fila se fueron por falta de stock")
            seLiberoPuesto()
            return False
    return True

def llegadaCliente():
    global tpll
    global nt
    global ns
    global sc
    global sp
    global tps
    global sto
    global sll
    global sta
    global t

    print("LLEGADA CLIENTE")
    t = tpll
    generarIntervaloDeArribo()
    tpll = t + ia
    nt = nt + 1
    arrep = arrepentimiento()
    if (not arrep):
        print("No se arrepintió")
        ns = ns + 1
        if(ns <= cc):
            if(stockDisponible()):
                buscoCajeroLibre()
                print("Atiende el cajero " + str(puestoActual))
                sto = sto + (t - ito[puestoActual])
                sll = sll + t
                generarTiempoDeAtencion()
                sta = sta + ta
                tps[puestoActual] = t + ta
                print("El cliente sale a las: " + str(tps[puestoActual]))
    return 1

def salidaPuesto():
    global ssal
    global sta
    global ns
    global tps
    global ito
    global t

    print("SE LIBERA PUESTO " + str(puestoActual))
    t = tps[puestoActual]
    ssal = ssal + t
    ns = ns - 1
    print("Ahora, NS = " + str(ns))
    if(ns >= cc):
        print("ATIENDO CLIENTE")
        buscoCliente()
        if(ns>=cc):
            generarTiempoDeAtencion()
            tps[puestoActual] = t + ta
            print("El cliente sale a las: " + str(tps[puestoActual]))
            sta = sta + ta
    else:
        seLiberoPuesto()
    print("Después del manejo del evento salida, NS = " + str(ns))
    return 1

def pedidoCuadernos():
    global t    
    global sc    
    global tprc    

    print("RECIBO CUADERNOS")
    t = tprc
    tprc = t + (14 * 8 * 60) #TODO REVISAR UNIDADES
    sc = sc + pc
    return 1

def pedidoPokemones():
    global t    
    global sp    
    global tprp
    
    print("RECIBO POKEMONES")
    t = tprp
    tprp = t + (30 * 8 * 60) #TODO REVISAR UNIDADES
    sp = sp + pp
    return 1

def arrepentimiento():
    global arr
    print("Chequeo arrepentimiento con ns = " + str(ns))
    if(ns > 15):
        arr = arr + 1
        return True
    elif (ns > 10):
        rand = random()
        if(rand > 0.4):
            arr = arr + 1
            return True
    return False

def sinStock():
    global vp
    global ns

    vp = vp + 1
    ns = ns - 1

    return 1

def vaciamiento():
    print("VACIAMIENTO")
    global tpll
    global tprc
    global tprp

    print("CANTIDAD DE PERSONAS EN EL SISTEMA")
    print(ns)
    print("")
    cantVaciamiento = 1
    while(ns != 0):  
        print("VACIAMIENTO " + str(cantVaciamiento))
        cantVaciamiento = cantVaciamiento + 1

        tpll = "H.V"
        tprc = "H.V"
        tprp = "H.V"
        
        proxEvent = proximoEvento()
        manejoProximoEvento(proxEvent)

        print("TERMINA VACIAMIENTO - t: " + str(t))
        print("NS: " + str(ns))
        for i in range(0,cc):
            print("TPS" + str(i) + ": " + str(tps[i]))
        print("")
        print("------------------------------------------")
        print("")


    return 1

def calculoDeResultados():   
    global pte    
    global pa
    global pto
    global pvp
    
    if(nt != 0):
        pte = (ssal - sll - sta) / nt
        pa = (arr/nt) * 100
        pto = (sto/(t*cc)) * 100
        pvp = (vp/nt) * 100

        print("SSAL: " + str(ssal))
        print("SLL: " + str(sll))
        print("STA: " + str(sta))
        print("STO: " + str(sto))
        print("T: " + str(t))
        print("VP: " + str(vp))
    else:
        print("No ingresó nadie al sistema")
    return 1

def impresionDeResultados():
    print("-------------RESULTADOS--------------")
    
    print("Cantidad total de clientes: " + str(nt))

    print("Promedio de tiempo de espera: " + str(pte))
    
    print("Porcentaje de arrepentimiento: " + str(pa))
    
    print("Porcentaje de tiempo ocioso general: " + str(pto))
    
    print("Porcentaje de ventas perdidas por falta de stock: " + str(pvp))
    
    print("-------------------------------------")
    
    return 1

def imprimirEstado():
    print("")
    print("--------ESTADO--------")

    print("T: " + str(t))

    # Eventos Futuros
    print("TPLL: " + str(tpll))
    print("TPRC: " + str(tprc))
    print("TPRP: " + str(tprp))
    print("TPS: ")
    print(tps)

    # Variables datos
    print("IA: " + str(ia))
    print("TA: " + str(ta))
    print("CE: " + str(ce))

    # Variables de control
    #cc
    #pc
    #pp

    # Variables de estado
    print("NS: " + str(ns))
    print("SC: " + str(sc))
    print("SP: " + str(sp))
    
    print("NT: " + str(nt))
    print("VP: " + str(vp))
    print("ARR: " + str(arr))
    print("SLL: " + str(sll))
    print("SSAL: " + str(ssal))
    print("STO: " + str(sto))
    print("STA: " + str(sta))
    print("Puesto Actual: " + str(puestoActual))

    print("ITO: ")
    print(ito)
    
    print("--------FIN ESTADO--------")
    print("")
    return 1

def main():
    system("cls")
    print("Comienzo de la simulación")
    print("")
    
    #Seteo el seed para el random del arrepentimiento
    seed(1)
    
    variablesDeControl()
    
    while(t < tf):  
        #imprimirEstado()
        print("ARRANCA VUELTA - t: " + str(t))
        print("NS: " + str(ns))
        proxEvent = proximoEvento()
        manejoProximoEvento(proxEvent)
        print("TERMINA VUELTA - t: " + str(t))
        print("NS: " + str(ns))
        for i in range(0,cc):
            print("TPS" + str(i) + ": " + str(tps[i]))
        print("")
        print("------------------------------------------")
        print("")
    
    vaciamiento()
    calculoDeResultados()
    impresionDeResultados()
    print("Finalización de la simulación")
 
if __name__ == "__main__":
    main()