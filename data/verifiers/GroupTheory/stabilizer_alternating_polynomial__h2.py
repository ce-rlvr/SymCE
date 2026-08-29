import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup
from sympy.combinatorics.named_groups import CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        n = None
        p = None
        
        # Parse the witness which could be a tuple (n, p), a dict, a polynomial, a group, or just n.
        if isinstance(witness, (tuple, list)):
            if len(witness) >= 2:
                n = witness[0]
                p = witness[1]
            elif len(witness) == 1:
                n = witness[0]
                p = 2
        elif isinstance(witness, dict):
            n = witness.get('n', 2)
            p = witness.get('p', 2)
        elif hasattr(witness, 'domain') and hasattr(witness.domain, 'char'):
            p = witness.domain.char
            n = len(witness.gens)
        else:
            if hasattr(witness, 'degree'):
                n = witness.degree
                p = 2
            elif hasattr(witness, 'characteristic'):
                p = witness.characteristic()
                n = 2
            elif hasattr(witness, 'char'):
                p = witness.char
                n = 2
            else:
                n = witness
                p = 2
                
        # Extract characteristic if p is a field/domain object
        if hasattr(p, 'characteristic'):
            p = p.characteristic()
        elif hasattr(p, 'char'):
            p = p.char
            
        n = int(n)
        p = int(p)
        
        # H_1: S_n is the symmetric group on n letters, where n >= 2
        h1 = (n >= 2)
        
        # H_2: \Delta is the alternating polynomial (this is a definition, so it holds)
        h2 = True
        
        # Conclusion: The stabilizer of \Delta is A_n.
        # In characteristic p, \Delta is fixed by an odd permutation iff p == 2.
        # Thus, the stabilizer is S_n if p == 2, and A_n otherwise.
        # Since n >= 2, S_n != A_n.
        # The conclusion fails (stabilizer is NOT A_n) if and only if p == 2.
        neg_q = (p == 2)
        
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group on n letters, where n >= 2",
    "H_2: \Delta is the alternating polynomial",
    "¬Q: The stabilizer of \Delta is not the alternating group A_n"
]

N_HYP = 2
NEG_Q_INDEX = 2