import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation

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

def conditions(witness):
    try:
        n, phi_dict = witness
    except Exception:
        return [False, False, False]
    
    # H_1: n is an integer >= 1
    try:
        n_val = int(n)
        h1 = (n_val == n) and (n_val >= 1)
        n = n_val
    except Exception:
        h1 = False

    # H_2: phi is an automorphism of Sn
    try:
        if not h1:
            h2 = False
        else:
            Sn = SymmetricGroup(n)
            
            def build_full_map(G, mapping):
                full_map = {G.identity: G.identity}
                queue = [G.identity]
                while queue:
                    u = queue.pop(0)
                    for g in G.generators:
                        if g not in mapping:
                            return None
                        v = u * g
                        val = full_map[u] * mapping[g]
                        if v in full_map:
                            if full_map[v] != val:
                                return None
                        else:
                            full_map[v] = val
                            queue.append(v)
                return full_map

            if callable(phi_dict):
                mapping = {g: phi_dict(g) for g in Sn.generators}
            elif isinstance(phi_dict, dict):
                mapping = phi_dict
            elif isinstance(phi_dict, (list, tuple)) and len(phi_dict) == len(Sn.generators):
                mapping = {Sn.generators[i]: phi_dict[i] for i in range(len(Sn.generators))}
            else:
                mapping = {}
                
            full_map = build_full_map(Sn, mapping)
            if full_map is None:
                h2 = False
            else:
                if len(full_map) == Sn.order() and len(set(full_map.values())) == Sn.order():
                    if all(val in Sn for val in full_map.values()):
                        h2 = True
                    else:
                        h2 = False
                else:
                    h2 = False
    except Exception:
        h2 = False

    # neg_Q: phi is not inner OR Aut(Sn) is not isomorphic to Sn
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            is_inner = False
            elements = list(Sn.generate())
            for g in elements:
                match1 = True
                match2 = True
                for gen in Sn.generators:
                    if full_map[gen] != g * gen * g**-1:
                        match1 = False
                    if full_map[gen] != g**-1 * gen * g:
                        match2 = False
                    if not match1 and not match2:
                        break
                if match1 or match2:
                    is_inner = True
                    break
            
            # It is a known mathematical fact that Aut(Sn) is isomorphic to Sn for all n except 2 and 6.
            aut_Sn_isomorphic_Sn = (n not in (2, 6))
            
            q = is_inner and aut_Sn_isomorphic_Sn
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer and S_n is the symmetric group on n letters",
    "H_2: phi is an automorphism of S_n",
    "¬Q: phi is not an inner automorphism, or Aut(S_n) is not isomorphic to S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2