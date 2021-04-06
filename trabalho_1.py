from random import randint
import itertools
import random
from shapely.geometry import Point, LineString
import math
from matplotlib import pyplot as plt
import copy
import numpy as np

# imprime array de objetos


def _print(list_, title_):
    if list_[0][0].x == None:
        print("Erro: input não é uma lista")
        return

    print("[", end=" ")
    for p in list_:
        print("[(", p[0].x, ",", p[0].y, "),(", p[1].x, ",", p[1].y, ")]", end=" ")
    print("]")

    fig, ax = plt.subplots()
    for p in list_:
        x = [p[0].x, p[1].x]
        y = [p[0].y, p[1].y]

        plt.plot(x, y, marker='.', markersize=10, color='#6699cc', alpha=0.7,
                 linewidth=3, solid_capstyle='round', zorder=2)
    plt.title(title_)

    _file = title_ + ".jpg"
    plt.savefig(_file)

# define as arestas


def setPath(_list):
    _in = copy.deepcopy(_list)
    l_out = []
    for i in range(len(_in)):
        if i == len(_in) - 1:
            l_out.append([_in[i], _in[0]])
        else:
            l_out.append([_in[i], _in[i+1]])
    return l_out


def permuteResult(_list):
    _out = copy.deepcopy(_list)
    random.shuffle(_out)
    return _out


def permutationsList(_list):
    _out = list(itertools.permutations(_list))   
    return _out


# verifica se uma lista contem uma linha


def containsLine(input_line, input_list):
    rev_line = [input_line[1], input_line[0]]
    if input_line in input_list or rev_line in input_list:
        return True
    else:
        return False

# funcao para gerar lista de coordenadas aleatorias no plano


def generate_random(n, m):
    points = []
    while len(points) < n:
        coord = Point(randint(-m, m), randint(-m, m))
        if not coord in points:
            points.append(coord)

    return points

# funcao para encontrar distancia entre dois pontos


def findDist(pi, pf):
    a = (pf.x - pi.x) * (pf.x - pi.x) + (pf.y - pi.y) * (pf.y - pi.y)
    return a

# encontra e retorna lista com distancia entre o no n e os outros nos da lista
# util para quando o no mais proximo não servir, verificamos se o segundo mais proximo
# serve, e etc
# index 0 é o proprio elemento, 1 é o mais proximo, 2 é o segundo mais proximo, ...


def findNearest(n, listN):
    p_res = []
    for x in listN:
        p_res.append({'Point': x, 'dist': findDist(n, x)})

    # organiza a lista em ordem de distancia do elemento central
    def myFunc(e):
        return e['dist']

    p_res.sort(key=myFunc)

    return p_res

# verificar se há intersecção entre dois segmentos de linha
# linha 1 formada pelos pontos p1 e p2
# linha 2 formada pelos pontos p3 e p4
# retorna false se não encontrar interseccao ou o ponto de interseccao caso encontre


def findIntersec(p1, p2, p3, p4):
    line1 = LineString([p1, p2])
    line2 = LineString([p3, p4])
    inters = line1.intersection(line2)
    #intersec_point = inters.x, inters.y

    if inters:
        return inters  # intersec_point para imprimir (x,y) ao invés de objeto
    else:
        return False

# encontrar todos os pares que se intersectam


def findAllIntersec(index, _listOfLines):
    inters_list = []
    for y in range(len(_listOfLines)):
        # condicionais para eliminar casos em q a reta 1 é igual a reta 2, ou quando as duas
        # retas tem 1 ponto em comum
        if _listOfLines[index][0] != _listOfLines[y][0] and _listOfLines[index][0] != _listOfLines[y][1] and _listOfLines[index][1] != _listOfLines[y][0] and _listOfLines[index][1] != _listOfLines[y][1]:
            v = findIntersec(_listOfLines[index][0], _listOfLines[index][1],
                             _listOfLines[y][0], _listOfLines[y][1])
            if v != False:
                inters_list.append(y)

    # devolve uma lista que informa o index dos pontos que formam todas as linhas
    # que intersectam _line
    return inters_list

# devolve lista com index das arestas q se intersectam

def intersecList(edges):
    intersections = []
    for i in range(len(edges)):  
        for j in findAllIntersec(i, edges):
            if [i, j] not in intersections and [j, i] not in intersections:
                intersections.append([i, j])
    return intersections


# troca arestas


def two_ex(index1, index2, edges):
    new_edges = copy.deepcopy(edges)
    new_edges[index1][1] = edges[index2][0]
    new_edges[index2][0] = edges[index1][1]

    return new_edges

# devolve o melhor poligono com 1 troca 2ex baseada na menor distancia


def teShortestPath(points):
    edges = setPath(points)
    intersections = intersecList(edges)

    _min_path = copy.deepcopy(edges)
    _min = pathLength(_min_path)
    for i in range(len(intersections)):
        cur_path = two_ex(intersections[i][0], intersections[i][1], edges)
        if pathLength(cur_path) < _min:
            _min_path = copy.deepcopy(cur_path)
            _min = pathLength(cur_path)
    return _min_path

