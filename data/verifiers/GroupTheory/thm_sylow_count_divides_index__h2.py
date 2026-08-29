import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def highest_power(n, p):
    if p <= 1: 
        return 0
    k = 0
    while n % (p**(k+1)) == 0:
        k += 1
    return p**k

def get_n_p(G, p):
    p_val = int(p)
    target_order = highest_power(G.order(), p_val)
    
    if sympy.isprime(p_val):
        P_one = None
        if hasattr(G, 'sylow_subgroup'):
            try:
                P_one = G.sylow_subgroup(p_val)
            except Exception:
                pass
                
        if P_one is None or P_one.order() != target_order:
            elements = list(G.elements)
            for g in elements:
                H = PermutationGroup([g])
                if H.order() == target_order:
                    P_one = H
                    break
            if P_one is None:
                for i in range(len(elements)):
                    for j in range(i+1, len(elements)):
                        H = PermutationGroup([elements[i], elements[j]])
                        if H.order() == target_order:
                            P_one = H
                            break
                    if P_one is not None:
                        break
                        
        if P_one is None or P_one.order() != target_order:
            return 0
            
        P_set = set(P_one.elements)
        normalizer_order = 0
        for g in list(G.elements):
            g_inv = g**-1
            is_in_normalizer = True
            for h in P_one.generators:
                if g * h * g_inv not in P_set:
                    is_in_normalizer = False
                    break
            if is_in_normalizer:
                normalizer_order += 1
                
        return G.order() // normalizer_order
    else:
        elements = list(G.elements)
        subgroups = set()
        
        def sig(H_elements):
            return tuple(sorted([tuple(g.array_form) for g in H_elements]))
            
        for g in elements:
            H = PermutationGroup([g])
            if H.order() == target_order:
                subgroups.add(sig(list(H.elements)))
                
        n_elements = len(elements)
        if n_elements <= 60:
            for i in range(n_elements):
                for j in range(i+1, n_elements):
                    H = PermutationGroup([elements[i], elements[j]])
                    if H.order() == target_order:
                        subgroups.add(sig(list(H.elements)))
                        
        if target_order >= 8 and n_elements <= 24:
            for i in range(n_elements):
                for j in range(i+1, n_elements):
                    for k in range(j+1, n_elements):
                        H = PermutationGroup([elements[i], elements[j], elements[k]])
                        if H.order() == target_order:
                            subgroups.add(sig(list(H.elements)))
                            
        return len(subgroups)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            P = witness.get('P')
            n_p = witness.get('n_p')
        else:
            G, p, P, n_p = witness
            
        def is_integer(x):
            return isinstance(x, int) or isinstance(x, sympy.Integer)
            
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
        
        if not is_integer(p) or p <= 1 or not h1:
            h2 = False
        else:
            p_val = int(p)
            actual_n_p = get_n_p(G, p_val)
            h2 = (actual_n_p is not None and is_integer(n_p) and int(n_p) == actual_n_p)
            
        if not is_integer(p) or p <= 1 or not h1:
            h3 = False
        else:
            p_val = int(p)
            target_order = highest_power(G.order(), p_val)
            if isinstance(P, PermutationGroup) and P.order() == target_order:
                h3 = all(g in G for g in P.generators)
            else:
                h3 = False
                
        if h1 and h3 and is_integer(n_p):
            n_p_val = int(n_p)
            index = G.order() // P.order()
            if n_p_val == 0:
                neg_q = True
            else:
                neg_q = (index % n_p_val != 0)
        else:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: n_p is the number of Sylow p-subgroups of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: n_p does not divide the index of P in G"
]

N_HYP = 3
NEG_Q_INDEX = 3