import sympy
from sympy.combinatorics.free_groups import free_group

# Top-level setup
# Define some standard free groups that a witness expression might reference.
F1, x = free_group("x")
F2, a, b = free_group("a, b")
F3, u, v, w = free_group("u, v, w")

class StallingsGraph:
    """
    Represents the Stallings core graph for a finitely generated subgroup of a free group.
    Used to solve the Word Problem (membership) and check finite index.
    """
    def __init__(self, n_gens):
        self.n_gens = n_gens
        self.adj = {0: {}}
        self.rev = {0: {}}
        self.next_v = 1

    def add_vertex(self):
        v = self.next_v
        self.next_v += 1
        self.adj[v] = {}
        self.rev[v] = {}
        return v

    def add_edge_raw(self, u, c, v):
        if u not in self.adj: self.adj[u] = {}
        if c not in self.adj[u]: self.adj[u][c] = []
        self.adj[u][c].append(v)
        
        if v not in self.rev: self.rev[v] = {}
        if c not in self.rev[v]: self.rev[v][c] = []
        self.rev[v][c].append(u)

    def add_word(self, word):
        if not word: return
        vertices = [0] + [self.add_vertex() for _ in range(len(word)-1)] + [0]
        for i, c in enumerate(word):
            if c > 0:
                self.add_edge_raw(vertices[i], c, vertices[i+1])
            else:
                self.add_edge_raw(vertices[i+1], -c, vertices[i])
        self.fold()

    def fold(self):
        changed = True
        while changed:
            changed = False
            merge_pairs = []
            for u in self.adj:
                for c, targets in self.adj[u].items():
                    if len(targets) > 1:
                        merge_pairs.append((targets[0], targets[1]))
            for v in self.rev:
                for c, sources in self.rev[v].items():
                    if len(sources) > 1:
                        merge_pairs.append((sources[0], sources[1]))
            
            if merge_pairs:
                changed = True
                u, v = merge_pairs[0]
                if u > v: u, v = v, u
                
                new_adj = {}
                new_rev = {}
                for node in self.adj:
                    n = u if node == v else node
                    if n not in new_adj: new_adj[n] = {}
                    if n not in new_rev: new_rev[n] = {}
                    for c, targets in self.adj[node].items():
                        if c not in new_adj[n]: new_adj[n][c] = []
                        for t in targets:
                            t_new = u if t == v else t
                            if t_new not in new_adj[n][c]:
                                new_adj[n][c].append(t_new)
                                
                for node in self.rev:
                    n = u if node == v else node
                    if n not in new_rev: new_rev[n] = {}
                    if n not in new_adj: new_adj[n] = {}
                    for c, sources in self.rev[node].items():
                        if c not in new_rev[n]: new_rev[n][c] = []
                        for s in sources:
                            s_new = u if s == v else s
                            if s_new not in new_rev[n][c]:
                                new_rev[n][c].append(s_new)
                                
                self.adj = new_adj
                self.rev = new_rev

    def contains(self, word):
        curr = 0
        for c in word:
            if c > 0:
                if c not in self.adj.get(curr, {}) or not self.adj[curr][c]:
                    return False
                curr = self.adj[curr][c][0]
            else:
                if -c not in self.rev.get(curr, {}) or not self.rev[curr][-c]:
                    return False
                curr = self.rev[curr][-c][0]
        return curr == 0

    def is_non_trivial(self):
        for v in self.adj:
            if self.adj[v]: return True
        return False

    def is_normal(self, N_words):
        for g in range(1, self.n_gens + 1):
            for w in N_words:
                if not self.contains([g] + w + [-g]): return False
                if not self.contains([-g] + w + [g]): return False
        return True

    def has_finite_index(self):
        vertices = set(self.adj.keys()) | set(self.rev.keys())
        for v in vertices:
            for c in range(1, self.n_gens + 1):
                if c not in self.adj.get(v, {}) or len(self.adj[v][c]) != 1:
                    return False
                if c not in self.rev.get(v, {}) or len(self.rev[v][c]) != 1:
                    return False
        return True


def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (F, N_gens) where F is a FreeGroup
    and N_gens is a list of FreeGroupElements generating the subgroup N.
    """
    try:
        if type(witness).__name__ == 'FpSubgroup':
            F = witness.parent
            N_gens = witness.generators
        else:
            F, N_gens = witness
            
        is_free_group = False
        if type(F).__name__ == 'FreeGroup':
            is_free_group = True
        elif type(F).__name__ == 'FpGroup' and len(F.relators) == 0:
            is_free_group = True
            
        if not is_free_group:
            return [False, False, False]
            
        n_gens = len(F.generators)
        if n_gens == 0:
            return [True, False, False]
            
        gen_to_int = {}
        for i, g in enumerate(F.generators):
            gen_to_int[g] = i + 1
            
        N_words = []
        for w in N_gens:
            word = []
            for g, exp in w.array_form:
                c = gen_to_int[g]
                if exp > 0:
                    word.extend([c] * exp)
                else:
                    word.extend([-c] * (-exp))
            N_words.append(word)
            
        sg = StallingsGraph(n_gens)
        for word in N_words:
            sg.add_word(word)
            
        h1 = is_free_group
        
        is_non_trivial = sg.is_non_trivial()
        is_finitely_generated = True  # N_gens is a finite list
        is_normal = sg.is_normal(N_words)
        
        h2 = is_non_trivial and is_finitely_generated and is_normal
        
        has_finite_index = sg.has_finite_index()
        neg_q = not has_finite_index
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: N is a non-trivial finitely generated normal subgroup of F",
    "¬Q: The subgroup N does NOT have finite index in F"
]

N_HYP = 2
NEG_Q_INDEX = 2