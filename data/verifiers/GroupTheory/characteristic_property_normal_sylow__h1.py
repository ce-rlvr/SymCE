import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_bool_attr_or_method(obj, attr_name, *args):
    """Helper to safely extract and evaluate boolean attributes or methods."""
    if hasattr(obj, attr_name):
        attr = getattr(obj, attr_name)
        if callable(attr):
            try:
                return attr(*args)
            except TypeError:
                try:
                    return attr()
                except Exception:
                    pass
            except Exception:
                pass
        else:
            return attr
    return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            P = witness.get('P')
            p = witness.get('p')
        elif hasattr(witness, 'G') and hasattr(witness, 'P') and hasattr(witness, 'p'):
            G = witness.G
            P = witness.P
            p = witness.p
        else:
            G, P, p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    h2 = False
    try:
        res = get_bool_attr_or_method(P, 'is_sylow_p_subgroup', G, p)
        if res is None:
            res = get_bool_attr_or_method(G, 'is_sylow_p_subgroup', P, p)
        
        if res is not None:
            h2 = bool(res)
        else:
            # Fallback for finite groups (e.g., sympy PermutationGroup)
            if hasattr(P, 'is_subgroup') and P.is_subgroup(G):
                order_P = P.order()
                order_G = G.order()
                f = sympy.factorint(order_P)
                is_p_group = (len(f) == 0) or (len(f) == 1 and list(f.keys())[0] == p)
                if is_p_group and order_G != sympy.oo:
                    index = order_G // order_P
                    if index % p != 0:
                        h2 = True
    except Exception:
        h2 = False

    # H_3: P is a normal subgroup of G
    h3 = False
    try:
        res = get_bool_attr_or_method(P, 'is_normal', G)
        if res is None:
            res = get_bool_attr_or_method(G, 'is_normal', P)
        
        if res is not None:
            h3 = bool(res)
        else:
            # Fallback for finite groups
            if hasattr(P, 'is_subgroup') and P.is_subgroup(G):
                h3 = True
                for g in G.generators:
                    for h in P.generators:
                        if not P.contains(g * h * ~g):
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # neg_Q: P is NOT a characteristic subgroup of G
    neg_q = False
    try:
        is_char = None
        res = get_bool_attr_or_method(P, 'is_characteristic', G)
        if res is None:
            res = get_bool_attr_or_method(G, 'is_characteristic', P)
        
        if res is not None:
            is_char = bool(res)
        
        if is_char is not None:
            neg_q = not is_char
        else:
            # If we cannot determine characteristic property, we assume it is characteristic
            # (since for finite groups, a normal Sylow p-subgroup is ALWAYS characteristic).
            # A valid counterexample must explicitly report that it is not characteristic.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: P is a normal subgroup of G",
    "¬Q: P is not a characteristic subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3