import sys
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from heapq import heappop, heappush


class Node:
    def __init__(self, vertex, weight=0):
        self.vertex = vertex
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight


class Graph:
    def __init__(self, edges, n):

        self.adjList = [[] for _ in range(n)]

        for (source, dest, weight) in edges:
            self.adjList[source].append((dest, weight))


def get_route(prev, i, route):
    if i >= 0:
        get_route(prev, prev[i], route)
        route.append(i)


def findShortestPaths(graph, source, n):

    pq = []
    heappush(pq, Node(source))

    dist = [sys.maxsize] * n

    dist[source] = 0

    done = [False] * n
    done[source] = True

    prev = [-1] * n

    while pq:

        node = heappop(pq)      
        u = node.vertex         

        for (v, weight) in graph.adjList[u]:
            if not done[v] and (dist[u] + weight) < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u
                heappush(pq, Node(v, dist[v]))

        done[u] = True

    route = []
    for i in range(n):
        if i != source and dist[i] != sys.maxsize:
            get_route(prev, i, route)
            print(
                f'Path ({source} —> {i}): Minimum cost = {dist[i]}, Route = {route}')
            route.clear()


def agregar_arista(G, u, v, w=1, di=True):
    G.add_edge(u, v, weight=w)
    if not di:
        G.add_edge(v, u, weight=w)


def draw_graph():
    G = nx.DiGraph()

    #index graph in agregar_arista with for loop 
    for i in range(len(edges)):
        agregar_arista(G, edges[i][0], edges[i][1], edges[i][2])
        
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, alpha=0.8,with_labels=True,node_color='skyblue',node_size=1200)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.show()

class StdOutRedirect:
    def __init__(self,  text: Text) -> None:
        self._text = text

    def write(self,  out: str) -> None:
        self._text.insert(END,  out)


class App(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent,  *args, **kwargs)
        self.stdout_text = Text(
            self,  bg="white",  fg="black",  font=("Helvetica", 15))
        self.stdout_text.pack(expand=True, fill=BOTH)
        sys.stdout = StdOutRedirect(self.stdout_text)

def ventan1():
    def getGrafo():
        grafo = Txtbox.get()
        arreglo = grafo.split(",")
        for i in range(len(arreglo)):
            arreglo[i] = int(arreglo[i])
        
        for i in range(0,len(arreglo),3):
            edges.append((arreglo[i],arreglo[i+1],arreglo[i+2]))
        
        App(ventana1).pack(expand=True, fill=BOTH)
        graph = Graph(edges, n)

        for source in range(n):
            findShortestPaths(graph, source, n)
        

    ventana1= Toplevel()
    ventana1.geometry("500x500")
    lbl_nodos = Label(ventana1, text="Ingresar rutas", font=("Arial", 15))
    lbl_nodos.pack()
    lbl_intro = Label(ventana1, text="Nodo inicio,Nodo final,Peso", font=("Arial", 9))
    lbl_ejemplo = Label(ventana1, text="ejemplo: 1,2,5", font=("Arial", 8))
    lbl_intro.pack()
    lbl_ejemplo.pack()
    Txtbox = Entry(ventana1, width=20)
    Txtbox.pack()
    btn_get = Button(ventana1, text="Ingresar", command=getGrafo)
    btn_get.pack()
    btn_graph = Button(ventana1, text="Graficar", command=draw_graph)
    btn_graph.pack()
    return 0

def ventan2():
    ventana2= Toplevel()
    ventana2.geometry("500x500")

    # generate graph with for loops and random weights
    
    for i in range(conect):
        edges.append((np.random.randint(0, n), np.random.randint(0, n), np.random.randint(1, 10)))

    btn_graph = Button(ventana2, text="Graficar", command=draw_graph)
    btn_graph.place(x=20,y=20)
    btn_graph.pack()
    App(ventana2).pack(expand=True, fill=BOTH)

    graph = Graph(edges, n)

    for source in range(n):
        findShortestPaths(graph, source, n)
    return 0

if __name__ == "__main__":
    n = 10
    conect = 9
    global edges
    edges = []
    root = Tk()
    root.title("Grafo")
    root.geometry("500x200")
    root.resizable(False, False)
    lbl_title = Label(root, text="Camino Minimo Dijkstra", font=("Arial", 20))
    lbl_title.pack()
    btn_graph = Button(root, text="Manual", command=ventan1)
    btn_graph.place(x=20,y=20)
    btn_graph.pack()
    btn_graph = Button(root, text="Automatico", command=ventan2)
    btn_graph.place(x=20,y=20)
    btn_graph.pack()
    root.mainloop()