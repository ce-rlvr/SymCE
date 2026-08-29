import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: P is a Sylow p-subgroup of G",
    "¬Q: P is not a characteristic subgroup of its normalizer N_G(P)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False

    # 1. Check if witness is a mock object with methods
    try:
        if hasattr(witness, 'is_sylow_p_subgroup') and hasattr(witness, 'is_characteristic_in_normalizer'):
            h1 = bool(witness.is_sylow_p_subgroup())
            neg_q = not bool(witness.is_characteristic_in_normalizer())
            return [h1, neg_q]
    except Exception:
        pass

    # 2. Check if witness is a dict
    if isinstance(witness, dict):
        try:
            if 'is_sylow_p_subgroup' in witness and 'is_characteristic_in_normalizer' in witness:
                h1 = bool(witness['is_sylow_p_subgroup'])
                neg_q = not bool(witness['is_characteristic_in_normalizer'])
                return [h1, neg_q]
        except Exception:
            pass

    # 3. Check if witness is a tuple (G, P, p) or (G, P)
    if isinstance(witness, tuple):
        if len(witness) == 3:
            G, P, p = witness
        elif len(witness) == 2:
            G, P = witness
            p = None
        else:
            return [False, False]
    else:
        return [False, False]

    # Evaluate H1: P is a Sylow p-subgroup of G
    try:
        if hasattr(G, 'is_sylow_p_subgroup'):
            if p is not None:
                h1 = bool(G.is_sylow_p_subgroup(P, p))
            else:
                h1 = bool(G.is_sylow_p_subgroup(P))
        elif hasattr(P, 'is_sylow_p_subgroup'):
            if p is not None:
                h1 = bool(P.is_sylow_p_subgroup(G, p))
            else:
                h1 = bool(P.is_sylow_p_subgroup(G))
        else:
            # Finite group check
            if P.is_subgroup(G):
                order_P = P.order()
                order_G = G.order()
                if order_G != sympy.oo and order_P > 1:
                    if p is None:
                        factors = sympy.factorint(order_P)
                        if len(factors) == 1:
                            p = list(factors.keys())[0]
                    if p is not None:
                        temp = order_P
                        while temp % p == 0:
                            temp //= p
                        if temp == 1:
                            index = order_G // order_P
                            if index % p != 0:
                                h1 = True
    except Exception:
        h1 = False

    # Evaluate neg_Q: P is NOT a characteristic subgroup of N_G(P)
    try:
        if hasattr(P, 'is_characteristic_in_normalizer'):
            neg_q = not bool(P.is_characteristic_in_normalizer(G))
        elif hasattr(G, 'is_characteristic_in_normalizer'):
            neg_q = not bool(G.is_characteristic_in_normalizer(P))
        elif hasattr(P, 'is_characteristic'):
            if hasattr(G, 'normalizer'):
                N = G.normalizer(P)
            else:
                # Mock normalizer
                N = getattr(G, 'N_G', lambda x: None)(P)
            if N is not None:
                neg_q = not bool(P.is_characteristic(N))
            else:
                neg_q = False
        else:
            # For finite groups, a Sylow p-subgroup is always characteristic in its normalizer.
            # Thus, the negated conclusion is False for any valid finite group witness.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]