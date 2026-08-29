import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: Standard algebra objects
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def check_attr(obj, names):
    """Helper to safely check for attributes/methods on a witness object."""
    for name in names:
        if hasattr(obj, name):
            val = getattr(obj, name)
            if callable(val):
                try:
                    return val()
                except Exception:
                    continue
            return val
    return None

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    # H_1: Let R be a commutative ring
    try:
        res = check_attr(witness, [
            'is_commutative', 'is_commutative_ring', 'commutative',
            'R_is_commutative', 'is_comm'
        ])
        if res is not None:
            h1 = bool(res)
        elif isinstance(witness, dict):
            for k in ['is_commutative', 'is_commutative_ring', 'commutative', 'is_comm']:
                if k in witness:
                    h1 = bool(witness[k])
                    break
    except Exception:
        pass

    # H_2: Let I and J be comaximal ideals of R
    try:
        res = check_attr(witness, [
            'are_comaximal', 'is_comaximal', 'are_comaximal_ideals',
            'comaximal', 'I_J_comaximal'
        ])
        if res is not None:
            h2 = bool(res)
        elif hasattr(witness, 'I') and hasattr(witness, 'J'):
            if hasattr(witness.I, 'is_comaximal'):
                h2 = bool(witness.I.is_comaximal(witness.J))
        elif isinstance(witness, dict):
            for k in ['are_comaximal', 'is_comaximal', 'comaximal', 'are_comaximal_ideals']:
                if k in witness:
                    h2 = bool(witness[k])
                    break
    except Exception:
        pass

    # neg_Q: The torsion group Tor_n^R(R/I, R/J) is NOT the zero module
    try:
        res = check_attr(witness, [
            'is_Tor_zero', 'Tor_is_zero', 'is_zero_module', 'tor_zero',
            'is_tor_zero', 'tor_is_zero'
        ])
        if res is not None:
            neg_q = not bool(res)
        elif isinstance(witness, dict):
            for k in ['is_Tor_zero', 'Tor_is_zero', 'is_zero_module', 'tor_zero']:
                if k in witness:
                    neg_q = not bool(witness[k])
                    break
    except Exception:
        pass

    # Fallback for tuple-based witnesses: (R, I, J, ...)
    if isinstance(witness, tuple) and len(witness) >= 3:
        R = witness[0]
        I = witness[1]
        J = witness[2]
        
        if not h1:
            try:
                res = check_attr(R, ['is_commutative', 'is_commutative_ring', 'commutative'])
                if res is not None: 
                    h1 = bool(res)
            except Exception:
                pass
            
        if not h2:
            try:
                if hasattr(I, 'is_comaximal'):
                    h2 = bool(I.is_comaximal(J))
                elif hasattr(R, 'are_comaximal'):
                    h2 = bool(R.are_comaximal(I, J))
            except Exception:
                pass
            
        if not neg_q:
            try:
                res = check_attr(R, ['is_Tor_zero', 'Tor_is_zero', 'is_zero_module'])
                if res is not None:
                    neg_q = not bool(res)
            except Exception:
                pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are comaximal ideals of R",
    "¬Q: Tor_n^R(R/I, R/J) is not the zero module"
]

N_HYP = 2
NEG_Q_INDEX = 2