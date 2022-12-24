import copy

class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass


class ExampleAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        print("TILES")
        for x in tiles:
            print(x)
        print(variables)
        print(f'{variables=}')
        print(f'{words=}')
        moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
                      ['2h', None], ['1v', None], ['0v', 3], ['1v', 1], ['2h', 1],
                      ['4h', 4], ['5v', 5]]
        domains = {var: [word for word in words] for var in variables}
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        print(f'{domains=}')
        print(f'{solution=}')
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
        print("GRAPH")
        print(self.graph)

    def get_all_arcs(self):
        all_arc = []
        for a in self.graph:
            for b in self.graph[a]:
                all_arc.append((a, b))
        return all_arc


graph = Graph([[0]], [])
sorted_keys = []

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

def assign_var(assignment, filled_tiles, var, value):
    assignment[var] = value
    ind = int(var[0:-1])
    value_len = len(value)
    if var[-1] == 'h':
        for i in range(0, value_len):
            filled_tiles[ind + i] = value[i]
    else:
        for i in range(0, value_len):
            filled_tiles[ind + i * graph.m] = value[i]

def is_consistent_assignment(var, value, filled_tiles):
    ind = int(var[0:-1])
    value_len = len(value)
    if var[-1] == 'h':
        for i in range(0, value_len):
            field = filled_tiles[ind + i]
            if field != '' and field != value[i]:
                return False
    else:
        for i in range(0, value_len):
            field = filled_tiles[ind + i * graph.m]
            if field != '' and field != value[i]:
                return False
    return True

def not_constraining(var1, value1, var2, value2, filled_tiles):
    # var1 = value1 is newly added in filled_tiles, so
    # it is enough to check if var2 = value 2 is consistent with filled_tiles
    return is_consistent_assignment(var2, value2, filled_tiles)

def satisfies_constraint(var1, value1, var2, value2):
    ind1 = int(var1[0:-1])
    value_len1 = len(value1)
    ind2 = int(var2[0:-1])
    value_len2 = len(value2)

    for i1 in range(0, value_len1):
        next_ind1 = ind1 + i1 if var1[-1] == 'h' else ind1 + i1 * graph.m
        for i2 in range(0, value_len2):
            next_ind2 = ind2 + i2 if var2[-1] == 'h' else ind2 + i2 * graph.m

            if next_ind1 == next_ind2 and value1[i1] != value2[i2]:
                return False

    return True

def update_domain_check_empty(domains, value1, var1, var2, filled_tiles):
    new_domain_var2 = []
    empty = True
    updated = False
    for value2 in domains[var2]:
        ret1 = not_constraining(var1, value1, var2, value2, filled_tiles)
        ret2 = satisfies_constraint(var1, value1, var2, value2)
        if ret1 != ret2:
            print("Funcstions should return the same value")

        if satisfies_constraint(var1, value1, var2, value2):
            new_domain_var2.append(value2)
            empty = False
        else:
            updated = True
    domains[var2] = new_domain_var2
    return empty, updated

def arc_consistency(domains):
    all_arcs = graph.get_all_arcs()
    while all_arcs:
        x, y = all_arcs.pop(0)  # x -> y
        new_domain_x = []
        for value_x in domains[x]:
            y_satisfying_value = False
            for value_y in domains[y]:
                if satisfies_constraint(x, value_x, y, value_y):
                    y_satisfying_value = True
                    break
            if y_satisfying_value is True:
                new_domain_x.append(value_x)

        if len(domains[x]) - len(new_domain_x) > 0:
            if len(new_domain_x) == 0:
                return False
            domains[x] = new_domain_x

            for z in graph.get_adj_list(x):  # z -> x
                all_arcs.append((z, x))

    return True

def arc_consistency2(domains, queue):
    while queue:
        y = queue.pop(0)
        for x in graph.get_adj_list(y):  # x -> y
            new_domain_x = []
            for value_x in domains[x]:
                y_satisfying_value = False
                for value_y in domains[y]:
                    if satisfies_constraint(x, value_x, y, value_y):
                        y_satisfying_value = True
                        break
                if y_satisfying_value is True:
                    new_domain_x.append(value_x)

            if len(domains[x]) - len(new_domain_x) > 0:  # has values to be deleted
                if len(new_domain_x) == 0:
                    return False
                domains[x] = new_domain_x

                queue.append(x)

    return True


def backtrack(solution, domains, level, assignment, filled_tiles, fc, arc):
    if level == graph.key_count:
        return True
    # var = get_next_unassigned(assignment)
    var = sorted_keys[level]
    if var is None:
        print("There is no next var but the algorithm did not stop")
        return False

    values = domains[var]
    len_values = len(values)

    for i in range(0, len_values):
        value = values[i]
        if is_consistent_assignment(var, value, filled_tiles):
            solution.append([var, i, domains])
            # print("var: " + str(var) + " i: " + str(i) + " value: " + value)
            new_assignment = copy.deepcopy(assignment)
            new_filled_tiles = copy.deepcopy(filled_tiles)
            new_domains = copy.deepcopy(domains)
            new_domains[var] = [value]

            assign_var(new_assignment, new_filled_tiles, var, value)
            queue = []
            if fc:
                should_continue = False
                for v in graph.get_adj_list(var):
                    if new_assignment[v] is None:
                        empty, updated = update_domain_check_empty(new_domains, value, var, v, new_filled_tiles)
                        if empty is True:
                            should_continue = True
                            break
                        # for arc2
                        if arc and updated:
                            queue.append(var)

                if should_continue is True:
                    continue

            if arc:
                if not arc_consistency2(new_domains, queue):
                    continue

            if backtrack(solution, new_domains, level + 1, new_assignment, new_filled_tiles, fc, arc):
                return True

    solution.append([var, None, domains])
    assignment[var] = None
    return False

class Backtracking(Algorithm):
    def __init__(self):
        self.fc = False
        self.arc = False

    def get_algorithm_steps(self, tiles, variables, words):
        global graph
        graph = Graph(tiles, variables)
        graph.print_graph()

        keys = [key for key in variables]
        global sorted_keys
        sorted_keys = sorted(keys, key=lambda x: (int(x[0:-1]), x[-1]))
        print(f'{sorted_keys=}')

        assignment = {key: None for key in variables}
        filled_tiles = form_filled_tiles(tiles)
        solution = []
        domains = {var: [word for word in words if len(word) == variables[var]] for var in variables}

        if self.arc:
            arc_consistency(domains)

        backtrack(solution, domains, 0, assignment, filled_tiles, self.fc, self.arc)

        print(f'{solution=}')
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
