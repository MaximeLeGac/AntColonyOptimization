import csv
import networkx as nx
import matplotlib.pyplot as plt
import random


#################################################################################################################################
def init():
    streets_graph = nx.Graph()

    parse_streets_data(streets_graph)

    starting_street = "SAUTRON Rue de la Futaie"
    ending_street = "SAUTRON Rue de la Bretonnière"

    #starting_street = "SAUTRON Rue des Tisserands"
    #ending_street = "SAUTRON Allée des Bleuets"

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

        if len(nodes_visited) == 5:
            current_intersection = ending_street


    print("ENDING AT : "+current_intersection)
    print("------------------------------------------------------------------------------------------------")

    print(best_way)


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
            current_intersection = neighbor
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
    current_intersection = neighbors[next_node]

    return next_node, current_intersection


#################################################################################################################################
# Used to parse the streets datas from the csv file to a graph
def parse_streets_data(streets_graph):
    tab_graph = []
    inc_impasse = 0

    # 0 - BI_MIN
    # 1 - COMMUNE
    # 2 - STATUT
    # 3 - LIBELLE
    # 4 - BI_MAX
    # 5 - BP_MIN
    # 6 - MOT_DIRECTEUR
    # 7 - BP_MAX
    # 8 - TENANT
    # 9 - ABOUTISSANT
    # 10 - RIVOLI
    # 11 - CATEGORIE

    with open('VOIES_NM.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row_split = str(row).split(',')
            tab = []
            poids = 0

            for i in range(len(row_split)):
                tab.append(row_split[i].split(': ')[1].replace("'", ""))


            # and (tab[1] == "SAUTRON")
            if (tab != []) and (tab[1] == "SAUTRON"):
                tab_graph.append(tab)
                tenant = tab[8]
                aboutissant = tab[9]
                libelle = tab[3]
                bi_min = tab[0]
                bi_max = tab[4]
                bp_min = tab[5]
                bp_max = tab[7]

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
                streets_graph.add_edge(tenant, aboutissant, street=libelle, weight=(str(poids)), pheromon=0, score=1)

    '''myedges = streets_graph.edges()
                myedges.sort()
                print(myedges)'''

    #nx.draw(streets_graph)
    #plt.show()


# =============================================
# Evalue un chemin en fonction de sa longueur et du nombre de phéromone présent sur celui-ci
# path : Chemain à évaluer
def evaluate(street):
    # 50% basé sur la longueur de la rue
    # 50% basé sur le nombre de phéromone
    street['score'] = (int(street['weight'])*50) + (street['pheromon']*50)
    return street
# =============================================

# =============================================
# Renvoit la prochaine rue à emprunter (sélection par Wheel)
# streets : Liste des rues empruntables à l'étape suivante
def next(streets):
    sumScore = sum(int(street['score']) for street in streets)
    scoreArea = random.randint(1, int(sumScore * 100)) % sumScore
    tmpScore = 0
    for street in streets:
        streetScore = int(street['score'])
        if tmpScore <= scoreArea and scoreArea < tmpScore + streetScore:
            return street
        tmpScore += streetScore
# =============================================