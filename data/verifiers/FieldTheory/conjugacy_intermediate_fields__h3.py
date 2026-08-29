import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The dropped hypothesis from the true theorem is that M_1 and M_2 are subfields of L.
    Without this, H_1 and H_2 can be conjugate (e.g., both equal to G) while M_1 and M_2 
    are completely unrelated and non-conjugate extensions over K.
    """
    try:
        # Handle dictionary-based mock witnesses
        if isinstance(witness, dict):
            h1 = bool(witness.get('L_is_finite_Galois', False))
            h2 = bool(witness.get('G_is_Galois_group', False))
            h3 = bool(witness.get('H1_H2_fix_M1_M2', False))
            m_conj = bool(witness.get('M1_M2_conjugate', False))
            h_conj = bool(witness.get('H1_H2_conjugate', False))
            
        # Handle tuple/list-based mock witnesses
        elif isinstance(witness, (list, tuple)):
            if len(witness) >= 5:
                h1 = bool(witness[0])
                h2 = bool(witness[1])
                h3 = bool(witness[2])
                m_conj = bool(witness[3])
                h_conj = bool(witness[4])
            else:
                return [False, False, False, False]
                
        # Handle object-based mock witnesses
        else:
            def get_val(obj, name):
                val = getattr(obj, name, False)
                return val() if callable(val) else val
                
            h1 = bool(get_val(witness, 'L_is_finite_Galois'))
            h2 = bool(get_val(witness, 'G_is_Galois_group'))
            h3 = bool(get_val(witness, 'H1_H2_fix_M1_M2'))
            m_conj = bool(get_val(witness, 'M1_M2_conjugate'))
            h_conj = bool(get_val(witness, 'H1_H2_conjugate'))
            
        # The conclusion is an equivalence. Its negation is True if the two sides differ.
        neg_q = (m_conj != h_conj)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: G is the Galois group of L/K",
    "H_3: H_1 and H_2 are the subgroups of G fixing M_1 and M_2 respectively",
    "¬Q: The equivalence (M_1 and M_2 are conjugate over K iff H_1 and H_2 are conjugate in G) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3