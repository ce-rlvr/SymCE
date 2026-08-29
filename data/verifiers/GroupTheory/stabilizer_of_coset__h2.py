import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_inv(x, identity, elements):
    try:
        return ~x
    except Exception:
        pass
    try:
        return x.inv()
    except Exception:
        pass
    try:
        return x**-1
    except Exception:
        pass
    for y in elements:
        if x * y == identity and y * x == identity:
            return y
    raise ValueError("No inverse found")

def conditions(witness):
    try:
        G, H, a = witness
    except Exception:
        return [False, False, False, False]

    try:
        if isinstance(G, PermutationGroup):
            h1 = True
            elements = list(G.elements)
            identity = G.identity
        else:
            elements = list(G)
            h1 = False
            if len(elements) > 0:
                identity = None
                for e in elements:
                    if all(e * x == x and x * e == x for x in elements):
                        identity = e
                        break
                if identity is not None:
                    h1 = True
                    for x in elements:
                        has_inv = False
                        for y in elements:
                            if x * y == identity and y * x == identity:
                                has_inv = True
                                break
                        if not has_inv:
                            h1 = False
                            break
                        for y in elements:
                            if not any(x * y == z for z in elements):
                                h1 = False
                                break
    except Exception:
        h1 = False
        elements = []
        identity = None

    try:
        h2 = all(any(h == e for e in elements) for h in H) and len(H) > 0
    except Exception:
        h2 = False

    try:
        h3 = any(a == e for e in elements)
    except Exception:
        h3 = False

    try:
        aH = []
        for h in H:
            val = a * h
            if not any(val == x for x in aH):
                aH.append(val)
                
        stabilizer = []
        for g in elements:
            gaH = []
            for x in aH:
                val = g * x
                if not any(val == y for y in gaH):
                    gaH.append(val)
            if len(gaH) == len(aH) and all(any(x == y for y in aH) for x in gaH):
                stabilizer.append(g)
                
        a_inv = get_inv(a, identity, elements)
        aHainv = []
        for h in H:
            val = (a * h) * a_inv
            if not any(val == x for x in aHainv):
                aHainv.append(val)
                
        is_subgroup = True
        if not any(identity == x for x in aHainv):
            is_subgroup = False
        else:
            for x in aHainv:
                x_inv = get_inv(x, identity, elements)
                if not any(x_inv == y for y in aHainv):
                    is_subgroup = False
                    break
                for y in aHainv:
                    xy = x * y
                    if not any(xy == z for z in aHainv):
                        is_subgroup = False
                        break
                        
        sets_equal = len(stabilizer) == len(aHainv) and all(any(x == y for y in aHainv) for x in stabilizer)
        
        conclusion = sets_equal and is_subgroup
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on the set of left cosets G/H by left multiplication",
    "H_3: aH is a left coset in G/H",
    "¬Q: The stabilizer of the coset aH under this action is not the conjugate subgroup aHa^{-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3