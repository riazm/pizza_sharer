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


def createGraph(pizzaWanters):
    pizza_graph = {}
    for wanter in pizzaWanters:
        pizza_graph[wanter.name] = []
        for sharer in pizzaWanters:
            if sharer != wanter:
                for wanted_pizza in wanter.wanted_pizzas:
                    if wanted_pizza in sharer.wanted_pizzas:
                        pizza_graph[wanter.name].append(sharer.name)
                        # print(wanter.name, "wants", wanted_pizza)
                        # print(sharer.name, "willing to share", sharer.wanted_pizzas)
    return(pizza_graph)


def bruteForce(want_graph):
    pair_graph = {}
    taken = []
    for wanter in want_graph:
        if wanter not in taken:
            want_graph[wanter] = set(want_graph[wanter]) - set(taken)
            for sharer in want_graph[wanter]:
                pair_graph[wanter] = sharer
                taken.append(sharer)
                taken.append(wanter)
                break
    return pair_graph


def getPath(want_graph, path):
    print(want_graph)
    wanter = path[-1]
    for sharer in want_graph[wanter]:
        if sharer not in path:
            path.append(sharer)
            getPath(want_graph, path)
            break
    return path


def augmentingPath(want_graph, initial_flow):
    for wanter in want_graph:
        if wanter not in initial_flow.keys() \
           and wanter not in initial_flow.values():
            return getPath(want_graph, [wanter])


graph = createGraph([riaz, scott, joulia, artemis,
                     rachel, monkey, tort, chicken])
print(graph)
pair_flow = bruteForce(graph)
print(pair_flow)
augmenting_path = augmentingPath(graph, pair_flow)
print(augmenting_path)

