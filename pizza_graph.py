class PizzaWanter:
    def __init__(self, name, wanted_pizzas):
        self.name = name
        self.wanted_pizzas = wanted_pizzas
        self.connections = []
        self.match = None

    def __str__(self):
        return "PizzaWanter: " + self.name

    def __repr__(self):
        return "PizzaWanter: " + self.name

    def get_connection_names(self):
        return ",".join([str(elem.name) for elem in self.connections])

    def get_match_name(self):
        if (self.match):
            return (self.match.name)
        else:
            return "No matches"
                                          
    # "wanted pizzas= " + ",".join([str(elem) for elem in self.wanted_pizzas]) \
    # + "\n" + "connections= " + ",".join([str(elem.name) for elem in self.connections]) \
    # + "\n" + "confirmed_match=" + (self.match or "No match")


riaz = PizzaWanter("riaz", {"mozarella", "funghi"})
scott = PizzaWanter("scott", {"aubergine"})
joulia = PizzaWanter("joulia", {"aubergine"})
artemis = PizzaWanter("artemis", {"mozarella", "courgette", "onion"})
rachel = PizzaWanter("rachel", {"courgette"})
monkey = PizzaWanter("monkey", {"funghi"})
tort = PizzaWanter("tort", {"onion", "cabbage"})
chicken = PizzaWanter("chicken", {"cabbage"})
edgar = PizzaWanter("edgar", {"mozarella"})
weirdo = PizzaWanter("weirdo", {"pine apple"})
oddboi = PizzaWanter("oddBoi", {"mozarella", "funghi", "courgette", "onion", "cabbage"})


#Create an adjacency matrix of pizza wanters
def create_graph(pizzaWanters):
    # check we have even number of wanters first
    if len(pizzaWanters)%2 != 0:
        print("error not equal number of pizza ppl, this graph will never match")
        
    pizza_graph = {}
    for wanter in pizzaWanters:
        pizza_graph[wanter.name] = set()
        for sharer in pizzaWanters:
            if sharer != wanter:
                if wanter.wanted_pizzas & sharer.wanted_pizzas:
                    pizza_graph[wanter.name].add(sharer.name)
                    wanter.connections.append(sharer.name)

    print("graph of wants:")
    for wanter in pizza_graph:
        print(wanter + "\t:" + str(pizza_graph[wanter]))
    return(pizza_graph)

# get a brute force matching
def brute_force(graph):
    matching = {}
    taken = set()
    for wanter in graph:
        if wanter not in taken:
            matching[wanter] = None
            for sharer in graph[wanter].difference(taken):
                    matching[wanter] = sharer
                    matching[sharer] = wanter
                    taken.add(sharer)
                    taken.add(wanter)
                    break
            
    print("initial matching:")
    for wanter in matching:
        print(wanter + "\t:" + str(matching[wanter]))
    return matching

def get_path(graph, matching_graph, path=[]):
    if path == []:
        for node in graph:
            print("No initial path, checking " + node)
            # Pick an initial node with no matches and find a connection
            if matching_graph[node] == None:
                print("using unmatched node " + node)
                path.append(node)
                break

    if path == []:
        print("No unmatched nodes, maximal matching created :) ")
        return None

    queue = [path]
    while queue:
        path = queue.pop(0)
        print("current path: " + str(path))
        initial_node = path[-1]
        for connected_node in graph[initial_node]:
            print("current node " + initial_node)
            print("Checking node " + connected_node)
            if connected_node in path:
                print("node already in path, ignore")
            elif matching_graph[connected_node] == None:
                    print("Found free node, connect and return path")
                    print((path) + [connected_node])
                    return path + [connected_node]
            elif matching_graph[connected_node] != None:
                    print("Matched node, connect with pair and continue search later")
                    pair = [connected_node, matching_graph[connected_node]]
                    queue.append(path + pair)
        print("Done searching from " + initial_node)
        print(path)