# devolve o melhor poligono com 1 troca 2ex baseada no primeiro conflito encontrado

def teFirst(points):
    edges = setPath(points)
    intersections = intersecList(edges)
    cur_path = edges
    if len(intersections) > 0:
        cur_path = two_ex(intersections[0][0], intersections[0][1], edges)
    
    return cur_path

# devolve o melhor poligono com 1 troca 2ex baseada no menor numero de conflitos


def teCrossEdges(points):
    edges = setPath(points)
    intersections = intersecList(edges)

    _min_path = copy.deepcopy(edges)
    _min = len(intersections)
    for i in range(len(intersections)):
        cur_path = two_ex(intersections[i][0], intersections[i][1], edges)
        new_intersec = intersecList(cur_path)
        if len(new_intersec) < _min:
            _min_path = copy.deepcopy(cur_path)
            _min = len(new_intersec)
    return _min_path

# devolve o melhor poligono com 1 troca 2ex baseada em um conflito aleatório encontrado

def teRandom(points):
    edges = setPath(points)
    intersections = intersecList(edges)
    cur_path = edges
    if len(intersections) > 0:
        i = random.randint(0,len(intersections)-1)
        cur_path = two_ex(intersections[i][0], intersections[i][1], edges)
    
    return cur_path

def hillClimbing(best, neighbours, flag):
    visited = []
    visited.append(best)
    next_length = 100000
    prev_length = 100000
    if flag == 1:
        cur_path = teShortestPath(neighbours[best])
        min_dist = pathLength(cur_path)
        for i in range(len(neighbours)):
            if best+1 < len(neighbours) and best+1 not in visited:
                next_path = teShortestPath(neighbours[best+1])
                next_length = pathLength(next_path)
                visited.append(best+1)
            if best-1 > 0 and best-1 not in visited:
                prev_path = teShortestPath(neighbours[best-1])
                prev_length = pathLength(prev_path)
                visited.append(best-1)
            if next_path and next_length <= min_dist and next_length <= prev_length:
                cur_path = next_path
                min_dist = next_length
                best += 1
            if prev_path and prev_length <= min_dist and prev_length < next_length:
                cur_path = prev_path
                min_dist = prev_length
                best -= 1
            if min_dist < next_length and min_dist < prev_length:
                print(i)
                break

    elif flag == 2:
        cur_path = teFirst(neighbours[best])
        min_dist = pathLength(cur_path)
        for i in range(len(neighbours)):
            if best+1 < len(neighbours) and best+1 not in visited:
                next_path = teFirst(neighbours[best+1])
                next_length = pathLength(next_path)
                visited.append(best+1)
            if best-1 > 0 and best-1 not in visited:
                prev_path = teFirst(neighbours[best-1])
                prev_length = pathLength(prev_path)
                visited.append(best-1)
            if next_path and next_length <= min_dist and next_length <= prev_length:
                cur_path = next_path
                min_dist = next_length
                best += 1
            if prev_path and prev_length <= min_dist and prev_length < next_length:
                cur_path = prev_path
                min_dist = prev_length
                best -= 1
            if min_dist < next_length and min_dist < prev_length:
                print(i)
                break

    elif flag == 3:
        cur_path = teCrossEdges(neighbours[best])
        min_dist = len(intersecList(cur_path))
        for i in range(len(neighbours)):
            if best+1 < len(neighbours) and best+1 not in visited:
                next_path = teCrossEdges(neighbours[best+1])
                next_length = len(intersecList(next_path))
                visited.append(best+1)
            if best-1 > 0 and best-1 not in visited:
                prev_path = teCrossEdges(neighbours[best-1])
                prev_length = len(intersecList(prev_path))
                visited.append(best-1)
            if next_path and next_length <= min_dist and next_length <= prev_length:
                cur_path = next_path
                min_dist = next_length
                best += 1
            if prev_path and prev_length <= min_dist and prev_length < next_length:
                cur_path = prev_path
                min_dist = prev_length
                best -= 1
            if min_dist < next_length and min_dist < prev_length:
                print(i)
                break

    elif flag == 4:
        cur_path = teRandom(neighbours[best])
        min_dist = pathLength(cur_path)
        for i in range(len(neighbours)):
            if best+1 < len(neighbours) and best+1 not in visited:
                next_path = teRandom(neighbours[best+1])
                next_length = pathLength(next_path)
                visited.append(best+1)
            if best-1 > 0 and best-1 not in visited:
                prev_path = teRandom(neighbours[best-1])
                prev_length = pathLength(prev_path)
                visited.append(best-1)
            if next_path and next_length <= min_dist and next_length <= prev_length:
                cur_path = next_path
                min_dist = next_length
                best += 1
            if prev_path and prev_length <= min_dist and prev_length < next_length:
                cur_path = prev_path
                min_dist = prev_length
                best -= 1
            if min_dist < next_length and min_dist < prev_length:
                print(i)
                break
    else:
        return None

    return cur_path

