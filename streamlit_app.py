
import numpy as np
import cvxpy as cp
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs

from sklearn.cluster import DBSCAN
from sklearn.neighbors import KNeighborsClassifier



#centros=np.random.normal(loc=0.0, scale=2.5, size=(10,2))

centros=np.array([[-1.03214567, -1.39927718],
       [-5.32720645, -0.06748737],
       [ 2.82421748, -5.91633287],
       [-4.59951274,  1.11133516],
       [-2.296698  ,  2.5331559 ],
       [ 0.76535303, -1.95176301],
       [ 2.71368711,  2.61737128],
       [-0.27428771,  3.47586674],
       [-2.41134015, -0.38274084],
       [-0.91147307,  1.60209808]])

X, labels_true = make_blobs(n_samples=600, centers=centros, cluster_std=0.5, random_state=120)

x_newc,labels_n= make_blobs(n_samples=80, centers=np.array([[-4.,-6.]]),cluster_std=0.25,random_state=120)

X_data_new=np.zeros((680,2))
X_data_new[0:600,:]=X
X_data_new[600:,:]=x_newc

#caminos=np.random.randint(0,2,size=(600,600))

def anadir_nuevos_clientes(X_clientes, X_nuevos_clientes, y_zona, y_hat_zona):
  cantidad_nuevos=X_nuevos_clientes.shape
  cantidad_clientes_actuales=X_clientes.shape
  if cantidad_clientes_actuales[1]==cantidad_nuevos[1]:
    nueva_data_clientes=np.zeros(shape=(cantidad_clientes_actuales[0]+cantidad_nuevos[0],cantidad_clientes_actuales[1]))
    nueva_data_clientes[0:cantidad_clientes_actuales[0],:]=X_clientes
    nueva_data_clientes[cantidad_clientes_actuales[0]:,:]=X_nuevos_clientes
    nueva_data_zonas=np.zeros(shape=(cantidad_clientes_actuales[0]+cantidad_nuevos[0],))
    nueva_data_zonas[0:cantidad_clientes_actuales[0]]=y_zona
    nueva_data_zonas[cantidad_clientes_actuales[0]:]=y_hat_zona
    return nueva_data_clientes, nueva_data_zonas
  else:
    print('error, revisar tamanos')

def definicion_zonas(X, eps, min_samples):
  db = DBSCAN(eps=eps, min_samples=min_samples, metric="euclidean").fit(X)
  X_clientes=X[db.labels_!=-1]
  y_zona=db.labels_[db.labels_!=-1]
  X_clientes_nuevos=X[db.labels_==-1]
  if np.unique(db.labels_).shape[0]>=3:
    model_clientes=KNeighborsClassifier(weights='distance',metric='euclidean').fit(X_clientes,y_zona)
    clientes_asignados=model_clientes.predict(X_clientes_nuevos)
    x_clientes,Y_zonas= anadir_nuevos_clientes(X_clientes, X_clientes_nuevos, y_zona, clientes_asignados)
    return x_clientes,Y_zonas
  else:
    return X, db.labels_


def distancia(x,y):
  return np.linalg.norm(x - y)

def matriz_distancias(X):
  dist=[]
  for i in range(len(X)):
    dist.append([distancia(X[i],X[j]) for j in range(len(X))])

  distancias=np.array(dist)
  return distancias


def centroides_simple(Y_zonas,x_clientes ):
  centroides=[]
  for i in np.unique(Y_zonas):
    centroides.append(np.median(x_clientes[Y_zonas==i], axis=0))
  centroides=np.array(centroides)
  return centroides

def matriz_con_centroides(distancias,label,centroides_id,centroides):
  distancias_0=distancias[label==centroides_id]
  centroides=centroides[centroides_id]
  clientes,coordenada=distancias_0.shape[0],distancias_0.shape[1]
  distancias_nuevo=np.zeros(shape=(clientes+1,coordenada))
  #Matriz Nueva
  distancias_nuevo[0]=centroides

  distancias_nuevo[1:clientes+1]=distancias_0
  return distancias_nuevo



plt.scatter(X[:,0], X[:,1])

plt.title('Mapa de clientes')

