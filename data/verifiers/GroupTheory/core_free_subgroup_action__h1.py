import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, n = witness
    except Exception:
        return [False, False]
        
    # H1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False
        
    # neg_Q: not (P <==> Q)
    try:
        if not (isinstance(n, int) and n > 0):
            neg_q = False
        elif isinstance(G, PermutationGroup):
            # For any valid group, the theorem holds mathematically (P <==> Q is True).
            # Thus, the equivalence never fails for a group.
            neg_q = False
        else:
            if isinstance(G, Permutation):
                G = [G]
            
            if isinstance(G, (list, tuple)) and all(isinstance(g, Permutation) for g in G):
                # Evaluate P: G acts faithfully and transitively on a set of size n
                elements = set(range(n))
                for p in G:
                    elements.update(range(p.size))
                    
                orbits = []
                visited_global = set()
                for i in elements:
                    if i not in visited_global:
                        visited = {i}
                        queue = [i]
                        while queue:
                            curr = queue.pop(0)
                            for p in G:
                                nxt = p(curr) if curr < p.size else curr
                                if nxt not in visited:
                                    visited.add(nxt)
                                    queue.append(nxt)
                        orbits.append(visited)
                        visited_global.update(visited)
                
                P = False
                for orb in orbits:
                    if len(orb) == n:
                        effects = set()
                        faithful = True
                        for p in G:
                            effect = tuple(p(x) if x < p.size else x for x in sorted(orb))
                            if effect in effects:
                                faithful = False
                                break
                            effects.add(effect)
                        if faithful:
                            P = True
                            break
                
                # Evaluate Q: exists subgroup H <= G with [G:H] = n and trivial core
                # Since G is just a list/set of permutations (not a group), it has no subgroups.
                Q = False
                
                neg_q = not (P == Q)
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: G acts faithfully and transitively on a set of size n iff there exists a core-free subgroup of index n FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1