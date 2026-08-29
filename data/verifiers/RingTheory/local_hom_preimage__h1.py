import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def get_attr(w, name, default=None):
    if isinstance(w, dict):
        return w.get(name, default)
    return getattr(w, name, default)

def conditions(witness) -> list[bool]:
    try:
        R_raw = get_attr(witness, 'R')
        S_raw = get_attr(witness, 'S')
        m_R_raw = get_attr(witness, 'm_R')
        m_S_raw = get_attr(witness, 'm_S')
        add_R = get_attr(witness, 'add_R')
        mul_R = get_attr(witness, 'mul_R')
        add_S = get_attr(witness, 'add_S')
        mul_S = get_attr(witness, 'mul_S')
        f = get_attr(witness, 'f')
        
        if any(x is None for x in [R_raw, S_raw, add_R, mul_R, add_S, mul_S, f, m_R_raw, m_S_raw]):
            h1_ok = False
        else:
            R = list(R_raw)
            S = list(S_raw)
            m_R = list(m_R_raw)
            m_S = list(m_S_raw)
            
            def apply_f(x):
                if isinstance(f, dict): return f[x]
                return f(x)
                
            h1_ok = True
            
            # Check f preserves addition
            for x in R:
                for y in R:
                    if apply_f(add_R(x, y)) != add_S(apply_f(x), apply_f(y)):
                        h1_ok = False
                        break
                if not h1_ok: break
                
            # Check f preserves multiplication
            if h1_ok:
                for x in R:
                    for y in R:
                        if apply_f(mul_R(x, y)) != mul_S(apply_f(x), apply_f(y)):
                            h1_ok = False
                            break
                    if not h1_ok: break
                    
            # Check f(m_R) subset m_S
            if h1_ok:
                for x in m_R:
                    if apply_f(x) not in m_S:
                        h1_ok = False
                        break
                        
            # Check m_R and m_S are non-empty subsets
            if h1_ok:
                if not m_R or not m_S:
                    h1_ok = False
                if not all(x in R for x in m_R):
                    h1_ok = False
                if not all(x in S for x in m_S):
                    h1_ok = False
                    
            # Check m_R and m_S are ideals
            if h1_ok:
                for x in m_R:
                    for y in m_R:
                        if add_R(x, y) not in m_R:
                            h1_ok = False
                            break
                    if not h1_ok: break
                if h1_ok:
                    for x in m_R:
                        for r in R:
                            if mul_R(r, x) not in m_R or mul_R(x, r) not in m_R:
                                h1_ok = False
                                break
                        if not h1_ok: break
                if h1_ok:
                    for x in m_S:
                        for y in m_S:
                            if add_S(x, y) not in m_S:
                                h1_ok = False
                                break
                        if not h1_ok: break
                if h1_ok:
                    for x in m_S:
                        for s in S:
                            if mul_S(s, x) not in m_S or mul_S(x, s) not in m_S:
                                h1_ok = False
                                break
                        if not h1_ok: break
    except Exception:
        h1_ok = False

    try:
        R_raw = get_attr(witness, 'R')
        f = get_attr(witness, 'f')
        m_R_raw = get_attr(witness, 'm_R')
        m_S_raw = get_attr(witness, 'm_S')
        
        R = list(R_raw)
        m_R = list(m_R_raw)
        m_S = list(m_S_raw)
        
        def apply_f(x):
            if isinstance(f, dict): return f[x]
            return f(x)
            
        preimage = []
        for x in R:
            if apply_f(x) in m_S:
                preimage.append(x)
                
        # Check if preimage != m_R
        neg_q = False
        for x in preimage:
            if x not in m_R:
                neg_q = True
                break
        if not neg_q:
            for x in m_R:
                if x not in preimage:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a local ring homomorphism",
    "¬Q: The preimage f^{-1}(m_S) is not equal to m_R"
]

N_HYP = 1
NEG_Q_INDEX = 1