#simulated annealing
def simulatedAnnealing(best, neighbours):
    best_path = teCrossEdges(neighbours[best])
    best_length = len(intersecList(best_path))

    curr, curr_path, curr_length = best, best_path, best_length

    for i in range(5000):
        if best_length == 0:
            break

        candidate = randint(curr, len(neighbours)-1)

        candidate_path = teCrossEdges(neighbours[candidate])
        candidate_length = len(intersecList(candidate_path))

        if candidate_length < best_length:
            best_path, best_length = candidate_path, candidate_length
        
        diff = candidate_length - curr_length
        t = 5000/float(i+1)
        ex = math.exp(-diff/t)

        if diff < 0 or np.random.rand() < ex:
            curr, curr_path, curr_length = candidate, candidate_path, candidate_length
    
    return best_path


# acha tamanho da lista de arestas
def pathLength(li):
    i = 0
    _size = 0
    while i < len(li):
        _size = _size + findDist(li[i][0], li[i][1])
        i += 1
    return _size

# cria caminho com preferencia aos pontos mais proximos
# primeira posicao do array contem tamanho total do caminho,
# demais contem o caminho ordenado


def pathByProx(n, li):
    _list = li.copy()
    _out = []
    _out.append(0)
    elem = n
    _out.append(elem)
    while len(_list) > 0:
        _list.remove(elem)
        if len(_list) > 1:
            _p = findNearest(elem, _list)[0]
            _out.append(_p["Point"])
            _out[0] = _out[0] + _p["dist"]
            elem = _p["Point"]
        else:
            _out.append(_list[0])
            _out[0] = _out[0] + \
                findDist(elem, _list[0]) + findDist(_list[0], n)
            break
    return _out


print("Deseja obter pontos aleatorios (1) ou quer adiciona-los manualmente (2)?")
c = int(input("Digite a opção (1 ou 2): "))
opt = True

if c == 1:
    n = int(input("Entre o numero de pontos que deseja gerar: "))
    m = int(input("entre o limite do espaço em que esses pontos devem ser gerados: "))
# Q1)
    # gera aleatoriamente n elementos delimitados de -m a m nos eixos x e y
    result = generate_random(n, m)

elif c == 2:
    result = []
    n = int(input("Entre o numero de pontos que deseja gerar: "))
    while n <= 0:
        n = int(input("O numero de pontos deve ser maior que 0, digite novamente: "))
    while n > 0:
        cx = int(input("Digite a coordenada x: "))
        cy = int(input("Digite a coordenada y: "))
        result.append(Point(cx, cy))
        n = n-1
else:
    opt = False

if opt == True:
    # Q1)
    print("Q1: numeros gerados")
    _print(setPath(result), "Q1")
    print("---------------")

# Q2a)
    # gera um resultado aleatorio a partir de uma permutacao
    permut_result = permuteResult(result)
    print("Q2: a)")
    _print(setPath(permut_result), "Q2 a)")
    print("---------------")

# Q2b)
    # pega elemento aleatorio da lista
    first = random.choice(result)
    print("Q2: b)")
    seq_prox = pathByProx(first, result)
    _size = seq_prox.pop(-len(seq_prox))
    print("Tamanho do caminho: ", math.sqrt(_size))
    _print(setPath(seq_prox), "Q2 b)")
    print("---------------")

# Q3)
    print("Q3:")
    _3 = result.copy()
    _3path = setPath(_3)
    _3inters = []
    for i in range(len(_3path)):
        for j in findAllIntersec(i, _3path):
            if [i, j] not in _3inters and [j, i] not in _3inters:
                _3inters.append([i, j])
    if len(_3inters) > 0:
        _print(two_ex(_3inters[0][0], _3inters[0][1], _3path), "Q3")
    else:
        _print(_3path, "Q3")

### Q4 e Q5
# lista com todas as permutacoes possiveis dos pontos gerados
    neighbours = permutationsList(result.copy())    
    best = randint(0, len(neighbours)-1)
# Q4a)
    # melhor caminho base no tamanho do poligono
    print("Q4: a)")
    _print(hillClimbing(best, neighbours, 1), "Q4 a)")
# Q4b)
    # melhor caminho base no candidato seguinte
    print("Q4: b)")
    _print(hillClimbing(best, neighbours, 2), "Q4 b)")
# Q4c)
    # melhor caminho base no menor cruzamento de arestas
    print("Q4: c)")
    _print(hillClimbing(best, neighbours, 3), "Q4 c)")
# Q4d)
    # melhor caminho base num aleatorio
    print("Q4: d)")
    _print(hillClimbing(best, neighbours, 4), "Q4 d)")

#Q5)
    # simulated anneling
    print("Q5:")
    _print(simulatedAnnealing(best, neighbours), "Q5")

else:
    print("Valor invalido, programa será encerrado")
