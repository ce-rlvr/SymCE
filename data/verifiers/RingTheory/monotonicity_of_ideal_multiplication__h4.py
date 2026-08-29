import sympy
from sympy import symbols, QQ, ZZ
from sympy.polys.domains.ring import Ring
from sympy.polys.rings import PolyRing

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "H_4: I is a subset of J",
    "¬Q: IK is not a subset of JK"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
            K = witness.get('K')
        else:
            R, I, J, K = witness
    except Exception:
        return [False] * 5

    # H1: R is a ring
    try:
        h1 = False
        if hasattr(R, 'is_Ring') and R.is_Ring:
            h1 = True
        elif hasattr(R, 'ideal'):
            h1 = True
        elif isinstance(R, (Ring, PolyRing)):
            h1 = True
    except Exception:
        h1 = False

    # H2: I is an ideal of R
    try:
        h2 = False
        if hasattr(I, 'ring') and I.ring == R:
            h2 = True
        elif hasattr(I, 'gens') and hasattr(I, 'contains'):
            h2 = True
    except Exception:
        h2 = False

    # H3: J is an ideal of R
    try:
        h3 = False
        if hasattr(J, 'ring') and J.ring == R:
            h3 = True
        elif hasattr(J, 'gens') and hasattr(J, 'contains'):
            h3 = True
    except Exception:
        h3 = False

    # H4: I \subseteq J
    try:
        h4 = False
        if hasattr(I, 'gens') and hasattr(J, 'contains'):
            h4 = all(bool(J.contains(g)) for g in I.gens)
        elif hasattr(I, 'subset'):
            h4 = bool(I.subset(J))
    except Exception:
        h4 = False

    # neg_Q: IK \not\subseteq JK
    try:
        neg_q = False
        
        # Compute IK
        try:
            IK = I * K
        except Exception:
            if hasattr(K, 'gens'):
                gens_IK = [i * k for i in I.gens for k in K.gens]
            else:
                gens_IK = [i * K for i in I.gens]
            IK = R.ideal(*gens_IK)
            
        # Compute JK
        try:
            JK = J * K
        except Exception:
            if hasattr(K, 'gens'):
                gens_JK = [j * k for j in J.gens for k in K.gens]
            else:
                gens_JK = [j * K for j in J.gens]
            JK = R.ideal(*gens_JK)
            
        # Check if IK is NOT a subset of JK
        if hasattr(IK, 'gens') and hasattr(JK, 'contains'):
            neg_q = any(not bool(JK.contains(g)) for g in IK.gens)
        elif hasattr(IK, 'subset'):
            neg_q = not bool(IK.subset(JK))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]