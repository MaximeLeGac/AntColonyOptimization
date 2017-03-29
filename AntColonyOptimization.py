import csv
import networkx as nx
import matplotlib.pyplot as plt
import random


#################################################################################################################################
def init():
    streets_graph = nx.Graph()

    parse_streets_data(streets_graph)

    '''starting_street = "SAUTRON Chemin de la Hubonnière"
                ending_street = "Rue des Lauriers"'''

    starting_street = "ORVAULT Chemin de la Grande Borne"
    ending_street = "SAUTRON Rue du Doussais"

    ant_launcher(streets_graph, starting_street, ending_street)


#################################################################################################################################
# 
def ant_launcher(streets_graph, starting_street, ending_street):
    nodes_visited = []
    best_way = []
    path_weight = 0

    nodes_visited.append(starting_street)
    best_way.append(starting_street)

    current_intersection = starting_street
    print("------------------------------------------------------------------------------------------------")
    print("STARTING AT : "+starting_street+" ==> GOING TO : "+ending_street)
    print("------------------------------------------------------------------------------------------------")

    while current_intersection != ending_street:

        #print("NEIGHBOR = "+str(streets_graph.neighbors(current_intersection)))
        # first the ant has to choose the next node to visit
        neighbor_to_visit, current_intersection = choose_next_node(streets_graph, current_intersection, nodes_visited, best_way)

        #print("current_intersection : "+current_intersection)
        #print("neighbor_to_visit : "+str(neighbor_to_visit))
        #print(streets_graph.edges(current_intersection, data='street'))
        #print("=========================================>"+streets_graph.edges(current_intersection, data='street')[neighbor_to_visit][1])

        #current_intersection = streets_graph.edges(current_intersection, data='street')[neighbor_to_visit][1]
        nodes_visited.append(current_intersection)
        best_way.append(current_intersection)

        print("GO TO : "+current_intersection)
        print("------------------------------------------------------------------------------------------------")

        '''if len(nodes_visited) == 10:
                                    current_intersection = ending_street'''


    print("ENDING AT : "+current_intersection)
    print("------------------------------------------------------------------------------------------------")

    print("BEST WAY = "+str(best_way)+"\n\n")

    sum_weight = calculate_weight(streets_graph, best_way)
    print("SUM WEIGHT = "+str(sum_weight))


#################################################################################################################################
# Return an integer which is the index of the next node the ant will visit
def choose_next_node(streets_graph, current_intersection, nodes_visited, best_way):
    neighbors = []
    next_node = 0
    index = 0
    next_node = -1

    '''
    - elle ne peut visiter qu’une fois chaque ville ;
    - plus une ville est loin, moins elle a de chance d’être choisie (c’est la « visibilité ») ;
    - plus l'intensité de la piste de phéromone disposée sur l’arête entre deux villes est grande, plus le trajet aura de chance d’être choisi ;
    - une fois son trajet terminé, la fourmi dépose, sur l’ensemble des arêtes parcourues, d’autant plus de phéromones que le trajet est court ;
    - les pistes de phéromones s’évaporent à chaque itération
    '''

    # Iteration on the neighbors to find the ones that haven't been visited
    for neighbor in streets_graph.neighbors_iter(current_intersection):
        #print("nodes_visited : "+str(nodes_visited))
        if neighbor not in nodes_visited:
            neighbors.append(neighbor)
            #current_intersection = neighbor
            #print(neighbor)

    # If the ant hasn't find any unvisited neighbor
    # The ant go backward until it finds a neighbor it hasn't visited
    while neighbors == []:
        best_way.remove(current_intersection)
        current_intersection = best_way[len(best_way)-1]
        print("BACKWARD TO : "+current_intersection)
        nodes_visited.append(current_intersection)

        # Iteration on the neighbors to find the ones that haven't been visited
        for neighbor in streets_graph.neighbors_iter(current_intersection):
            #print("nodes_visited 2 : "+str(nodes_visited))
            if neighbor not in nodes_visited:
                neighbors.append(neighbor)
                #print("Dat voisin : "+neighbor)

    next_node = random.randint(0, (len(neighbors)-1))

    # 5% de chances de prendre le prochain noeud en random
    if (random.randint(0, 100) < 5):
        current_intersection = neighbors[next_node]
    else:
        # sinon on évalue les possibilités puis choix du prochain noeud par Wheel Selection
        current_intersection = next(streets_graph, current_intersection, neighbors)

    return next_node, current_intersection

