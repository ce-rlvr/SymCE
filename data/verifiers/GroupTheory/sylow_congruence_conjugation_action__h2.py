import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: S is the set of all Sylow p-subgroups of G",
    "H_4: P acts on S by conjugation",
    "¬Q: The number of Sylow p-subgroups of G (the cardinality of S) is not congruent to 1 modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4

def get_all_subgroups(G, expected_order):
    if hasattr(G, 'subgroups'):
        try:
            subs = G.subgroups()
            return [H for H in subs if H.order() == expected_order]
        except Exception:
            pass

    elements = list(G.elements)
    id_elem = None
    for e in elements:
        if e * e == e:
            id_elem = e
            break
            
    if expected_order == 1:
        return [PermutationGroup([id_elem])]
        
    elements.remove(id_elem)
    subgroups = []
    
    for subset in itertools.combinations(elements, expected_order - 1):
        subset_set = set(subset)
        subset_set.add(id_elem)
        
        is_subgroup = True
        for x in subset:
            if ~x not in subset_set:
                is_subgroup = False
                break
        if not is_subgroup:
            continue
            
        for x in subset:
            for y in subset:
                if x * y not in subset_set:
                    is_subgroup = False
                    break
            if not is_subgroup:
                break
                
        if is_subgroup:
            subgroups.append(PermutationGroup(list(subset_set)))
            
    return subgroups

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, p, P = witness
                S_provided = False
            elif len(witness) == 4:
                G, p, P, S = witness
                S_provided = True
            else:
                return [False] * 5
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H1
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2
    try:
        if not isinstance(p, (int, sympy.Integer)) or p < 1:
            h2 = False
        elif not isinstance(P, PermutationGroup):
            h2 = False
        else:
            order_G = G.order()
            k = 0
            if p > 1:
                while order_G % (p**(k+1)) == 0:
                    k += 1
            expected_order = p**k
            h2 = P.is_subgroup(G) and P.order() == expected_order
    except Exception:
        h2 = False

    # H3
    try:
        if h1 and h2:
            expected_order = P.order()
            all_sylows = get_all_subgroups(G, expected_order)
            
            if S_provided:
                if not isinstance(S, (list, tuple, set)):
                    h3 = False
                else:
                    def get_elems(grp):
                        return frozenset(grp.elements)
                    set_S = {get_elems(H) for H in S if isinstance(H, PermutationGroup)}
                    set_all = {get_elems(H) for H in all_sylows}
                    h3 = (set_S == set_all)
            else:
                h3 = True
                S = all_sylows
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4
    try:
        if h1 and h2 and h3:
            h4 = True
            def get_elems(grp):
                return frozenset(grp.elements)
            set_S = {get_elems(H) for H in S}
            
            for x in P.elements:
                for H in S:
                    conj_elems = frozenset({x * h * (~x) for h in H.elements})
                    if conj_elems not in set_S:
                        h4 = False
                        break
                if not h4:
                    break
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q
    try:
        if h1 and h2 and h3:
            def get_elems(grp):
                return frozenset(grp.elements)
            unique_S = {get_elems(H) for H in S}
            neg_q = (len(unique_S) % p) != 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]