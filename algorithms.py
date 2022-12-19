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

    def get_adj_list(self, key):
        return self.graph[key]

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

    def assign_key(self, key):
        self.assigned[key] = True

    def unassign_key(self, key):
        self.assigned[key] = False

    def form_filled_tiles(self, tiles):
        ind = 0
        for i in range(0, self.n):
            for j in range(0, self.m):
                if tiles[i][j] is True:
                    self.filled_tiles[ind] = '-'
                ind += 1


def assign_var(graph, var, value):
    graph.assign_key(var)
    ind = int(var[0:-1])
    value_len = len(value)
    if var[-1] == 'h':
        for i in range(0, value_len):
            graph.filled_tiles[ind + i] = value[i]
    else:
        for i in range(0, value_len):
            graph.filled_tiles[ind + i * graph.m] = value[i]


def unassign_var(graph, var, value_len):
    if graph.assigned[var] is True:
        graph.unassign_key(var)
        ind = int(var[0:-1])
        if var[-1] == 'h':
            for i in range(0, value_len):
                graph.filled_tiles[ind + i] = ''
        else:
            for i in range(0, value_len):
                graph.filled_tiles[ind + i * graph.m] = ''
    # if var == '4h':
    #     print("BBBBBBBBBBBBBBBBBBBBBB " + var)
    #     print(graph.filled_tiles)


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

def not_constraining(var1, value1, var2, value2, graph):
    # var1 = value1 is newly added in filled_tiles, so
    # it is enough to check if var2 = value 2 would constrain with filled_tiles
    return is_consistent_assignment(var2, value2, graph)

def update_domain(new_domains, value1, var1, var2, graph):
    new_domains_var2 = []
    for value2 in new_domains[var2]:
        if not_constraining(var1, value1, var2, value2, graph):
            new_domains_var2.append(value2)
    new_domains[var2] = new_domains_var2


def backtrack(graph, moves_list, domains, level, fc, arc):
    if level == graph.key_count:
        return True
    var = graph.get_next_unassigned()

    values = domains[var]
    len_values = len(values)
    len_in_domain = 0 if (len_values == 0) else len(values[0])

    for i in range(0, len_values):
        value = values[i]
        if is_consistent_assignment(var, value, graph):
            if not fc and not arc:
                moves_list.append([var, i])
                assign_var(graph, var, value)
                if backtrack(graph, moves_list, domains, level + 1, fc, arc):
                    return True
                # moves_list.append([var, None])
                unassign_var(graph, var, len_in_domain)

            if fc:
                print("FC")
                # moves_list.append([var, 0])
                # assign_var(graph, var, value)
                # new_domains = copy.deepcopy(domains)
                # new_domains[var] = [value]
                # # for v in graph.get_adj_list(var):
                # #     if graph.assigned[v] is False:
                # #         # update_domain(new_domains, value, var, v, graph)
                # if backtrack(graph, moves_list, new_domains, level + 1, fc, arc):
                #     return True

    # reset
    moves_list.append([var, None])
    unassign_var(graph, var, len_in_domain)
    return False

class Backtracking(Algorithm):
    def __init__(self):
        self.fc = False
        self.arc = False

    # da li u backtrackingu domen ostaje konstantno isti ili kad izvrsim dodelu onda azuriram

    def get_algorithm_steps(self, tiles, variables, words):
        graph = Graph(tiles, variables)
        graph.print_graph()

        moves_list = []
        domains = {var: [word for word in words if len(word) == variables[var]] for var in variables}
        backtrack(graph, moves_list, domains, 0, self.fc, self.arc)

        print("MOVES LIST: ")
        print(moves_list)
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution


class ForwardChecking(Backtracking):
    def __init__(self):
        super().__init__()
        self.fc = True
        self.arc = False


class ArcConsistency(Backtracking):
    def __init__(self):
        super().__init__()
        self.fc = True
        self.arc = True