# Definamos las zonas
x_clientes,Y_zonas=definicion_zonas(X, 0.49,15)

plt.figure(figsize=(8,8))
for i in np.unique(Y_zonas):
  plt.scatter(x_clientes[:,0][Y_zonas==i], x_clientes[:,1][Y_zonas==i], label='Zona '+ str(int(i)+1)+' con '+ str(Y_zonas[Y_zonas==i].shape[0])+' clientes')
plt.title('Mapa de clientes')
plt.legend()

centroides=centroides_simple(Y_zonas,x_clientes)

plt.figure(figsize=(8,8))
for i in np.unique(Y_zonas):
  plt.scatter(x_clientes[:,0][Y_zonas==i], x_clientes[:,1][Y_zonas==i], label='Zona '+ str(int(i)+1))
plt.scatter(centroides[:,0],centroides[:,1], color='black')

for i in range(centroides.shape[0]):
  plt.annotate(str(i+1), (centroides[i,0]+0.1, centroides[i,1]+0.1))
plt.title('Mapa de clientes y sus Hubs')
plt.legend(loc='best')

definir_zonados, label_zonados=definicion_zonas(x_clientes[Y_zonas==2], 0.2,6)

plt.figure(figsize=(8,8))
for i in np.unique(label_zonados):
  plt.scatter(definir_zonados[:,0][label_zonados==i], definir_zonados[:,1][label_zonados==i], label='Zona '+ '2.'+str(int(i)+1)+' con '+ str(label_zonados[label_zonados==i].shape[0])+' clientes')
plt.scatter(centroides[2,0],centroides[2,1], color='black', label='Hub')
plt.title('Mapa de clientes Zona 2')
plt.legend()

plt.scatter(X[:,0], X[:,1], label="Antiguos Clientes")
plt.scatter(x_newc[:,0], x_newc[:,1], label="Zona Nueva")
plt.title('Mapa de clientes')
plt.legend()

x_clientes2,Y_zonas2=definicion_zonas(X_data_new,0.49,15)

plt.figure(figsize=(8,8))
for i in np.unique(Y_zonas2):
  plt.scatter(x_clientes2[:,0][Y_zonas2==i], x_clientes2[:,1][Y_zonas2==i], label='Zona '+ str(int(i)+1)+' con '+ str(Y_zonas2[Y_zonas2==i].shape[0])+' clientes')
plt.title('Mapa de clientes 2')
plt.legend()

distancias_centroides=matriz_distancias(centroides)


def ruteo_vendedores(ubicacion,centroides_id, centroides_cluster,velocidad, tiempo_por_cliente,hl):
  xn=ubicacion[centroides_cluster==centroides_id]
  cantidad_de_clientes=xn.shape[0]
  velocidad=velocidad
  tiempo_por_cliente=tiempo_por_cliente
  distancias_0=matriz_distancias(xn)*velocidad

  r=[]

  #Modelo
  x=cp.Variable(shape=(distancias_0.shape[0],distancias_0.shape[0]),boolean = True)
  #T=cp.Variable()
  objetivo=cp.Minimize(cp.sum(x)) #cp.sum(x)
  #Restricciones:

  for i in range(distancias_0.shape[0]):
    r.append(cp.sum([distancias_0[i,j]*x[i,j] for j in range(distancias_0.shape[0])] ) + cp.sum([tiempo_por_cliente*x[i,j] for j in range(distancias_0.shape[0])])<=hl)#*y[i,0]
    r.append(cp.sum(x[:,i])==1)
    #r.append(cp.sum(x[i,:])>=1-y[i,0])

  # for i in range(distancias_0.shape[0]):
  #   r.append(x[i,0]<=cp.sum([x[i,j] for j in range(distancias_0.shape[0])]))

  # solucion
  prob = cp.Problem(objetivo,r)
  solu=prob.solve(verbose=False)

  # variables
  rutas=np.array(x.value)
  vendedores=rutas#.max(axis=1).sum()
  #locacion=np.array(y.value)
  if(prob.status=='optimal'):
    return rutas, vendedores, cantidad_de_clientes, distancias_0#, locacion
  else:
    print('faliure')
    return np.nan, prob.status, np.nan, np.nan

