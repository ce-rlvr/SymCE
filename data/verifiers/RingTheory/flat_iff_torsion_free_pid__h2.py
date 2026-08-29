import sympy
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: M is flat but not torsion-free, or torsion-free but not flat"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_PID', False))
            is_flat = bool(witness.get('is_flat', False))
            is_torsion_free = bool(witness.get('is_torsion_free', False))
            neg_q = is_flat != is_torsion_free
            return [h1, neg_q]
            
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
            if hasattr(R, 'is_PID'):
                h1 = bool(R.is_PID)
            elif isinstance(R, dict):
                h1 = bool(R.get('is_PID', False))
                
            if hasattr(M, 'is_flat') and hasattr(M, 'is_torsion_free'):
                is_flat = bool(M.is_flat)
                is_torsion_free = bool(M.is_torsion_free)
                neg_q = is_flat != is_torsion_free
            elif isinstance(M, dict):
                is_flat = bool(M.get('is_flat', False))
                is_torsion_free = bool(M.get('is_torsion_free', False))
                neg_q = is_flat != is_torsion_free
            return [h1, neg_q]
            
        if hasattr(witness, 'is_PID'):
            h1 = bool(witness.is_PID)
        
        if hasattr(witness, 'is_flat') and hasattr(witness, 'is_torsion_free'):
            is_flat = bool(witness.is_flat)
            is_torsion_free = bool(witness.is_torsion_free)
            neg_q = is_flat != is_torsion_free
            
    except Exception:
        pass
        
    return [h1, neg_q]