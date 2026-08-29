import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup, Permutation

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, sigma, tau = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is the symmetric group S_n
    try:
        if isinstance(G, PermutationGroup) and G.degree > 0:
            # A permutation group of degree n is the symmetric group S_n iff its order is n!
            h1 = (G.order() == math.factorial(G.degree))
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: sigma and tau are permutations in G
    try:
        h2 = isinstance(sigma, Permutation) and isinstance(tau, Permutation) and (sigma in G) and (tau in G)
    except Exception:
        h2 = False
        
    # neg_Q: not (conjugate in G iff same cycle type)
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        elif not (isinstance(sigma, Permutation) and isinstance(tau, Permutation)):
            neg_q = False
        else:
            # Pad permutations to the same size to accurately compare cycle structures and equality
            def pad(p, size):
                if p.size >= size: 
                    return p
                arr = list(p.array_form)
                arr.extend(list(range(p.size, size)))
                return Permutation(arr)
                
            max_size = max(G.degree, sigma.size, tau.size)
            s = pad(sigma, max_size)
            t = pad(tau, max_size)
            
            # In SymPy, cycle_structure maps length to count for lengths >= 2.
            # Since s and t are padded to the same size, same cycle_structure implies same number of fixed points.
            same_cycle_type = (s.cycle_structure == t.cycle_structure)
            
            are_conjugate = False
            if s == t:
                are_conjugate = True
            elif (sigma in G) and (tau in G) and G.degree > 0 and G.order() == math.factorial(G.degree):
                # Shortcut: In S_n, two elements are conjugate iff they have the same cycle type
                are_conjugate = same_cycle_type
            else:
                # Breadth-first search to find if t is in the conjugacy class of s in G
                visited = {s}
                queue = [s]
                gens = G.generators
                found = False
                for curr in queue:
                    if len(visited) > 50000:
                        break
                    for g in gens:
                        next_perm = g * curr * ~g
                        if next_perm == t:
                            found = True
                            break
                        if next_perm not in visited:
                            visited.add(next_perm)
                            queue.append(next_perm)
                    if found:
                        break
                are_conjugate = found
                
            q = (are_conjugate == same_cycle_type)
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is the symmetric group S_n",
    "H_2: sigma and tau are permutations in G",
    "¬Q: sigma and tau are conjugate in G if and only if they have the same cycle type fails"
]

N_HYP = 2
NEG_Q_INDEX = 2