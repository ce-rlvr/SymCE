import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_elements(G):
    return list(G.generate())

def get_identity(G):
    for g in get_elements(G):
        if g * g == g:
            return g
    return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            N = witness['N']
            H = witness['H']
            phi = witness['phi']
        elif len(witness) == 3:
            N, H, phi = witness
        elif len(witness) == 4:
            G, N, H, phi = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
    
    # H_1: G is the external semidirect product N ⋊_φ H
    h1_ok = False
    try:
        if hasattr(N, 'generate') and hasattr(H, 'generate'):
            N_elems = get_elements(N)
            H_elems = get_elements(H)
            h1_ok = True
            for h in H_elems:
                try:
                    mapping = phi(h) if callable(phi) else phi[h]
                except Exception:
                    h1_ok = False
                    break
                for n in N_elems:
                    try:
                        mapped_n = mapping(n) if callable(mapping) else mapping[n]
                    except Exception:
                        h1_ok = False
                        break
                    if mapped_n not in N_elems:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion fails
    neg_q = False
    try:
        if h1_ok:
            N_prime = N.derived_subgroup()
            N_elems = get_elements(N)
            Np_elems = get_elements(N_prime)
            
            cosets = []
            seen = set()
            for n in N_elems:
                if n not in seen:
                    coset = frozenset([n * x for x in Np_elems])
                    cosets.append(coset)
                    seen.update(coset)
            
            well_defined = True
            for h in get_elements(H):
                mapping = phi(h) if callable(phi) else phi[h]
                for C in cosets:
                    mapped_C = set((mapping(n) if callable(mapping) else mapping[n]) for n in C)
                    if not any(mapped_C.issubset(C2) for C2 in cosets):
                        well_defined = False
                        break
                if not well_defined:
                    break
            
            if not well_defined:
                neg_q = True
            else:
                phi_star = {}
                for h in get_elements(H):
                    star_map = {}
                    mapping = phi(h) if callable(phi) else phi[h]
                    for C in cosets:
                        n = next(iter(C))
                        mapped_n = mapping(n) if callable(mapping) else mapping[n]
                        for C2 in cosets:
                            if mapped_n in C2:
                                star_map[C] = C2
                                break
                    phi_star[h] = star_map
                
                op = {}
                for C1 in cosets:
                    for C2 in cosets:
                        n1 = next(iter(C1))
                        n2 = next(iter(C2))
                        n12 = n1 * n2
                        for C3 in cosets:
                            if n12 in C3:
                                op[(C1, C2)] = C3
                                break
                
                all_auto = True
                for h in get_elements(H):
                    star_map = phi_star[h]
                    if len(set(star_map.values())) != len(cosets):
                        all_auto = False
                        break
                    for C1 in cosets:
                        for C2 in cosets:
                            if star_map[op[(C1, C2)]] != op[(star_map[C1], star_map[C2])]:
                                all_auto = False
                                break
                        if not all_auto:
                            break
                    if not all_auto:
                        break
                
                if not all_auto:
                    neg_q = True
                else:
                    is_action = True
                    e_H = get_identity(H)
                    if e_H is None or e_H not in phi_star:
                        is_action = False
                    else:
                        for C in cosets:
                            if phi_star[e_H][C] != C:
                                is_action = False
                                break
                    
                    if is_action:
                        for h1 in get_elements(H):
                            for h2 in get_elements(H):
                                h12 = h1 * h2
                                for C in cosets:
                                    if phi_star[h12][C] != phi_star[h1][phi_star[h2][C]]:
                                        is_action = False
                                        break
                                if not is_action:
                                    break
                            if not is_action:
                                break
                    
                    if not is_action:
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is the external semidirect product N ⋊_φ H",
    "¬Q: H does not act on N/N' by well-defined group automorphisms φ*(h)"
]

N_HYP = 1
NEG_Q_INDEX = 1