def augment_path(path, match_graph):
    for index,node in enumerate(path):
        if match_graph[node] == None:
            try:
                print("setting match to forward node")
                match_graph[node] = path[index+1]
            except IndexError:
                print("unable to set to forward node, must be last node")
                match_graph[node] = path[index-1]
        elif match_graph[node] == path[index+1]:
            match_graph[node] = path[index-1]
        elif match_graph[node] == path[index-1]:
            match_graph[node] = path[index+1]
    return match_graph
        
pizzaWanters = [riaz, rachel,  scott, joulia, artemis,
                     monkey, tort, chicken]

graph = create_graph(pizzaWanters)
#initial_matching = brute_force(graph)
initial_matching = {"riaz": "artemis",
                    "artemis": "riaz", 
                    "monkey"  : None,
                    "rachel"  : None,
                    "tort"    :"chicken",
                    "scott"   :"joulia",
                    "chicken" :"tort",
                    "joulia"  :"scott"}
print("gake initial matching")
for wanter in initial_matching:
    print(wanter + "\t:" + str(initial_matching[wanter]))

path = get_path(graph, initial_matching)
print("path is "+ str(path))



            

def get_augmenting_path(pizzaWanters):
    for wanter in pizzaWanters:
        print("Bulding path from " + str(wanter))
        if wanter.match is None:
            path = get_path(pizzaWanters, [wanter])
            if len(path) > 1:
                return path
    return None

def augmentingPath(want_graph, initial_match):
    for wanter in want_graph:
        if wanter not in initial_match.keys() \
           and wanter not in initial_match.values():
            path = getPath(want_graph, [wanter])
            if len(path) > 1:
                return path
    return None

def subtractAugmentingPath(want_graph, initial_match, augmenting_path):
    augmented_match = {}
    for share_pair in zip(augmenting_path, augmenting_path[1:]):
        wanter = share_pair[0]
        sharer = share_pair[1]
        if wanter in initial_match.keys():
            if initial_match[wanter] == sharer:
                print("Error, wanter - sharer path already exists", wanter, sharer)
        elif wanter in initial_match.values():
            for node in want_graph[wanter]:
                connection = initial_match.get(node)
                if connection == wanter:
                    initial_match.pop(node)
        else:
            augmented_match[wanter] = sharer

    initial_match.update(augmented_match)
    return initial_match

def subtract_augumenting_path(pizzaWanters, augmentingPath):
    while len(augmentingPath) > 1:
        node = augmentingPath.pop()
        if node.match == None:
            print("Inverting non match between " + str(node) + " & " + str(augmentingPath[-1]))
            node.match = augmentingPath[-1]
            augmentingPath[-1].match = node
        elif node.match == augmentingPath[-1]:
            print("Inverting match between " + str(node) + " & " + str(augmentingPath[-1]))
            node.match = None
            augmentingPath[-1].match = None
        elif node.match != augmentingPath[-1]:
            print("Completing inversion between " + str(node) +"  & "+ str(augmentingPath[-1]))
            augmentingPath[-1].match = None
        else:
            print("Match not next augmented path, error")

    return pizzaWanters


    

# initial_matching_edges = bruteForce(graph)
# brute_force(pizzaWanters)
# print("initial matching")
# for wanter in pizzaWanters:
#     print(str(wanter) + ": " + wanter.get_match_name())

# while True:
#     augmenting_path = get_augmenting_path(pizzaWanters)
#     print("augmenting path", augmenting_path)
#     augmenting_path_list = augmentingPath(graph, initial_matching_edges)
#     #    print("augmenting path", augmenting_path_list)
#     if augmenting_path_list == None:
#         break
#     else:
#         initial_matching_edges = subtractAugmentingPath(graph, initial_matching_edges, augmenting_path_list)
#         augmented_pizzaWanters = subtract_augumenting_path(pizzaWanters, augmenting_path)

# print("final matching edges")
# for wanter in augmented_pizzaWanters:
#     print(str(wanter) + ": " + wanter.get_match_name())

