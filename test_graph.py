import pizza_graph
graph = {"monkey"  : set(['riaz']),
         "riaz"    : set(['monkey', 'artemis']),
         "rachel"  : set(['artemis']),
         "artemis" : set(['tort', 'riaz', 'rachel']),
         "tort"    : set(['chicken', 'artemis']),
         "scott"   : set(['joulia']),
         "chicken" : set(['tort']),
         "joulia"  : set(['scott'])}


def test_path_1():
    matching = {"riaz": "artemis",
                "artemis": "riaz", 
                "monkey"  : None,
                "rachel"  : None,
                "tort"    : None,
                "scott"   :"joulia",
                "chicken" : None,
                "joulia"  :"scott"}

    path = (pizza_graph.get_path(graph, matching, ["tort", "artemis", "riaz"]))

    assert path[0] == "tort"
    assert path[1] == "artemis"
    assert path[2] == "riaz"
    assert path[3] == "monkey"
    check_path(graph, matching, path)

def test_path_2():
    matching = {"riaz": "artemis",
                "artemis": "riaz", 
                "monkey"  : None,
                "rachel"  : None,
                "tort"    : None,
                "scott"   :"joulia",
                "chicken" : None,
                "joulia"  :"scott"}

    path = (pizza_graph.get_path(graph, matching, ["tort"]))
    check_path(graph, matching, path)
    assert path == ["tort", "chicken"]

def test_path_3():
    matching = {"riaz": "artemis",
                "artemis": "riaz", 
                "monkey"  : None,
                "rachel"  : None,
                "tort"    :"chicken",
                "scott"   :"joulia",
                "chicken" :"tort",
                "joulia"  :"scott"}

    path = (pizza_graph.get_path(graph, matching, ["monkey"]))
    print("got " + str(path))
    check_path(graph, matching, path)
    assert path == ["monkey", "riaz", "artemis", "rachel"]
 
def check_path(graph, matching, path):
    assert path != None, "Path is empty"
    assert len(path) == len(set(path))
    for node_index, node in enumerate(path):
        if node_index == 0:
            #check first element isn't a match
            assert matching[node] == None, "First element should not have a match"
        elif node_index == len(path) -1:
            #check final element isn't a match
            assert matching[node] == None, "last element should not have a match"
        else:
            assert path[node_index +1] in graph[node], \
                "element "+ path[node_index +1] +" following does not connect to " + node
            assert path[node_index -1] in graph[node], "element preceding does not connect"
            if path[node_index -1 ] == matching[node]:
                assert path[node_index +1] != matching[node], "match found behind and ahead"
            elif path[node_index+1] == matching[node]:
                assert path[node_index -1] != matching[node], "match found ahead and behind"

        
    
def test_path_4():
    # this always ends in an odd path sort it out
    graph = {"a1"  : set(['b1', 'b3', 'b5']),
             "a2"  : set(['b2', 'b3']),
             "a3"  : set(['b1', 'b3']),
             "a4"  : set(['b4', 'b3']),
             "a5"  : set(['b3', 'b5']),
             "b1"  : set(['a1', 'a3']),
             "b2"  : set(['a2']),
             "b3"  : set(['a2', 'a1', 'a3']),
             "b4"  : set(['a4']),
             "b5"  : set(['a5', 'a1'])
    }
    
    matching = {"a1": "b1",
                "a2": "b2", 
                "a3": "b3",
                "a4": None,
                "a5": None,
                "b1": "a1",
                "b2": "a2",
                "b3": "a3",
                "b4": None,
                "b5": None}

    path = (pizza_graph.get_path(graph, matching, ["a4"]))
    check_path(graph, matching, path)

def test_augment_path_single_pair():
    matching = {"riaz": "artemis",
                "artemis": "riaz", 
                "monkey"  : None,
                "rachel"  : None,
                "tort"    : None,
                "scott"   :"joulia",
                "chicken" : None,
                "joulia"  :"scott"}

    path = ["tort", "chicken"]
    augmented_path = pizza_graph.augment_path(path, matching)

    assert augmented_path == {"riaz": "artemis",
                              "artemis": "riaz", 
                              "monkey"  : None,
                              "rachel"  : None,
                              "tort"    : "chicken",
                              "scott"   :"joulia",
                              "chicken" : "tort",
                              "joulia"  :"scott"}

def test_augment_path_max_element():
    matching = {"riaz": "artemis",
                "artemis": "riaz", 
                "monkey"  : None,
                "rachel"  : None,
                "tort"    : "chicken",
                "scott"   :"joulia",
                "chicken" : "tort",
                "joulia"  :"scott"}

    path = ["monkey", "riaz", "artemis","tort","chicken","rachel"]
    augmented_path = pizza_graph.augment_path(path, matching)

    assert augmented_path == {"riaz": "monkey",
                              "artemis": "tort", 
                              "monkey"  : "riaz",
                              "rachel"  : "chicken",
                              "tort"    : "artemis",
                              "scott"   :"joulia",
                              "chicken" : "rachel",
                              "joulia"  :"scott"}
