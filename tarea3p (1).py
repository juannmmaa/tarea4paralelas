"""
Tarea 4 Ayudantia Computación Paralela Segundo Semestre 2014

Integrantes : Jonathan León (johnnysavior)
              Juan Cortez (juannmmaa)
              Felipe Alvarez R. (fliseven)

Version Paralela de la tarea 3 del mismo ramo...

"""
from mpi4py import MPI
import time


comm = MPI.COMM_WORLD

rank =  comm.rank
size =  comm.size

if rank==0:
    starting_point=time.time()     
    
    archivo = open('matriz.txt', 'r')
    #leemos linea por linea y guardamos en una lista
    matriz=archivo.readlines()
    #eliminamos el "\n" de cada fila
    for indice in range(len(matriz)):
        matriz[indice]=matriz[indice][:-1]
    #separamos cada fila en los numeros  que trae separados por espacios
    for indice in range(len(matriz)):
        matriz[indice]=matriz[indice].split(" ")
    #ahora hay que transformar cada valor en un int, pues la matriz que obtenemos
    #es todo string de strings
    for indice_i in range(len(matriz)):
        for indice_j in range(len(matriz[indice_i])):
            matriz[indice_i][indice_j]=int(matriz[indice_i][indice_j])

    #definimos algunas cuantas variables necesarias para multiplicar el producto final
    mayor=-999999999
    producto=int()

    #definimos variables donde guardaremos los 4 numeros que generan la multiplicacion mas grande de la matriz
    a=int()
    b=int()
    c=int()
    d=int()

    comm.send (matriz, dest = 1)
    comm.send (matriz, dest = 2)
    #buscando la mayor multiplicacion de 4 numeros adjacentes de forma horizontal, tenemos algo asi.
    for i in range(len(matriz)):
        for j in range(len(matriz[i])-3):
            producto=matriz[i][j]*matriz[i][j+1]*matriz[i][j+2]*matriz[i][j+3]
            if producto>mayor:
                mayor=producto


    matriz.reverse()
    j=3
    for i in range(len(matriz)-3):
        for j in range(len(matriz)-3):
            producto=matriz[i][j]*matriz[i+1][j-1]*matriz[i+2][j-2]*matriz[i+3][j-3]
            if producto>mayor:
                mayor=producto


if rank==1:
    matriz_recibir = comm.recv(source=0)
    mayor=-99999999
    #ahora se repite el procedimiento de multiplicacion anterior pero ahora lo hacemos de arriba
    #hacia abajo con cada columna.
    for i in range(len(matriz_recibir)-3):
        for j in range(len(matriz_recibir[i])):
            producto=matriz_recibir[i][j]*matriz_recibir[i+1][j]*matriz_recibir[i+2][j]*matriz_recibir[i+3][j]
            if producto>mayor:
                mayor=producto


    comm.send(mayor, dest=0)

if rank==2:
    matriz_recibir = comm.recv(source=0)
    mayor=-999999
    #ahora se repite el procedimiento de multiplicacion anterior pero ahora lo hacemos en forma
    #diagonal de derecha a izquierda.

    for i in range(len(matriz_recibir)-3):
        for j in range(len(matriz_recibir)-3):
            producto=matriz_recibir[i][j]*matriz_recibir[i+1][j-1]*matriz_recibir[i+2][j-2]*matriz_recibir[i+3][j-3]
            if producto>mayor:
                mayor=producto

    comm.send(mayor, dest=0)

if rank==0:
    mayor_uno = comm.recv(source=1)
    mayor_dos = comm.recv(source=2)
    
    elapsed_time=time.time()-starting_point
    elapsed_time_int = float(elapsed_time)

    if mayor>mayor_uno and mayor>mayor_dos:
        print mayor
    elif mayor_uno>mayor and mayor_uno>mayor_dos:
        print mayor_uno
    else:
        print mayor_dos
        
    print "Time: ", elapsed_time 
        
        
