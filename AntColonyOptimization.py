import csv
import networkx as nx
import matplotlib.pyplot as plt


def init():
    streets_graph = nx.Graph()

    parse_streets_data(streets_graph)

    starting_street = "SAUTRON Rue de la Futaie"
    ending_street = "SAUTRON Rue de la Bretonnière"

    '''print(nx.all_neighbors(streets_graph, starting_street))
            
                for i in streets_graph.neighbors_iter(starting_street):
                    print(i)'''

    ant_launcher(streets_graph, starting_street, ending_street)




# 
def ant_launcher(streets_graph, starting_street, ending_street):
    nodes_visited = []
    best_way = []
    path_weight = 0

    current_intersection = starting_street

    while current_intersection != ending_street:

        print("NEIGHBOR = "+str(streets_graph.neighbors(current_intersection)))

        # first the ant has to choose the next node to visit
        neighbor_to_visit = choose_next_node(streets_graph, current_intersection, nodes_visited, best_way)

        #print(streets_graph.edges(current_intersection, data='street')[0])

        current_intersection = ending_street


    return 0

# 
def choose_next_node(streets_graph, current_intersection, nodes_visited, best_way):
    neighbors = []
    next_node = 0
'''
- elle ne peut visiter qu’une fois chaque ville ;
- plus une ville est loin, moins elle a de chance d’être choisie (c’est la « visibilité ») ;
- plus l'intensité de la piste de phéromone disposée sur l’arête entre deux villes est grande, plus le trajet aura de chance d’être choisi ;
- une fois son trajet terminé, la fourmi dépose, sur l’ensemble des arêtes parcourues, d’autant plus de phéromones que le trajet est court ;
- les pistes de phéromones s’évaporent à chaque itération
'''

    for neighbor in streets_graph.neighbors_iter(current_intersection):
        neighbors.append(neighbor)
        print(neighbor)



    return next_node

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
            if tab != []:
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
                streets_graph.add_edge(tenant, aboutissant, street=libelle, weight=(str(poids)), pheromon=0)


    '''myedges = streets_graph.edges()
                myedges.sort()
                print(myedges)'''

    #nx.draw(streets_graph)
    #plt.show()





