import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to provide the group G, and the sequences d and e.
    It can be a dictionary {'G': G, 'd': d, 'e': e} or a tuple (G, d, e).
    """
    G = None
    d = None
    e = None
    
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            d = witness.get('d')
            e = witness.get('e')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, d, e = witness
            elif len(witness) == 5:
                # In case the witness includes r and s explicitly: (G, s, e, r, d)
                G, _, e, _, d = witness
    except Exception:
        pass

    # H1: G is a finite abelian group
    h1_ok = False
    try:
        if G is not None:
            is_ab = getattr(G, 'is_abelian', False)
            if callable(is_ab):
                is_ab = is_ab()
            if is_ab:
                # Check finiteness
                if hasattr(G, 'order'):
                    order = G.order() if callable(G.order) else G.order
                    if order < float('inf'):
                        h1_ok = True
                else:
                    # Assume finite if it's a permutation group without an explicit infinite order
                    h1_ok = True
    except Exception:
        pass

    # H2: G is isomorphic to the direct sum of Z_{e_j} where e_j > 1 and e_j | e_{j+1}
    h2_ok = False
    try:
        if G is not None and e is not None and hasattr(G, 'abelian_invariants'):
            is_ab = getattr(G, 'is_abelian', False)
            if callable(is_ab):
                is_ab = is_ab()
            if is_ab:
                if isinstance(e, (int, sympy.Integer)):
                    e_list = [int(e)]
                else:
                    e_list = [int(x) for x in e]
                
                if all(x > 1 for x in e_list):
                    divides_ok = True
                    for i in range(1, len(e_list)):
                        if e_list[i] % e_list[i-1] != 0:
                            divides_ok = False
                            break
                    if divides_ok:
                        invs = [int(x) for x in G.abelian_invariants()]
                        if invs == e_list:
                            h2_ok = True
    except Exception:
        pass

    # neg_Q: It is NOT the case that r = s and d_i = e_i for all i
    # This means the sequence d is not equal to the sequence e.
    neg_q_ok = False
    try:
        if d is not None and e is not None:
            if isinstance(d, (int, sympy.Integer)):
                d_list = [int(d)]
            else:
                d_list = [int(x) for x in d]
                
            if isinstance(e, (int, sympy.Integer)):
                e_list = [int(e)]
            else:
                e_list = [int(x) for x in e]
                
            if d_list != e_list:
                neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite abelian group",
    "H_2: G is isomorphic to the direct sum of Z_{e_j} where e_j > 1 and e_j | e_{j+1}",
    "¬Q: It is not the case that r = s and d_i = e_i for all i"
]

N_HYP = 2
NEG_Q_INDEX = 2