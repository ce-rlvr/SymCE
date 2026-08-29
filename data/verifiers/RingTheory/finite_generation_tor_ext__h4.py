import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    """
    Check the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - R is a commutative Noetherian ring
      - M is a finitely generated R-module
      - N is a finitely generated R-module
    Conclusion:
      - Tor_i^R(M, N) and Ext^i_R(M, N) are finitely generated R-modules
    """
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        # Handle mock dictionary witnesses often used when SymPy lacks domain-specific structures
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative_noetherian', False))
            h2 = bool(witness.get('M_is_finitely_generated', False))
            h3 = bool(witness.get('N_is_finitely_generated', False))
            neg_q = not bool(witness.get('Tor_Ext_finitely_generated', True))
            return [h1, h2, h3, neg_q]
            
        # Handle object or tuple witnesses
        if hasattr(witness, 'R') and hasattr(witness, 'M') and hasattr(witness, 'N'):
            R = witness.R
            M = witness.M
            N = witness.N
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, M, N = witness
        else:
            return [False, False, False, False]
            
        # H_1: R is a commutative Noetherian ring
        if hasattr(R, 'is_commutative') and hasattr(R, 'is_Noetherian'):
            h1 = bool(R.is_commutative and R.is_Noetherian)
        elif hasattr(R, 'is_commutative_noetherian'):
            h1 = bool(R.is_commutative_noetherian)
            
        # H_2: M is a finitely generated R-module
        if hasattr(M, 'is_finitely_generated'):
            h2 = bool(M.is_finitely_generated)
            
        # H_3: N is a finitely generated R-module
        if hasattr(N, 'is_finitely_generated'):
            h3 = bool(N.is_finitely_generated)
            
        # ¬Q: Tor_i^R(M, N) and Ext^i_R(M, N) are NOT finitely generated R-modules
        if hasattr(witness, 'Tor_Ext_finitely_generated'):
            neg_q = not bool(witness.Tor_Ext_finitely_generated)
        else:
            # SymPy does not natively compute Tor and Ext for modules.
            # If no explicit flag is provided on the witness, we cannot verify the failure.
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: M is a finitely generated R-module",
    "H_3: N is a finitely generated R-module",
    "¬Q: Tor_i^R(M, N) and Ext^i_R(M, N) are not finitely generated R-modules"
]

N_HYP = 3
NEG_Q_INDEX = 3