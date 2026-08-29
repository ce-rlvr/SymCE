import math
from itertools import combinations
import sympy
from sympy import Matrix
from sympy.ntheory import factorint
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def extract_data(witness):
    ring_n, invs, elements = None, None, None
    
    # 1. Try dict
    if isinstance(witness, dict):
        ring_n = witness.get("ring_n", witness.get("R"))
        invs = witness.get("module_invs", witness.get("M"))
        elements = witness.get("elements", witness.get("m_i"))
    # 2. Try object attributes
    elif not isinstance(witness, (tuple, list)):
        ring_n = getattr(witness, "ring_n", getattr(witness, "R", None))
        invs = getattr(witness, "module_invs", getattr(witness, "M", None))
        elements = getattr(witness, "elements", getattr(witness, "m_i", None))
        
    if ring_n is not None and invs is not None and elements is not None:
        if isinstance(elements, list) and len(elements) > 0 and isinstance(elements[0], int):
            if isinstance(invs, list) and len(invs) == 1:
                elements = [[val] for val in elements]
        return ring_n, invs, elements

    # 3. Try iterable heuristics
    iterable = witness if isinstance(witness, (tuple, list)) else [witness]
    
    list_of_ints = []
    for item in iterable:
        if isinstance(item, int) and item >= 2 and ring_n is None:
            ring_n = item
        elif isinstance(item, list) and len(item) > 0 and all(isinstance(val, list) for val in item):
            elements = item
        elif isinstance(item, list) and all(isinstance(val, int) for val in item):
            list_of_ints.append(item)

    if invs is None and len(list_of_ints) > 0:
        invs = list_of_ints[0]
        
    if elements is None and len(list_of_ints) > 1:
        if len(invs) == 1:
            elements = [[val] for val in list_of_ints[1]]
        elif len(list_of_ints[1]) == 0:
            elements = []
            
    if elements is None and invs is not None and len(invs) == 1:
        for item in iterable:
            if isinstance(item, int) and item != ring_n:
                elements = [[item]]
                break
                
    if elements is None and len(list_of_ints) > 0 and list_of_ints[0] == []:
        elements = []

    return ring_n, invs, elements

def conditions(witness) -> list[bool]:
    ring_n, invs, elements = extract_data(witness)

    try:
        h1 = isinstance(ring_n, int) and ring_n >= 2
    except Exception:
        h1 = False

    try:
        if h1:
            factors = factorint(ring_n)
            h2 = len(factors) == 1
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        h3 = h2
    except Exception:
        h3 = False

    try:
        if isinstance(invs, list) and all(isinstance(x, int) and x >= 1 for x in invs):
            h4 = h1 and all(ring_n % x == 0 for x in invs)
        else:
            h4 = False
    except Exception:
        h4 = False

    try:
        if isinstance(elements, list) and isinstance(invs, list):
            h5 = True
            for el in elements:
                if not isinstance(el, list) or len(el) != len(invs):
                    h5 = False
                    break
                if not all(isinstance(x, int) for x in el):
                    h5 = False
                    break
        else:
            h5 = False
    except Exception:
        h5 = False

    try:
        if not (h4 and h5):
            neg_q = False
        else:
            k = len(invs)
            r = len(elements)
            if k == 0:
                generates = True
            elif math.comb(r + k, k) > 2000:
                generates = True
            else:
                rows = list(elements)
                for i in range(k):
                    row = [0] * k
                    row[i] = invs[i]
                    rows.append(row)
                
                A = Matrix(rows)
                gcd_minors = 0
                for row_indices in combinations(range(r + k), k):
                    submatrix = A.extract(row_indices, range(k))
                    det = int(abs(submatrix.det()))
                    gcd_minors = math.gcd(gcd_minors, det)
                    if gcd_minors == 1:
                        break
                generates = (gcd_minors == 1)
            neg_q = not generates
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring with maximal ideal m",
    "H_3: k is the residue field R/m",
    "H_4: M is a finitely generated R-module",
    "H_5: m_1, ..., m_n are elements of M",
    "¬Q: The elements m_1, ..., m_n do not generate M as an R-module"
]

N_HYP = 5
NEG_Q_INDEX = 5