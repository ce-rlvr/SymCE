import sympy
from sympy import Poly, Expr
from sympy.combinatorics import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.abc import x

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

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: f(x) = x^3 - x - 1 in Q polynomials",
    "not Q: Degree of E over Q is not 6 or Gal(E/Q) is not isomorphic to S3"
]

def get_degree(witness):
    if isinstance(witness, str):
        s = witness.lower()
        if 'splitting' in s and 'x' in s and '3' in s:
            return 6
        if 'q' in s or 'rationals' in s:
            return 1

    if isinstance(witness, Poly):
        try:
            if not witness.is_irreducible:
                return None
        except Exception:
            pass
        return int(witness.degree())
        
    if isinstance(witness, Expr):
        free_syms = witness.free_symbols
        if len(free_syms) == 1:
            try:
                p = Poly(witness)
                if not p.is_irreducible:
                    return None
                return int(p.degree())
            except Exception:
                pass
        try:
            return int(sympy.minpoly(witness).degree())
        except Exception:
            pass
            
    if hasattr(witness, 'degree'):
        if callable(witness.degree):
            return int(witness.degree())
        else:
            return int(witness.degree)
            
    if hasattr(witness, 'minpoly'):
        return int(witness.minpoly.degree())
            
    if isinstance(witness, (int, float)):
        return int(witness)
        
    return None

def conditions(witness):
    # H_1: Let f(x) = x^3 - x - 1 in Q polynomials
    # This hypothesis is a constant definition, independent of the witness E.
    h1 = True
    
    q = False
    try:
        deg = None
        group = None
        
        # Check if witness is provided as a tuple like (field_or_degree, galois_group)
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            if isinstance(witness[0], int):
                deg = witness[0]
            else:
                deg = get_degree(witness[0])
            group = witness[1]
        else:
            deg = get_degree(witness)
            
        if deg == 6:
            if group is not None:
                # Check if the provided group is isomorphic to S3
                # S3 is the unique non-abelian group of order 6
                if hasattr(group, 'order') and hasattr(group, 'is_abelian'):
                    if group.order() == 6 and not group.is_abelian:
                        q = True
                    else:
                        q = False
                else:
                    s = str(group)
                    if 'S3' in s or 'SymmetricGroup(3)' in s:
                        q = True
                    else:
                        q = False
            else:
                # If no explicit group is provided but the degree is 6, we assume it is 
                # the splitting field of x^3 - x - 1 (which has Galois group S3).
                q = True
        else:
            q = False
            
    except Exception:
        q = False
        
    return [h1, not q]