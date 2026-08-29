import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.ntheory import isprime, factorint

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

def extract_witness(witness):
    if isinstance(witness, dict):
        if 'p' in witness and 'q' in witness and 'G' in witness:
            return witness['p'], witness['q'], witness['G']
    if isinstance(witness, (list, tuple)):
        if len(witness) == 3:
            return witness[0], witness[1], witness[2]
    if hasattr(witness, 'order'):
        try:
            o = witness.order()
            factors = factorint(o)
            if len(factors) == 2 and all(v == 1 for v in factors.values()):
                p, q = list(factors.keys())
                return p, q, witness
        except Exception:
            pass
    raise ValueError("Invalid witness format")

def conditions(witness) -> list[bool]:
    try:
        p, q, G = extract_witness(witness)
    except Exception:
        return [False, False, False, False]

    try:
        h1_ok = bool(isprime(p) and isprime(q) and p != q)
    except Exception:
        h1_ok = False

    try:
        h2_ok = hasattr(G, 'order') and hasattr(G, 'center')
    except Exception:
        h2_ok = False

    try:
        h3_ok = bool(G.order() == p * q)
    except Exception:
        h3_ok = False

    try:
        neg_q_ok = bool(G.center().order() > 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "H_2: G is a group",
    "H_3: the order of G is pq",
    "¬Q: The center Z(G) is not the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3