#################################################################################################################################
# Used to calculate the sum of weights on a path
def calculate_weight(streets_graph, tab_streets):
    sum_weight = 0
    first_node = tab_streets[0]

    #for new_street in tab_streets:
    for i in range(1, len(tab_streets)):
        second_node = tab_streets[i]
        print(first_node)
        print(second_node)
        print("weight : "+str(streets_graph[first_node][second_node]['weight']))
        sum_weight += streets_graph[first_node][second_node]['weight']
        first_node = second_node
    
    return sum_weight

#################################################################################################################################
# Used to parse the streets datas from the csv file to a graph
def parse_streets_data(streets_graph):
    tab_graph = []
    inc_impasse = 0

    # 0 - CATEGORIE
    # 1 - LIBELLE
    # 2 - MOT_DIRECTEUR
    # 3 - STATUT
    # 4 - COMMUNE
    # 5 - RIVOLI
    # 6 - TENANT
    # 7 - ABOUTISSANT
    # 8 - BI_MIN
    # 9 - BP_MIN
    # 10 - BI_MAX
    # 11 - BP_MAX

    with open('VOIES_NM.csv', 'r', newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(csv.reader(csvfile)):
            
            if index != 0:

                if (row != []) and (row[4] == "SAUTRON"):
                    tenant = row[6]
                    aboutissant = row[7]
                    libelle = row[1]
                    bi_min = row[8]
                    bi_max = row[10]
                    bp_min = row[9]
                    bp_max = row[11]

                    if tenant == "":
                        tenant = str(inc_impasse)
                        inc_impasse += 1

                    if aboutissant == "":
                        aboutissant = str(inc_impasse)
                        inc_impasse += 1

                    if tenant == 'Impasse':
                        tenant = libelle

                    if aboutissant == 'Impasse':
                        aboutissant = libelle

                    if tenant == aboutissant:
                        tenant = libelle

                    if bi_min != "":
                        poids = int(bi_max)-int(bi_min)
                    elif bp_min != "":
                        poids = int(bp_max)-int(bp_min)

                    if poids == 0:
                        poids = 1

                    '''print("===========================================================")
                                                                    print("LIBELLE      = "+str(libelle))
                                                                    print("TENANT       = "+str(tenant))
                                                                    print("ABOUTISSANT  = "+str(aboutissant))
                                                                    print("POIDS        = "+str(poids))'''
                    streets_graph.add_edge(tenant, aboutissant, street=libelle, weight=(poids), pheromon=0, score=1)

    #nx.draw(streets_graph)
    #plt.show()


# =============================================
# Evalue un chemin en fonction de sa longueur et du nombre de phéromone présent sur celui-ci
# streets : Liste des rues à évaluer
def evaluate(streets_graph, current_intersection, streets):
    for street in streets:
        # 50% basé sur la longueur de la rue
        # 50% basé sur le nombre de phéromone
        print("current_intersection = "+current_intersection)
        print("street = "+street)
        streets_graph[current_intersection][street]['score'] = (streets_graph[current_intersection][street]['weight']*50)+(streets_graph[current_intersection][street]['pheromon']*50)
    return streets
# =============================================

# =============================================
# Renvoit la prochaine rue à emprunter (sélection par Wheel)
# streets : Liste des rues empruntables à l'étape suivante
def next(streets_graph, current_intersection, streets):
    evaluate(streets_graph, current_intersection, streets)
    sumScore = sum(int(streets_graph[current_intersection][street]['score']) for street in streets)
    scoreArea = random.randint(1, int(sumScore * 100)) % sumScore
    tmpScore = 0
    for street in streets:
        streetScore = int(streets_graph[current_intersection][street]['score'])
        if tmpScore <= scoreArea and scoreArea < tmpScore + streetScore:
            return street
        tmpScore += streetScore
# =============================================