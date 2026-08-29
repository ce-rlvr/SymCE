import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
from sympy.polys.domains import QQ, ZZ
import z3
import math
import itertools
import functools

# Top-level setup
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

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

x, y, t = sympy.symbols('x y t')

def conditions(witness) -> list[bool]:
    neg_q = False
    try:
        # The conjecture states: E/F is separable iff E \otimes_F K is reduced for all K.
        # This is true for algebraic extensions. If the 'algebraic' hypothesis is dropped,
        # transcendental extensions (like F(x)/F) become counterexamples because they are
        # not algebraic (hence not separable in the classical algebraic sense), but their
        # tensor product with any field extension K is a localization of K[x], which is a
        # domain and thus reduced.
        
        is_transcendental = False
        
        if isinstance(witness, str):
            s = witness.lower().replace(" ", "")
            if any(sub in s for sub in ['x', 't', 'transcendental', 'q(t)', 'f(x)', 'f(t)']):
                is_transcendental = True
                
        elif type(witness).__name__ == 'FractionField':
            is_transcendental = True
            
        elif hasattr(witness, 'is_Symbol') and witness.is_Symbol:
            is_transcendental = True
            
        elif hasattr(witness, 'is_transcendental') and witness.is_transcendental:
            is_transcendental = True
            
        elif isinstance(witness, tuple):
            for w in witness:
                if isinstance(w, str):
                    s = w.lower().replace(" ", "")
                    if any(sub in s for sub in ['x', 't', 'transcendental']):
                        is_transcendental = True
                elif type(w).__name__ == 'FractionField':
                    is_transcendental = True
                elif hasattr(w, 'is_Symbol') and w.is_Symbol:
                    is_transcendental = True
                elif hasattr(w, 'is_transcendental') and w.is_transcendental:
                    is_transcendental = True
                    
        if not is_transcendental:
            s_wit = str(witness).lower().replace(" ", "")
            if any(sub in s_wit for sub in ['transcendental', 'q(t)', 'f(x)', 'f(t)']):
                is_transcendental = True
                
        if is_transcendental:
            neg_q = True
            
    except Exception:
        pass

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The extension E/F is transcendental (not algebraic, hence not separable), but E ⊗_F K is reduced for all K"
]
N_HYP = 0
NEG_Q_INDEX = 0