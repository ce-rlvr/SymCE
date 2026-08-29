import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation(0)])

CONDITION_LABELS = [
    "H_1: G is a permutation group acting transitively on a finite set Omega",
    "¬Q: The equivalence (G is doubly transitive iff G_alpha acts transitively on Omega \\ {alpha}) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            return [False, False]
        
        degree = witness.degree
        if degree < 1:
            return [False, False]
            
        domain = list(range(degree))
        
        # Check H1: G is transitive on domain
        orbit = {domain[0]}
        queue = [domain[0]]
        while queue:
            curr = queue.pop(0)
            for g in witness.generators:
                nxt = g(curr)
                if nxt not in orbit:
                    orbit.add(nxt)
                    queue.append(nxt)
        h1 = (len(orbit) == len(domain))
    except Exception:
        h1 = False

    try:
        if not h1:
            return [h1, False]
            
        degree = witness.degree
        domain = list(range(degree))
        
        # Left side: G is doubly transitive on Omega
        # 2-transitivity requires at least 2 elements.
        if degree < 2:
            left_side = False
        else:
            pairs = [(x, y) for x in domain for y in domain if x != y]
            start = pairs[0]
            orbit_pairs = {start}
            queue_pairs = [start]
            while queue_pairs:
                cx, cy = queue_pairs.pop(0)
                for g in witness.generators:
                    nx, ny = g(cx), g(cy)
                    if (nx, ny) not in orbit_pairs:
                        orbit_pairs.add((nx, ny))
                        queue_pairs.append((nx, ny))
            left_side = (len(orbit_pairs) == len(pairs))
            
        # Right side: G_alpha acts transitively on Omega \ {alpha}
        alpha = domain[0]
        G_alpha = witness.stabilizer(alpha)
        domain_minus = [x for x in domain if x != alpha]
        
        # Transitivity on an empty set is vacuously true.
        if not domain_minus:
            right_side = True
        else:
            start_m = domain_minus[0]
            orbit_m = {start_m}
            queue_m = [start_m]
            while queue_m:
                curr = queue_m.pop(0)
                for g in G_alpha.generators:
                    nxt = g(curr)
                    if nxt not in orbit_m:
                        orbit_m.add(nxt)
                        queue_m.append(nxt)
            right_side = (len(orbit_m) == len(domain_minus))
            
        conclusion = (left_side == right_side)
        neg_q = not conclusion
        
    except Exception:
        neg_q = False

    return [h1, neg_q]