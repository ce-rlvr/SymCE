import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    witness is expected to be a dictionary with:
      'R_n': integer n >= 0, representing the ring R = Z/nZ (or Z if n=0)
      'x': dict mapping G-elements (tuples of ints) to R-elements (ints)
      'y': dict mapping G-elements to R-elements, the inverse of x
    """
    try:
        R_n = int(witness['R_n'])
        x = witness['x']
        y = witness['y']
    except Exception:
        return [False, False, False]
        
    try:
        h1 = True
        keys = list(x.keys()) + list(y.keys())
        if not keys:
            h1 = False
        else:
            k = len(keys[0])
            for g in keys:
                if not isinstance(g, tuple):
                    h1 = False
                    break
                if len(g) != k:
                    h1 = False
                    break
                if not all(isinstance(i, (int, sympy.Integer)) for i in g):
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        h2 = R_n >= 0
        for v in list(x.values()) + list(y.values()):
            if not isinstance(v, (int, sympy.Integer)):
                h2 = False
                break
    except Exception:
        h2 = False

    try:
        def clean(d):
            res = {}
            for g, c in d.items():
                c = int(c)
                val = c % R_n if R_n > 0 else c
                if val != 0:
                    res[g] = val
            return res

        def mult(a, b):
            res = {}
            for g1, c1 in a.items():
                for g2, c2 in b.items():
                    g = tuple(int(i) + int(j) for i, j in zip(g1, g2))
                    c = int(c1) * int(c2)
                    val = c % R_n if R_n > 0 else c
                    res[g] = res.get(g, 0) + val
            return clean(res)

        x_clean = clean(x)
        y_clean = clean(y)
        
        xy = mult(x_clean, y_clean)
        yx = mult(y_clean, x_clean)
        
        k = len(list(x.keys())[0]) if x else 1
        id_g = tuple([0] * k)
        
        is_unit = (xy == {id_g: 1}) and (yx == {id_g: 1})
        
        not_ug = len(x_clean) > 1
        
        neg_q = is_unit and not_ug
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a torsion-free abelian group",
    "H_2: The group ring is formed over R",
    "¬Q: There exists a unit in the group ring not of the form u*g"
]

N_HYP = 2
NEG_Q_INDEX = 2