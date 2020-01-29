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
scott = PizzaWanter("scott", ["mozarella"])
joulia = PizzaWanter("joulia", ["funghi"])
artemis = PizzaWanter("artemis", ["pineapple", "mozarella", "funghi"])
rachel = PizzaWanter("rachel", ["pineapple"])

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
            
graph = createGraph([riaz, scott, joulia, rachel, artemis])
print(graph)
pair_graph = bruteForce(graph)
print(pair_graph)