def rutas_de_vendedores(rutas,distancias, cantidad_de_clientes):
  clientes=np.linspace(1,int(cantidad_de_clientes),int(cantidad_de_clientes)).astype(int)
  rutas_vendedores_bool=np.where(rutas[rutas.max(axis=1)>0]>0,True,False)
  lista_clientes=[]
  tiempos_est=[]
  for i,j in enumerate(rutas_vendedores_bool):
    lista_clientes.append(list(clientes[j]))
    tiempos_est.append(tiempo_estimado(clientes[j],distancias))
    print("vendedor",i+1 ,"cantidad de clientes", clientes[j].shape[0],"tiempo estimado",tiempo_estimado(clientes[j],distancias) , "ruta",clientes[j])
  return lista_clientes, tiempos_est

def tiempo_estimado(rutas_de_vendedor,distancias):
  y=0
  for i in range(len(rutas_de_vendedor)-1):
    y+=distancias[rutas_de_vendedor[i]-1,rutas_de_vendedor[i+1]-1]
  total=len(rutas_de_vendedor)*0.8+y
  return np.round(total,3)

def generador_label_ruta(rutas_de_vendedor):
  clientes_=''
  for i in rutas_de_vendedor:
    clientes_+='> '+str(i)
  return clientes_

def graficos_de_rutas(rutas,ubicacion,cluster, cluster_id, rutas_de_vendedor):
  Xn=ubicacion[cluster==cluster_id]
  bool_ruta=np.where(rutas[rutas.max(axis=1)>0]>0,True,False)
  plt.figure(figsize=(10,10))
  for i in range(bool_ruta.shape[0]):
    pl=Xn[bool_ruta[i]]
    plt.plot(pl[:,0],pl[:,1], label='vendedor '+str(i+1), marker='X')#generador_label_ruta(rutas_de_vendedor[i])
  plt.legend()


rutas,vendedores,cantidad_de_clientes, distancias=ruteo_vendedores(x_clientes,2,Y_zonas,1/15, 0.8,8) #locacion

rutas_de_vendedor, tiempos_recorrido=rutas_de_vendedores(rutas,distancias, cantidad_de_clientes)

list(np.random.choice(rutas_de_vendedor[0], size=9,replace=True))

tiempo_estimado(rutas_de_vendedor[11],distancias)

rutas_de_vendedor[0]

tiempo_estimado([121,7,29,11,41,42,116,119,48,],distancias)

X_data=x_clientes[Y_zonas==2]
for i in [121,7,29,11,41,42,116,119,48]:
  plt.scatter(X_data[i-1,0],X_data[i-1,1], label=str(i))
  #plt.annotate(str(i), (X_data[i-1,0]+0.1, X_data[i-1,0]+0.1))
plt.legend()



tiempo_estimado(list(np.random.choice(rutas_de_vendedor[6], size=9,replace=True)),distancias)

graficos_de_rutas(rutas,x_clientes,Y_zonas, 2, rutas_de_vendedor)
plt.scatter(centroides[2,0],centroides[2,1], color='black', label='Hub')

ventas=np.random.randint(500,5000 ,size=(122,7))


rutas_dos_cero,vendedores_dos_cero,cantidad_de_clientes_dos_cero, distancias_dos_cero=ruteo_vendedores(definir_zonados,0,label_zonados,1/15, 0.8,8) #locacion
rutas_de_vendedor_dos_cero, tiempos_recorrido_dos_cero=rutas_de_vendedores(rutas_dos_cero,distancias_dos_cero, cantidad_de_clientes_dos_cero)

graficos_de_rutas(rutas_dos_cero,definir_zonados,label_zonados, 0, rutas_de_vendedor_dos_cero)

rutas,vendedores,cantidad_de_clientes, distancias=ruteo_vendedores(definir_zonados,1,label_zonados,1/15, 0.8,8) #locacion
rutas_de_vendedor, tiempos_recorrido=rutas_de_vendedores(rutas,distancias, cantidad_de_clientes)

