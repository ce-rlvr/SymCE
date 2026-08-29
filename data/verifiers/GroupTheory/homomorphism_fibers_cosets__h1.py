import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

CONDITION_LABELS = [
    "H_1: f: G \\to H is a group homomorphism",
    "H_2: x and y are elements of G",
    "¬Q: f(x) = f(y) is not equivalent to x^{-1}y \\in \\ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def eval_f(f, z):
    if hasattr(f, '__call__'):
        return f(z)
    elif isinstance(f, dict):
        return f[z]
    else:
        raise ValueError("f must be callable or dict")

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            f = witness['f']
            x = witness['x']
            y = witness['y']
        elif len(witness) == 5:
            G, H, f, x, y = witness
        elif len(witness) == 3:
            f, x, y = witness
            G = f.domain
            H = f.codomain
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: f is a group homomorphism
    h1_ok = False
    try:
        if hasattr(f, 'domain') and hasattr(f, 'codomain') and hasattr(f, 'kernel'):
            h1_ok = (f.domain == G and f.codomain == H)
        else:
            if hasattr(G, 'elements') and hasattr(H, 'elements'):
                e_G = G.identity if hasattr(G, 'identity') else 0
                e_H = H.identity if hasattr(H, 'identity') else 0
                
                if eval_f(f, e_G) == e_H:
                    is_hom = True
                    for a in G.elements:
                        for b in G.elements:
                            try:
                                ab = a * b
                            except Exception:
                                ab = a + b
                                
                            try:
                                fa_fb = eval_f(f, a) * eval_f(f, b)
                            except Exception:
                                fa_fb = eval_f(f, a) + eval_f(f, b)
                                
                            if eval_f(f, ab) != fa_fb:
                                is_hom = False
                                break
                        if not is_hom:
                            break
                    h1_ok = is_hom
            else:
                h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: x and y are elements of G
    h2_ok = False
    try:
        if hasattr(G, 'contains'):
            h2_ok = bool(G.contains(x) and G.contains(y))
        elif hasattr(G, 'elements'):
            h2_ok = bool(x in G.elements and y in G.elements)
        else:
            h2_ok = bool(x in G and y in G)
    except Exception:
        h2_ok = False

    # neg_Q: f(x) = f(y) is NOT equivalent to x^{-1}y \in \ker(f)
    neg_q_ok = False
    try:
        fx = eval_f(f, x)
        fy = eval_f(f, y)
        
        try:
            z = x**-1 * y
        except Exception:
            try:
                z = (~x) * y
            except Exception:
                z = -x + y
            
        fz = eval_f(f, z)
        
        if hasattr(H, 'identity'):
            e_H = H.identity
        elif hasattr(f, 'codomain') and hasattr(f.codomain, 'identity'):
            e_H = f.codomain.identity
        else:
            if hasattr(G, 'identity'):
                e_H = eval_f(f, G.identity)
            else:
                e_H = eval_f(f, 0)
            
        in_ker = bool(fz == e_H)
        lhs = bool(fx == fy)
        rhs = in_ker
        
        neg_q_ok = bool(lhs != rhs)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]