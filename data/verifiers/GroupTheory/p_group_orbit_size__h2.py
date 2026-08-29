import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

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

def get_p(P):
    if hasattr(P, 'is_PermutationGroup') and P.is_PermutationGroup:
        order = P.order()
    elif isinstance(P, list) and all(hasattr(g, 'array_form') for g in P):
        G = PermutationGroup(P)
        order = G.order()
    else:
        order = len(list(P))
        
    if order == 1:
        return 2
    factors = factorint(order)
    if len(factors) == 1:
        return list(factors.keys())[0]
    return None

def conditions(witness) -> list[bool]:
    # H1: P is a finite p-group for some prime p
    try:
        P = witness[0]
        if hasattr(P, 'is_PermutationGroup') and P.is_PermutationGroup:
            order = P.order()
            h1 = (order == 1 or len(factorint(order)) == 1)
        elif isinstance(P, list) and all(hasattr(g, 'array_form') for g in P):
            G = PermutationGroup(P)
            if len(set(P)) != G.order():
                h1 = False
            else:
                order = G.order()
                h1 = (order == 1 or len(factorint(order)) == 1)
        else:
            order = len(list(P))
            h1 = (order == 1 or len(factorint(order)) == 1)
    except Exception:
        h1 = False

    # H2: P acts on X
    try:
        if len(witness) in (2, 3):
            P_obj = witness[0]
            h2 = (hasattr(P_obj, 'is_PermutationGroup') and P_obj.is_PermutationGroup) or \
                 (isinstance(P_obj, list) and all(isinstance(g, Permutation) for g in P_obj))
        elif len(witness) == 4:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: O is an orbit of the action of P on X
    try:
        if len(witness) == 2:
            P_obj, O = witness
            action = lambda g, x: g(x)
            gens = P_obj.generators if hasattr(P_obj, 'generators') else P_obj
        elif len(witness) == 3:
            P_obj, X, O = witness
            action = lambda g, x: g(x)
            gens = P_obj.generators if hasattr(P_obj, 'generators') else P_obj
        elif len(witness) == 4:
            P_obj, X, action, O = witness
            gens = P_obj.generators if hasattr(P_obj, 'generators') else P_obj
        else:
            gens = []
            O = []
            action = None
        
        if not O:
            h3 = False
        else:
            O_set = set(O)
            x = list(O_set)[0]
            
            orbit = set()
            queue = [x]
            orbit.add(x)
            
            while queue:
                curr = queue.pop(0)
                for g in gens:
                    next_val = action(g, curr)
                    if next_val not in orbit:
                        orbit.add(next_val)
                        queue.append(next_val)
            
            h3 = (orbit == O_set)
    except Exception:
        h3 = False

    # neg_Q: The cardinality of O is NOT equal to p^k for some non-negative integer k
    try:
        P_obj = witness[0]
        O = witness[-1]
        p = get_p(P_obj)
        if p is None:
            neg_q = False
        else:
            card_O = len(O)
            if card_O == 0:
                neg_q = True
            else:
                temp = card_O
                while temp % p == 0 and temp > 1:
                    temp //= p
                neg_q = (temp != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P is a finite p-group for some prime p",
    "H_2: P acts on X",
    "H_3: O is an orbit of the action of P on X",
    "¬Q: The cardinality of O is not equal to p^k for some non-negative integer k"
]

N_HYP = 3
NEG_Q_INDEX = 3