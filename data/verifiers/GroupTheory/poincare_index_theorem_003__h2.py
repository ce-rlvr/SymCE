import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import math
from itertools import combinations

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_normal_subgroups(G):
    """Helper to find all normal subgroups of a PermutationGroup G."""
    try:
        elements = list(G.generate())
        classes = []
        unseen = set(elements)
        while unseen:
            x = unseen.pop()
            c_class = set()
            for g in elements:
                c_elem = g * x * (~g)
                c_class.add(c_elem)
            classes.append(c_class)
            unseen -= c_class
            
        id_elem = G.identity
        id_class = None
        for c in classes:
            if id_elem in c:
                id_class = c
                break
                
        if id_class is None:
            return []
                
        other_classes = [c for c in classes if c != id_class]
        
        normal_subgroups = []
        g_order = G.order()
        
        for r in range(len(other_classes) + 1):
            for combo in combinations(other_classes, r):
                subset = set(id_class)
                for c in combo:
                    subset.update(c)
                
                # Lagrange's theorem check
                if g_order % len(subset) != 0:
                    continue
                    
                is_subgroup = True
                # Check closure under inversion
                for a in subset:
                    if ~a not in subset:
                        is_subgroup = False
                        break
                        
                # Check closure under multiplication
                if is_subgroup:
                    for a in subset:
                        for b in subset:
                            if a * b not in subset:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                
                if is_subgroup:
                    normal_subgroups.append(subset)
                    
        return normal_subgroups
    except Exception:
        return []

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        elif isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G = getattr(witness, 'G', None)
            H = getattr(witness, 'H', None)
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: The index of H in G is a finite integer n
    try:
        if isinstance(H, PermutationGroup):
            h_size = H.order()
        else:
            h_size = len(H)
            
        n = G.order() / h_size
        h2_ok = (n == int(n))
    except Exception:
        h2_ok = False

    # neg_Q: There is NO normal subgroup K of G such that K is a subgroup of H and index of K in G divides n factorial
    try:
        conclusion_holds = False
        if isinstance(H, PermutationGroup):
            h_size = H.order()
            h_elements = set(H.generate())
        else:
            h_size = len(H)
            h_elements = set(H)
            
        n = G.order() / h_size
        if n == int(n):
            n = int(n)
            n_fact = math.factorial(n)
            
            normal_subgroups = get_normal_subgroups(G)
            
            for K_set in normal_subgroups:
                if K_set.issubset(h_elements):
                    idx = G.order() / len(K_set)
                    if idx == int(idx) and n_fact % int(idx) == 0:
                        conclusion_holds = True
                        break
                        
        neg_q_ok = not conclusion_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The index of H in G is a finite integer n",
    "¬Q: There is no normal subgroup K of G contained in H such that the index of K in G divides n factorial"
]

N_HYP = 2
NEG_Q_INDEX = 2