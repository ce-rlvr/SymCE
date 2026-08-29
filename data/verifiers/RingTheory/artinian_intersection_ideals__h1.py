import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import symbols, Dummy, Poly, groebner
import math

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_dimensional(polys):
    if not polys:
        return False
    vars = set()
    for p in polys:
        if hasattr(p, 'free_symbols'):
            vars.update(p.free_symbols)
    vars = list(vars)
    if not vars:
        return True
    try:
        G = groebner(polys, *vars)
        for v in vars:
            found = False
            for p in G:
                poly = Poly(p, *vars)
                monoms = poly.monoms()
                if not monoms:
                    continue
                lm = monoms[0]
                idx = vars.index(v)
                if lm[idx] > 0 and sum(lm) == lm[idx]:
                    found = True
                    break
            if not found:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, I, J = witness
            elif len(witness) == 2:
                I, J = witness
            else:
                return [False, False, False, False]
                
            # Case 1: Ideals represented as integers (in ZZ)
            if isinstance(I, (int, sympy.Integer)) and isinstance(J, (int, sympy.Integer)):
                I = int(I)
                J = int(J)
                h1 = True
                h2 = (I != 0)
                h3 = (J != 0)
                intersect = abs(I * J) // math.gcd(I, J) if (I and J) else 0
                q = (intersect != 0)
                neg_q = not q
                return [h1, h2, h3, neg_q]
                
            # Case 2: Ideals represented as lists of SymPy polynomials
            if isinstance(I, list) and isinstance(J, list):
                h1 = True
                h2 = is_zero_dimensional(I)
                h3 = is_zero_dimensional(J)
                
                vars = set()
                for p in I + J:
                    if hasattr(p, 'free_symbols'):
                        vars.update(p.free_symbols)
                vars = list(vars)
                
                if not vars:
                    q = True
                else:
                    t = Dummy('t')
                    polys = [t * p for p in I] + [(1 - t) * q for q in J]
                    G = groebner(polys, t, *vars)
                    intersect = [p for p in G if not p.has(t)]
                    q = is_zero_dimensional(intersect)
                    
                neg_q = not q
                return [h1, h2, h3, neg_q]
                
            # Case 3: Ideals represented as sympy.polys.rings.Ideal objects
            if hasattr(I, 'intersect') and hasattr(I, 'ring'):
                h1 = True
                def is_zero_dim_ideal(ideal):
                    try:
                        G = ideal.groebner_basis()
                        ring = ideal.ring
                        gens = ring.gens
                        for i, v in enumerate(gens):
                            found = False
                            for p in G:
                                lm = p.LM
                                if lm[i] > 0 and sum(lm) == lm[i]:
                                    found = True
                                    break
                            if not found:
                                return False
                        return True
                    except Exception:
                        return False
                
                h2 = is_zero_dim_ideal(I)
                h3 = is_zero_dim_ideal(J)
                intersect = I.intersect(J)
                q = is_zero_dim_ideal(intersect)
                neg_q = not q
                return [h1, h2, h3, neg_q]
    except Exception:
        pass
        
    # Case 4: Custom witness objects
    try:
        h1 = bool(witness.is_ideal(witness.I) and witness.is_ideal(witness.J))
    except Exception:
        h1 = False
    try:
        h2 = bool(witness.quotient_is_artinian(witness.I))
    except Exception:
        h2 = False
    try:
        h3 = bool(witness.quotient_is_artinian(witness.J))
    except Exception:
        h3 = False
    try:
        intersect = witness.intersection(witness.I, witness.J)
        q = bool(witness.quotient_is_artinian(intersect))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: The quotient ring R/I is Artinian",
    "H_3: The quotient ring R/J is Artinian",
    "¬Q: The quotient ring R/(I \\cap J) is not Artinian"
]

N_HYP = 3
NEG_Q_INDEX = 3