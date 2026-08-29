import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: m and n are non-zero integers",
    "¬Q: G does not admit the presentation < a, t | t a^m t^-1 = a^n >"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            m = witness.get('m')
            n = witness.get('n')
            G = witness.get('G')
        elif isinstance(witness, tuple) and len(witness) == 3:
            m, n, G = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: m and n are non-zero integers
    try:
        m_val = int(m)
        n_val = int(n)
        h1 = (m_val != 0) and (n_val != 0) and (m == m_val) and (n == n_val)
    except Exception:
        h1 = False
        
    # neg_Q: G does NOT admit the presentation
    try:
        q = False
        
        # Check if G is provided as a finitely presented group matching BS(m, n)
        if type(G).__name__ == 'FpGroup':
            if len(G.generators) == 2 and len(G.relators) == 1:
                rel = G.relators[0]
                # The relator t * a^m * t^-1 * a^-n has length 2 + |m| + |n|
                if len(rel) == 2 + abs(m_val) + abs(n_val):
                    q = True
                    
        # Check if G is provided as the standard matrix representation
        elif isinstance(G, list) and len(G) == 2:
            try:
                a, t_mat = G
                if hasattr(a, 'shape') and hasattr(t_mat, 'shape'):
                    expected_a = sympy.Matrix([[1, 1], [0, 1]])
                    expected_t = sympy.Matrix([[sympy.Rational(n_val, m_val), 0], [0, 1]])
                    if a == expected_a and t_mat == expected_t:
                        # The matrix group is isomorphic to BS(m, n) iff |m|=1 or |n|=1
                        if abs(m_val) == 1 or abs(n_val) == 1:
                            q = True
            except Exception:
                pass
                
        # For finite groups (like S3, Z4) and other non-isomorphic structures, q remains False.
        # BS(m, n) is always infinite, so no finite group admits its presentation.
        
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]