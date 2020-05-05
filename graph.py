class PizzaWanter:
    def __init__(self, name, wanted_pizzas):
        self.name = name
        self.wanted_pizzas = wanted_pizzas
        self.connections = []
        self.confirm_match = None

    def __str__(self):
        return self.name

    def print_connections(self):
        return ",".join([str(elem.name) for elem in self.connections])

    def print_match(self):
        return self.confirm_match.name
                                          
    # "wanted pizzas= " + ",".join([str(elem) for elem in self.wanted_pizzas]) \
    # + "\n" + "connections= " + ",".join([str(elem.name) for elem in self.connections]) \
    # + "\n" + "confirmed_match=" + (self.confirm_match or "No match")


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
        print(str(wanter) + " connected to " + wanter.print_connections())
    return(pizza_graph)


def bruteForce(want_graph):
    matching_edges = {}
    taken = []
    for wanter in want_graph:
        if wanter not in taken:
            for sharer in want_graph[wanter]:
                if sharer not in taken:
                    matching_edges[wanter] = sharer
                    wanter.confirm_match = sharer
                    taken.append(sharer)
                    taken.append(wanter)
                    print(wanter)
                break
    return matching_edges


def getPath(want_graph, path):
    wanter = path[-1]
    print("Adding to" + path)
    for sharer in want_graph[wanter]:
        if sharer not in path:
            print("Foud" + sharer + "adding to path")
            path.append(sharer)
            getPath(want_graph, path)
            break
    return path


def augmentingPath(want_graph, initial_match):
    for wanter in want_graph:
        print("Bulding path from" + wanter)
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

graph = createGraph([riaz, scott, joulia, artemis,
                     rachel, monkey, tort, chicken])
print("graph", graph)
initial_matching_edges = bruteForce(graph)
print("initial matching", initial_matching_edges)

while True:
    augmenting_path = augmentingPath(graph, initial_matching_edges)
    print("augmenting path", augmenting_path)
    if augmenting_path == None:
        break
    else: 
        initial_matching_edges = subtractAugmentingPath(graph, initial_matching_edges, augmenting_path)
        print("matching edges", initial_matching_edges)


print("subtracted_path", initial_matching_edges)

