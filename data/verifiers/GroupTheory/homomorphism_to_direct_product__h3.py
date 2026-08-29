import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "f is a group homomorphism if and only if both compositions pi_1 o f and pi_2 o f are group homomorphisms"
    """
    # Parse witness
    if isinstance(witness, dict):
        G = witness.get('G')
        H1 = witness.get('H1')
        H2 = witness.get('H2')
        f = witness.get('f')
        op = witness.get('op', None)
        pi1 = witness.get('pi1', lambda x: x[0])
        pi2 = witness.get('pi2', lambda x: x[1])
        op_G = witness.get('op_G', lambda a, b: a * b)
        op_H1 = witness.get('op_H1', lambda a, b: a * b)
        op_H2 = witness.get('op_H2', lambda a, b: a * b)
    else:
        try:
            G = witness[0]
            H1 = witness[1]
            H2 = witness[2]
            f = witness[3]
            op = witness[4] if len(witness) > 4 and witness[4] is not None else None
            pi1 = witness[5] if len(witness) > 5 and witness[5] is not None else lambda x: x[0]
            pi2 = witness[6] if len(witness) > 6 and witness[6] is not None else lambda x: x[1]
            op_G = witness[7] if len(witness) > 7 and witness[7] is not None else lambda a, b: a * b
            op_H1 = witness[8] if len(witness) > 8 and witness[8] is not None else lambda a, b: a * b
            op_H2 = witness[9] if len(witness) > 9 and witness[9] is not None else lambda a, b: a * b
        except Exception:
            return [False, False, False]

    # Default operation for H1 x H2 is component-wise multiplication
    if op is None:
        op = lambda a, b: (op_H1(a[0], b[0]), op_H2(a[1], b[1]))

    def evaluate_f(func, g):
        if isinstance(func, dict):
            return func[g]
        return func(g)

    def get_elements(grp):
        if hasattr(grp, 'elements'):
            return list(grp.elements)
        elif isinstance(grp, (list, tuple, set)):
            return list(grp)
        else:
            raise ValueError("Not a group")

    def in_group(val, grp):
        if hasattr(grp, 'elements'):
            return val in grp.elements
        return val in grp

    # H_1: G, H1, and H2 are groups
    try:
        get_elements(G)
        get_elements(H1)
        get_elements(H2)
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: f is a function from G to H1 x H2
    try:
        h2_ok = True
        elements = get_elements(G)
        for g in elements:
            val = evaluate_f(f, g)
            v1 = pi1(val)
            v2 = pi2(val)
            if not in_group(v1, H1) or not in_group(v2, H2):
                h2_ok = False
                break
    except Exception:
        h2_ok = False

    # neg_Q: f is a group homomorphism is NOT equivalent to both pi_1 o f and pi_2 o f being group homomorphisms
    try:
        elements = get_elements(G)
        
        # Check if f is a homomorphism
        f_is_hom = True
        for g1 in elements:
            for g2 in elements:
                g12 = op_G(g1, g2)
                val1 = evaluate_f(f, g1)
                val2 = evaluate_f(f, g2)
                val12 = evaluate_f(f, g12)
                if val12 != op(val1, val2):
                    f_is_hom = False
                    break
            if not f_is_hom:
                break
                
        # Check if pi_1 o f is a homomorphism
        pi1_is_hom = True
        for g1 in elements:
            for g2 in elements:
                g12 = op_G(g1, g2)
                v1 = pi1(evaluate_f(f, g1))
                v2 = pi1(evaluate_f(f, g2))
                v12 = pi1(evaluate_f(f, g12))
                if v12 != op_H1(v1, v2):
                    pi1_is_hom = False
                    break
            if not pi1_is_hom:
                break

        # Check if pi_2 o f is a homomorphism
        pi2_is_hom = True
        for g1 in elements:
            for g2 in elements:
                g12 = op_G(g1, g2)
                v1 = pi2(evaluate_f(f, g1))
                v2 = pi2(evaluate_f(f, g2))
                v12 = pi2(evaluate_f(f, g12))
                if v12 != op_H2(v1, v2):
                    pi2_is_hom = False
                    break
            if not pi2_is_hom:
                break
                
        both_pi_hom = pi1_is_hom and pi2_is_hom
        
        # The conclusion fails if the equivalence does not hold
        neg_q = (f_is_hom != both_pi_hom)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G, H1, and H2 are groups",
    "H_2: f is a function from G to H1 x H2",
    "¬Q: f is a group homomorphism is not equivalent to both pi_1 o f and pi_2 o f being group homomorphisms"
]

N_HYP = 2
NEG_Q_INDEX = 2