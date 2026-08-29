import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            m = witness.get('m')
            n = witness.get('n')
        else:
            G, m, n = witness
    except Exception:
        return [False, False]

    try:
        h1 = int(m) == m and int(n) == n and m >= 2 and n >= 2
    except Exception:
        h1 = False

    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            expected_order = n * (m ** n)
            if G.order() != expected_order:
                neg_q = True
            else:
                admits = False
                elements = list(G.generate())
                id_el = elements[0]**0 if elements else None
                for a in elements:
                    if a**n != id_el:
                        continue
                    for b in elements:
                        if b**m != id_el:
                            continue
                        rels_ok = True
                        for i in range(n):
                            for j in range(i+1, n):
                                x = (a**i) * b * (a**-i)
                                y = (a**j) * b * (a**-j)
                                if x * y != y * x:
                                    rels_ok = False
                                    break
                            if not rels_ok:
                                break
                        if rels_ok:
                            if PermutationGroup(a, b).order() == expected_order:
                                admits = True
                                break
                    if admits:
                        break
                neg_q = not admits
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m, n >= 2 are integers",
    "¬Q: G does not admit the presentation"
]

N_HYP = 1
NEG_Q_INDEX = 1