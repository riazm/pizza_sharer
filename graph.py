class PizzaWanter:
    def __init__(self, name, wanted_pizzas):
        self.name = name
        self.wanted_pizzas = wanted_pizzas
        self.connections = []
        self.match = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

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


riaz = PizzaWanter("riaz", ["mozarella", "funghi"])
scott = PizzaWanter("scott", ["aubergine"])
joulia = PizzaWanter("joulia", ["aubergine"])
artemis = PizzaWanter("artemis", ["mozarella", "courgette", "onion"])
rachel = PizzaWanter("rachel", ["courgette"])
monkey = PizzaWanter("monkey", ["funghi"])
tort = PizzaWanter("tort", ["onion", "cabbage"])
chicken = PizzaWanter("chicken", ["cabbage"])
edgar = PizzaWanter("edgar", ["mozarella"])
weirdo = PizzaWanter("weirdo", ["pine apple"])
oddboi = PizzaWanter("oddBoi", ["mozarella", "funghi", "courgette", "onion", "cabbage"])


def createGraph(pizzaWanters):
    pizza_graph = {}
    for wanter in pizzaWanters:
        pizza_graph[wanter.name] = []
        for sharer in pizzaWanters:
            if sharer != wanter:
                for wanted_pizza in wanter.wanted_pizzas:
                    if wanted_pizza in sharer.wanted_pizzas:
                        pizza_graph[wanter.name].append(sharer.name)
                        wanter.connections.append(sharer)
        # print(str(wanter) + " connected to " + wanter.get_connection_names())
    return(pizza_graph)


def bruteForce(want_graph):
    matching_edges = {}
    taken = []
    for wanter in want_graph:
        if wanter not in taken:
            for sharer in want_graph[wanter]:
                if sharer not in taken:
                    matching_edges[wanter] = sharer
                    taken.append(sharer)
                    taken.append(wanter)
                break
    return matching_edges

def brute_force(pizzaWanters):
    matching_edges = {}
    taken = []
    for wanter in pizzaWanters:
        if wanter not in taken:
            for sharer in wanter.connections:
                if sharer not in taken:
                    wanter.match = sharer
                    sharer.match = wanter
                    taken.append(sharer)
                    taken.append(wanter)
                    # print(str(wanter) + " matched to " + wanter.get_match_name())
                break
    return matching_edges


def getPath(want_graph, path):
    wanter = path[-1]
    for sharer in want_graph[wanter]:
        if sharer not in path:
            path.append(sharer)
            getPath(want_graph, path)
            break
    return path

def get_path(pizzaWanters, path):
    # would be better to use from collections import deque
    queue = [path[-1]]
    discovered = []
    while queue:
        currentNode = queue.pop(0)
        print("current node is " + str(currentNode))
        print("queue is" + str(queue))
        for connection in currentNode.connections:
            print("examining connection " + str(connection))
            if connection is currentNode.match:
                print("connection is the current match, ignore")
            elif connection in path:
                print("connection in discovered already, cycle?")
            elif connection.match:
                print("connection has a match " + str(connection.match))
                path.append(connection)
                path.append(connection.match)
                queue.append(connection.match)
            else:
                print("Found free node " + str(connection) + " returning path")
                path.append(connection)
                print(path)
                return path

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

pizzaWanters = [riaz, scott, joulia, artemis,
                     rachel, monkey, tort, chicken]
graph = createGraph(pizzaWanters)
print("graph", graph)
initial_matching_edges = bruteForce(graph)
brute_force(pizzaWanters)
print("initial matching")
for wanter in pizzaWanters:
    print(str(wanter) + ": " + wanter.get_match_name())

while True:
    augmenting_path = get_augmenting_path(pizzaWanters)
    print("augmenting path", augmenting_path)
    augmenting_path_list = augmentingPath(graph, initial_matching_edges)
    #    print("augmenting path", augmenting_path_list)
    if augmenting_path_list == None:
        break
    else:
        initial_matching_edges = subtractAugmentingPath(graph, initial_matching_edges, augmenting_path_list)
        augmented_pizzaWanters = subtract_augumenting_path(pizzaWanters, augmenting_path)

print("final matching edges")
for wanter in augmented_pizzaWanters:
    print(str(wanter) + ": " + wanter.get_match_name())

