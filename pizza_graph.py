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
            if connected_node in path and connected_node != path[-2]:
                cycle = []
                for node in reversed(path):
                    if node != connected_node:
                        cycle.append(node)
                if len(cycle) % 2 == 0:
                    print(cycle)
                    shrink_cycle(graph, path, cycle)
                    return "ODD cycle detected!"
            elif connected_node in path and connected_node == path[-2]:
                print("last node, ignore")
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

def shrink_cycle(graph, path, cycle):
    cycle_root = cycle[0]
    contracted_graph = {}
    print(cycle_root)
    for node in graph:
        print("node " + node)
        if node == cycle_root:
            contracted_graph[node] = graph[node].difference(cycle)
            print("Set cycle root " + node + " to " + str(contracted_graph[node]))            
        elif node in cycle:
            print("what")
        elif graph[node].difference(cycle) != graph[node]:
            contracted_graph[node] = graph[node].difference(cycle)
            contracted_graph[node].add(cycle_root)
            print(contracted_graph[node])
        else:
            print("why am i here")
    return contracted_graph
    
def augment_path(path, match_graph):
    for index,node in enumerate(path):
        if match_graph[node] == None:
            try:
                print("Must be first node, set match to next")
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


