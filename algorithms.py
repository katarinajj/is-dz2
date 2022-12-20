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
        self.key_count = len(variables)
        for key in variables:
            self.graph[key] = set()

        self.form_constraints(tiles, variables)
        for key in variables:
            self.graph[key] = sorted(self.graph[key])

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

    def get_all_arcs(self):
        all_arc = []
        for a in self.graph:
            for b in self.graph[a]:
                all_arc.append((a, b))
        return all_arc


def get_next_unassigned(assignment):
    for key in assignment:
        if assignment[key] is None:
            return key
    return None


def form_filled_tiles(tiles):
    n = len(tiles)
    m = len(tiles[0])
    filled_tiles = [''] * (len(tiles) * len(tiles[0]))
    ind = 0
    for i in range(0, n):
        for j in range(0, m):
            if tiles[i][j] is True:
                filled_tiles[ind] = '-'
            ind += 1
    return filled_tiles

def assign_var(assignment, filled_tiles, var, value, m):
    assignment[var] = value
    ind = int(var[0:-1])
    value_len = len(value)
    if var[-1] == 'h':
        for i in range(0, value_len):
            filled_tiles[ind + i] = value[i]
    else:
        for i in range(0, value_len):
            filled_tiles[ind + i * m] = value[i]

def is_consistent_assignment(var, value, filled_tiles, m):
    ind = int(var[0:-1])
    value_len = len(value)
    if var[-1] == 'h':
        for i in range(0, value_len):
            field = filled_tiles[ind + i]
            if field != '' and field != value[i]:
                return False
    else:
        for i in range(0, value_len):
            field = filled_tiles[ind + i * m]
            if field != '' and field != value[i]:
                return False
    return True

def not_constraining(var1, value1, var2, value2, filled_tiles, m):
    # var1 = value1 is newly added in filled_tiles, so
    # it is enough to check if var2 = value 2 would constrain with filled_tiles
    return is_consistent_assignment(var2, value2, filled_tiles, m)

def update_domain(new_domains, value1, var1, var2, filled_tiles, m):
    new_domains_var2 = []
    for value2 in new_domains[var2]:
        if not_constraining(var1, value1, var2, value2, filled_tiles, m):
            new_domains_var2.append(value2)
    new_domains[var2] = new_domains_var2

def satisfies_constraint(filled_tiles, var1, value1, var2, value2, m):
    ind1 = int(var1[0:-1])
    value_len1 = len(value1)
    ind2 = int(var2[0:-1])
    value_len2 = len(value2)

    for i1 in range(0, value_len1):
        next_ind1 = ind1 + i1 if var1[-1] == 'h' else ind1 + i1 * m
        for i2 in range(0, value_len2):
            next_ind2 = ind2 + i2 if var2[-1] == 'h' else ind2 + i2 * m

            if next_ind1 == next_ind2 and value1[i1] != value2[i2]:
                return False

    return True


def arc_consistency(graph, domains, filled_tiles):
    all_arcs = graph.get_all_arcs()
    while all_arcs:
        x, y = all_arcs.pop(0)
        x_vals_to_del = []
        for val_x in domains[x]:
            y_no_val = True

            for val_y in domains[y]:
                if satisfies_constraint(filled_tiles, x, val_x, y, val_y, graph.m):
                    y_no_val = False
                    break

            if y_no_val:
                x_vals_to_del.append(val_x)

        if x_vals_to_del:
            domains[x] = [val for val in domains[x] if val not in x_vals_to_del]
            if not domains[x]:
                return False

            for z in graph.get_adj_list(x):
                all_arcs.append((z, x))
    return True


def backtrack(graph, moves_list, domains, level, assignment, filled_tiles, fc, arc):
    if level == graph.key_count:
        return True
    var = get_next_unassigned(assignment)

    values = domains[var]
    len_values = len(values)

    for i in range(0, len_values):
        value = values[i]
        if is_consistent_assignment(var, value, filled_tiles, graph.m):
            moves_list.append([var, i])
            new_assignment = copy.deepcopy(assignment)
            new_filled_tiles = copy.deepcopy(filled_tiles)
            new_domains = copy.deepcopy(domains)
            new_domains[var] = [value]

            assign_var(new_assignment, new_filled_tiles, var, value, graph.m)

            if fc:
                print("FC")
                for v in graph.get_adj_list(var):
                    if new_assignment[v] is None:
                        update_domain(new_domains, value, var, v, new_filled_tiles, graph.m) # works with filled_tiles

            if arc: # samo za izmenjene domene proveravam
                print("ARC")
                if not arc_consistency(graph, new_domains, new_filled_tiles):
                    new_assignment[var] = None
                    continue

            if backtrack(graph, moves_list, new_domains, level + 1, new_assignment, new_filled_tiles, fc, arc):
                return True

    moves_list.append([var, None])
    return False

class Backtracking(Algorithm):
    def __init__(self):
        self.fc = False
        self.arc = False

    def get_algorithm_steps(self, tiles, variables, words):
        graph = Graph(tiles, variables)
        print("GRAPH: ")
        graph.print_graph()

        assignment = {key: None for key in variables}
        filled_tiles = form_filled_tiles(tiles)
        moves_list = []
        domains = {var: [word for word in words if len(word) == variables[var]] for var in variables}

        backtrack(graph, moves_list, domains, 0, assignment, filled_tiles, self.fc, self.arc)

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
