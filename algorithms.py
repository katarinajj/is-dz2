import copy


class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass


class ExampleAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        print("TILES")
        for x in tiles:
            print(x)
        print("VARIABLES")
        print(variables)
        print("WORDS")
        print(words)
        moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
                      ['2h', None], ['1v', None], ['0v', 3], ['1v', 1], ['2h', 1],
                      ['4h', 4], ['5v', 5]]
        domains = {var: [word for word in words] for var in variables}
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        print("DOMAINS")
        print(domains)
        print("SOLUTION")
        print(solution)
        return solution


class Node:
    def __init__(self, val, adj_list):
        self.val = val
        self.adj_list = adj_list


class Graph:
    def __init__(self, tiles, variables):
        self.n = len(tiles)
        self.m = len(tiles[0])
        self.graph = {}
        self.assigned = {}
        self.key_count = len(variables)
        for key in variables:
            self.graph[key] = set()
            self.assigned[key] = False

        self.form_constraints(tiles, variables)
        for key in variables:
            self.graph[key] = sorted(self.graph[key])

        self.filled_tiles = [''] * (self.n * self.m)
        self.form_filled_tiles(tiles)

    def edge(self, a, b):
        if a != b:
            self.graph[a].add(b)
            self.graph[b].add(a)

    def form_key_edges(self, key, cnt, variables):
        key_h = str(cnt) + 'h'
        if key_h in variables:
            self.edge(key, key_h)
        key_v = str(cnt) + 'v'
        if key_v in variables:
            self.edge(key, key_v)

    def form_constraints(self, tiles, variables):
        cnt = 0
        n = len(tiles)
        m = len(tiles[0])
        for i in range(0, n):
            for j in range(0, m):
                key = str(cnt) + 'h'
                if key in variables:
                    for col in range(j, j + variables[key]):
                        self.form_key_edges(key, i * m + col, variables)

                key = str(cnt) + 'v'
                if key in variables:
                    for row in range(i, i + variables[key]):
                        self.form_key_edges(key, row * m + j, variables)

                cnt += 1

    def print_graph(self):
        print(self.graph)

    def get_next_unassigned(self):
        for key in self.assigned:
            if self.assigned[key] is False:
                return key
        return None

    def assigned_key(self, key):
        self.assigned[key] = True

    def unassigned_key(self, key):
        self.assigned[key] = False

    def form_filled_tiles(self, tiles):
        ind = 0
        for i in range(0, self.n):
            for j in range(0, self.m):
                if tiles[i][j] is True:
                    self.filled_tiles[ind] = '-'
                ind += 1

    def are_constrained(self, a, b):
        return b in self.graph[a]


def assign_var(graph, var, value):
    graph.assigned_key(var)
    ind = int(var[0:-1])
    value_len = len(value)
    if var[-1] == 'h':
        for i in range(0, value_len):
            graph.filled_tiles[ind + i] = value[i]
    else:
        for i in range(0, value_len):
            graph.filled_tiles[ind + i * graph.m] = value[i]

def unassign_var(graph, var, value_len):
    graph.unassigned_key(var)
    ind = int(var[0:-1])
    if var[-1] == 'h':
        for i in range(0, value_len):
            graph.filled_tiles[ind + i] = ''
    else:
        for i in range(0, value_len):
            graph.filled_tiles[ind + i * graph.m] = ''

def is_consistent_assignment(var, value, graph):
    ind = int(var[0:-1])
    value_len = len(value)
    if var[-1] == 'h':
        for i in range(0, value_len):
            field = graph.filled_tiles[ind + i]
            if field != '' and field != value[i]:
                return False
    else:
        for i in range(0, value_len):
            field = graph.filled_tiles[ind + i * graph.m]
            if field != '' and field != value[i]:
                return False

    return True

def backtrack_search(graph, moves_list, domains, level, fc=False):
    if level == graph.key_count:
        return True
    var = graph.get_next_unassigned()

    values = domains[var]
    len_values = len(values)
    len_in_domain = 0 if (len_values == 0) else len(values[0])

    for i in range(0, len_values):
        value = values[i]
        if is_consistent_assignment(var, value, graph):
            moves_list.append([var, i])
            assign_var(graph, var, value)

            # if fc:
            #     new_dom = copy.deepcopy(domains)
            #     new_dom[var] = [value]
            #     for v in variables:
            #         if var != v and graph.are_constrained(var, v):
            #             update_domain(new_dom[var], v, value, graph)

            if backtrack_search(graph, moves_list, domains, level + 1, fc):
                return True

    moves_list.append([var, None])
    unassign_var(graph, var, len_in_domain)
    return False

class Backtracking(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        graph = Graph(tiles, variables)
        graph.print_graph()

        moves_list = []
        domains = {var: [word for word in words if len(word) == variables[var]] for var in variables}
        backtrack_search(graph, moves_list, domains, 0)

        print("MOVES LIST: ")
        print(moves_list)
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution


class ForwardChecking(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        graph = Graph(tiles, variables)
        graph.print_graph()

        moves_list = []
        domains = {var: [word for word in words if len(word) == variables[var]] for var in variables}
        backtrack_search(graph, moves_list, domains, 0, True)

        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution


class ArcConsistency(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        solution = []
        return solution
