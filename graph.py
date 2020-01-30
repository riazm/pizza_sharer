class PizzaWanter:
    def __init__(self, name, wanted_pizzas):
        self.name = name
        self.wanted_pizzas = wanted_pizzas
        self.potential_connections = []
        self.confirm_connection = None

    def __str__(self):
        return "wanted pizzas= " + ",".join([str(elem) for elem in self.wanted_pizzas]) \
    + "\n" + "connections= " + ",".join([str(elem) for elem in self.connections])


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


def getPath(want_graph, path):
    wanter = path[-1]
    for sharer in want_graph[wanter]:
        if sharer not in path:
            path.append(sharer)
            getPath(want_graph, path)
            break
    return path


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

graph = createGraph([riaz, scott, joulia, artemis,
                     rachel, monkey, tort, chicken,
                     edgar, weirdo, oddboi])
print("graph", graph)
initial_matching_edges = bruteForce(graph)
print("initial matching", initial_matching_edges)

while True:
    augmenting_path = augmentingPath(graph, initial_matching_edges)
    print("augmenting path", augmenting_path)
    if augmenting_path == None:
        break
    else: 
        matching_edges = subtractAugmentingPath(graph, initial_matching_edges, augmenting_path)


print("subtracted_path", matching_edges)