rutas,vendedores,cantidad_de_clientes, distancias=ruteo_vendedores(definir_zonados,2,label_zonados,1/15, 0.8,8) #locacion
rutas_de_vendedor, tiempos_recorrido=rutas_de_vendedores(rutas,distancias, cantidad_de_clientes)



def agente_viajero_sencillo_n_vendedores(distancias,cantidad_vendedores,velocidad):
  tamano=distancias.shape[0]
  distancias=distancias*velocidad
  x=cp.Variable(shape=(tamano,tamano),boolean = True)
  #u = cp.Variable(tamano, integer=True)
  funcion_objetivo=cp.Minimize(cp.sum(cp.multiply(distancias,x)))#[x[i,j]*distancias[i,j] for i in range(tamano) for j in range(tamano)]
  restric=[]
  for i in range(1,tamano):
    restric.append(cp.sum(x[1:,i])==1)
    restric.append(cp.sum(x[i,1:])==1)
    #restric.append(cp.sum(x[i,:])==1)
    #restric.append(cp.sum(x[:,i])==cp.sum(x[i,:]))
    #restric.append(x[i,i]==0)
    for i in range(tamano):
      restric.append(x[i,i]==0)
    #Restriccion cantidad de vendedores sugerido
    restric.append(cp.sum(x[0,:])==cantidad_vendedores)
    restric.append(cp.sum(x[:,0])==cantidad_vendedores)
    # restric.append(u[1:] >= 2)
    # restric.append(u[1:] <= tamano)
    # restric.append(u[0] == 1)

    # for i in range(1, tamano):
    #   for j in range(1, tamano):
    #       if i != j:
    #           restric += [ u[i] - u[j] + 1  <= (tamano - 1) * (1 - x[i, j]) ]

  prob = cp.Problem(funcion_objetivo,restric)
  solu=prob.solve(verbose=False)
  resu=np.array(x.value)
  if(prob.status=='optimal'):
    return resu, solu
  else:
    print('faliure')
    np.nan, prob.status

vectores, rsolucion = agente_viajero_sencillo_n_vendedores(distancias_centroides, 2, 1/15)

vectores[1:,1:]


def modelo_asignacion_vendedores(cantidad_de_rutas, tiempo_disponible, demanda_por_periodo, costo_por_vendedor,vendedores, presupuesto_minimo ):

  x=cp.Variable(shape=(tiempo_disponible,cantidad_de_rutas),boolean = True)
  #R=cp.Variable(shape=(tiempo_disponible,cantidad_de_rutas),boolean = True)

  objetivo=cp.Maximize(cp.sum(cp.multiply(x,demanda_por_periodo))-cp.sum(costo_por_vendedor*x))

  r=[]
  for i in range(tiempo_disponible):
    #r.append(cp.sum(x[i,:])==cp.sum(R[i,:]))
    r.append(cp.sum(cp.multiply(x[i,:],demanda_por_periodo[i,:]))>=presupuesto_minimo) #presupuesto_minimo #cp.sum(presupuesto_minimo*x[i,:]
    r.append(cp.sum(x[i,:])<=vendedores)

  for i in range(cantidad_de_rutas):
    r.append(cp.sum(x[:,i])<=1)

  prob = cp.Problem(objetivo,r)
  solu=prob.solve(verbose=False)

  #R=np.array(R.value)
  x=np.array(x.value)

  return solu, x

ventas=np.random.randint(2000,5000,size=(20,))

tasa_desatencion=[1,0.79,0.75,0.5,0.45,0.35,0.2]

ventas_dia=np.zeros((7,20))

for i,j in enumerate(tasa_desatencion):
  ventas_dia[i]=ventas*j

obj=[]
cant_max=[]
clientes_visitados=[]
for i in range(1,15):
  opt,vend=modelo_asignacion_vendedores(20,7,ventas_dia, 1500,i,800)
  obj.append(opt)
  cant_max.append(vend.sum(axis=1).max())
  clientes_visitados.append(vend.sum())

plt.scatter(cant_max,clientes_visitados)
plt.xticks(np.arange(1, 20, step=1))
plt.grid()
plt.show()

plt.scatter(clientes_visitados,obj)
plt.xticks(np.arange(1, 21, step=1))
plt.grid()
plt.show()

