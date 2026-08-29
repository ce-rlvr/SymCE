import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Provide some standard free groups for convenience
F1, x = free_group('x')
F2, a, b = free_group('a, b')
F3, u, v, w = free_group('u, v, w')

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, S) where F is a free group and S is a subset of F.
    """
    try:
        F, S = witness
    except Exception:
        return [False, False]
        
    # H_1: F is a free group
    try:
        F_dummy, _ = free_group('dummy')
        FreeGroupClass = type(F_dummy)
        h1 = isinstance(F, FreeGroupClass)
    except Exception:
        h1 = False
        
    # neg_Q: The Cayley graph of F with respect to S is NOT a tree
    try:
        if not isinstance(S, (list, tuple, set)):
            raise ValueError
            
        ElementClass = type(F.identity)
        for s in S:
            if not isinstance(s, ElementClass) or s.group != F:
                raise ValueError
                
        tree = True
        n = len(F.generators)
        
        if not S:
            # Empty generating set: Cayley graph is a tree iff the group is trivial
            tree = (n == 0)
        else:
            # A tree cannot have self-loops (identity in S)
            if F.identity in S:
                tree = False
            else:
                # A tree cannot have multiple edges between the same pair of vertices
                S_set = set(S)
                for s in S:
                    if s**-1 in S_set:
                        tree = False
                        break
                
                if tree:
                    # Abelianization check: S must freely generate F, so its abelianization 
                    # must be a basis for Z^n. Thus, |S| == n and the determinant must be ±1.
                    M = []
                    for s in S:
                        sums = {g: 0 for g in F.generators}
                        for gen, exp in s.array_form:
                            sums[gen] += exp
                        M.append([sums[g] for g in F.generators])
                        
                    if len(S) != n:
                        tree = False
                    elif n > 0:
                        det = sympy.Matrix(M).det()
                        if abs(det) != 1:
                            tree = False
                            
                if tree:
                    # BFS to detect any short cycles in the Cayley graph
                    S_all = []
                    for s in S:
                        S_all.append(s)
                        S_all.append(s**-1)
                        
                    visited = set([F.identity])
                    queue = [(F.identity, None)]
                    max_nodes = 2000
                    
                    for depth in range(10):
                        next_queue = []
                        cycle_found = False
                        for node, last_inv in queue:
                            for s in S_all:
                                if s == last_inv:
                                    continue  # No backtracking
                                neighbor = node * s
                                if neighbor in visited:
                                    cycle_found = True
                                    break
                                visited.add(neighbor)
                                next_queue.append((neighbor, s**-1))
                            if cycle_found:
                                break
                        if cycle_found:
                            tree = False
                            break
                        queue = next_queue
                        if not queue or len(visited) > max_nodes:
                            break
                            
        neg_q = not tree
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: The Cayley graph of F with respect to S is NOT a tree"
]

N_HYP = 1
NEG_Q_INDEX = 1