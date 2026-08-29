import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from itertools import permutations

# Standard group bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    try:
        # H_1: G is a finite group
        # In SymPy, PermutationGroup instances are always finite groups.
        H_1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        H_1_ok = False
        
    try:
        if not H_1_ok:
            return [False, False]
            
        n = witness.order()
        
        # To prevent TLE on large groups, we restrict the size.
        # The intended counterexample (e.g., a non-regular embedding of V4) has n=4.
        if n > 8:
            return [H_1_ok, False]
            
        # 1. Construct the regular representation of W (which is isomorphic to W)
        elements = list(witness.generate())
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        reg_gens = []
        for g in witness.generators:
            p_array = [0] * n
            for i, x in enumerate(elements):
                p_array[i] = elem_to_idx[x * g]
            reg_gens.append(Permutation(p_array))
            
        if not reg_gens:
            reg_gens.append(Permutation(list(range(n))))
            
        reg_W = PermutationGroup(reg_gens)
        
        # 2. Helper to compute the normalizer of a subgroup in S_n
        def get_normalizer(G, degree):
            gens = G.generators
            if not gens:
                gens = [Permutation(list(range(degree)))]
                
            G_elements = set()
            for g in G.generate():
                arr = g.array_form
                if len(arr) < degree:
                    arr = arr + list(range(len(arr), degree))
                G_elements.add(tuple(arr))
                
            # If G moves points >= degree, it's not a subgroup of S_{degree}
            if any(len(arr) > degree for arr in G_elements):
                return None
                
            norm_elements = []
            for p_tuple in permutations(range(degree)):
                p_inv = [0] * degree
                for i, val in enumerate(p_tuple):
                    p_inv[val] = i
                    
                is_norm = True
                for g in gens:
                    g_array = g.array_form
                    if len(g_array) < degree:
                        g_array = g_array + list(range(len(g_array), degree))
                        
                    conj = tuple(p_tuple[g_array[p_inv[i]]] for i in range(degree))
                    if conj not in G_elements:
                        is_norm = False
                        break
                if is_norm:
                    norm_elements.append(Permutation(p_tuple))
            return PermutationGroup(norm_elements)
            
        # 3. Compute normalizers
        norm_W = get_normalizer(witness, n)
        
        if norm_W is None:
            # If the witness is not a valid subgroup of S_{|G|}, the premise fails
            neg_Q_ok = True
        else:
            # The normalizer of the regular representation is isomorphic to the holomorph
            norm_reg_W = get_normalizer(reg_W, n)
            
            if norm_W.order() != norm_reg_W.order():
                neg_Q_ok = True
            else:
                try:
                    neg_Q_ok = not norm_W.is_isomorphic(norm_reg_W)
                except AttributeError:
                    # Fallback if is_isomorphic is unavailable
                    neg_Q_ok = False
                    
    except Exception:
        neg_Q_ok = False
        
    return [H_1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The normalizer of \\rho(G) in the symmetric group S_{|G|} is not isomorphic to the holomorph of G"
]

N_HYP = 1
NEG_Q_INDEX = 1