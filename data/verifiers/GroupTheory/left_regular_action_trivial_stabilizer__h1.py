import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_G_op_y_e(witness):
    """
    Extracts the set G, the binary operation op, the element y, and the identity e
    from the witness. The witness can be a dictionary, an object with attributes,
    or a tuple of length 2, 3, or 4.
    """
    G, op, y, e = None, None, None, None
    
    if isinstance(witness, dict):
        G = witness.get('G')
        op = witness.get('op', lambda a, b: a * b)
        y = witness.get('y')
        e = witness.get('e')
    elif hasattr(witness, 'G') and hasattr(witness, 'y'):
        G = witness.G
        op = getattr(witness, 'op', lambda a, b: a * b)
        y = witness.y
        e = getattr(witness, 'e', None)
    elif isinstance(witness, tuple):
        if len(witness) == 4:
            G, op, y, e = witness
        elif len(witness) == 3:
            if callable(witness[1]):
                G, op, y = witness
            else:
                G, y, e = witness
                op = lambda a, b: a * b
        elif len(witness) == 2:
            G, y = witness
            op = lambda a, b: a * b
            
    if G is not None:
        try:
            G = list(G)
        except Exception:
            pass

    # If identity e is not provided, try to find it
    if G is not None and e is None and op is not None:
        for cand in G:
            try:
                if all(op(cand, x) == x and op(x, cand) == x for x in G):
                    e = cand
                    break
            except Exception:
                pass
                
    return G, op, y, e

def conditions(witness) -> list[bool]:
    G, op, y, e = get_G_op_y_e(witness)
    
    # H_1: G acts on itself by left multiplication
    # This requires G to be closed under the operation, the operation to be associative,
    # and the identity element e to act trivially (e * x = x).
    h1_ok = False
    try:
        if G is not None and op is not None and e is not None:
            h1_ok = True
            # Check closure
            for g in G:
                for x in G:
                    if op(g, x) not in G:
                        h1_ok = False
                        break
                if not h1_ok: break
            
            # Check associativity (action axiom: g1 * (g2 * x) == (g1 * g2) * x)
            if h1_ok:
                for g1 in G:
                    for g2 in G:
                        for x in G:
                            if op(g1, op(g2, x)) != op(op(g1, g2), x):
                                h1_ok = False
                                break
                        if not h1_ok: break
                    if not h1_ok: break
            
            # Check identity action (action axiom: e * x == x)
            if h1_ok:
                for x in G:
                    if op(e, x) != x:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # H_2: y is an element of G
    h2_ok = False
    try:
        if G is not None and y is not None:
            h2_ok = y in G
    except Exception:
        h2_ok = False

    # ¬Q: The stabilizer of y is not the trivial subgroup {e}
    neg_q_ok = False
    try:
        if G is not None and op is not None and y is not None and e is not None:
            stab = [g for g in G if op(g, y) == y]
            if len(stab) != 1 or stab[0] != e:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G acts on itself by left multiplication",
    "H_2: y is an element of G",
    "¬Q: The stabilizer of y is not the trivial subgroup {e}"
]

N_HYP = 2
NEG_Q_INDEX = 2