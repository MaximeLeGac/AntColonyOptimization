import csv
import networkx as nx
import matplotlib.pyplot as plt
import random

NB_ANTS = 200

#################################################################################################################################
def init():
    streets_graph = nx.Graph()
    best_way = []
    best_weight = 0
    path_found_by_ant = []

    parse_streets_data(streets_graph)

    starting_street = "ORVAULT Chemin de la Grande Borne"
    ending_street = "SAUTRON Rue du Doussais"

    for i in range(NB_ANTS):
        path_found_by_ant = ant_launcher(streets_graph, starting_street, ending_street)

        sum_weight = calculate_weight(streets_graph, path_found_by_ant)

        # if a shorter path has been found or it's the first path found
        if (sum_weight < best_weight) or (best_weight == 0):
            print("BEST WEIGHT = "+str(best_weight))
            print("SUM WEIGHT  = "+str(sum_weight))
            print("PATH FOUND  = "+str(path_found_by_ant))
            best_weight = sum_weight
            best_way = path_found_by_ant

    print("\n\nBest path found by the ants : "+str(best_way))
    print("Weight of the best path : "+str(best_weight))



#################################################################################################################################
# 
def ant_launcher(streets_graph, starting_street, ending_street):
    nodes_visited = []
    path_found = []
    path_weight = 0

    nodes_visited.append(starting_street)
    path_found.append(starting_street)

    current_intersection = starting_street
    '''print("------------------------------------------------------------------------------------------------")
                print("STARTING AT : "+starting_street+" ==> GOING TO : "+ending_street)
                print("------------------------------------------------------------------------------------------------")'''

    while current_intersection != ending_street:

        # first the ant has to choose the next node to visit
        current_intersection = choose_next_node(streets_graph, current_intersection, nodes_visited, path_found)

        nodes_visited.append(current_intersection)
        path_found.append(current_intersection)

        '''print("GO TO : "+current_intersection)
                                print("------------------------------------------------------------------------------------------------")'''

    '''print("ENDING AT : "+current_intersection)
                print("------------------------------------------------------------------------------------------------")
            
                print("PATH FOUND = "+str(path_found))'''

    return path_found


#################################################################################################################################
# Return an integer which is the index of the next node the ant will visit
def choose_next_node(streets_graph, current_intersection, nodes_visited, path_found):
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
        if neighbor not in nodes_visited:
            neighbors.append(neighbor)

    # If the ant hasn't find any unvisited neighbor
    # The ant go backward until it finds a neighbor it hasn't visited
    while neighbors == []:
        path_found.remove(current_intersection)
        current_intersection = path_found[len(path_found)-1]
        #print("BACKWARD TO : "+current_intersection)
        nodes_visited.append(current_intersection)

        # Iteration on the neighbors to find the ones that haven't been visited
        for neighbor in streets_graph.neighbors_iter(current_intersection):
            if neighbor not in nodes_visited:
                neighbors.append(neighbor)

    next_node = random.randint(0, (len(neighbors)-1))

    # 5% de chances de prendre le prochain noeud en random
    if (random.randint(0, 100) < 5):
        current_intersection = neighbors[next_node]
    else:
        # sinon on évalue les possibilités puis choix du prochain noeud par Wheel Selection
        current_intersection = next(streets_graph, current_intersection, neighbors)

    return current_intersection

#################################################################################################################################
# Used to calculate the sum of weights on a path
def calculate_weight(streets_graph, tab_streets):
    sum_weight = 0
    first_node = tab_streets[0]

    #for new_street in tab_streets:
    for i in range(1, len(tab_streets)):
        second_node = tab_streets[i]
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