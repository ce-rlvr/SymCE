import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness) -> list[bool]:
    # 1. Torsion-free
    try:
        tf = False
        if isinstance(witness, dict) and 'is_torsion_free' in witness:
            tf = bool(witness['is_torsion_free'])
        elif hasattr(witness, 'is_torsion_free'):
            tf = bool(witness.is_torsion_free)
        elif hasattr(witness, 'order'):
            tf = (witness.order() == 1)
        else:
            w_str = str(witness).lower()
            if 'heisenberg' in w_str or 'unipotent' in w_str:
                tf = True
    except Exception:
        tf = False

    # 2. Divisible
    try:
        div = False
        if isinstance(witness, dict) and 'is_divisible' in witness:
            div = bool(witness['is_divisible'])
        elif hasattr(witness, 'is_divisible'):
            div = bool(witness.is_divisible)
        elif hasattr(witness, 'order'):
            div = (witness.order() == 1)
        else:
            w_str = str(witness).lower()
            if 'heisenberg' in w_str or 'unipotent' in w_str:
                if any(x in w_str for x in ['q', 'rational', 'real', 'complex', '(r)', '(c)', ' r ', ' c ']):
                    div = True
    except Exception:
        div = False

    # 3. Isomorphic to Q-vector space
    try:
        q_vs = False
        is_ab = None
        if isinstance(witness, dict) and 'is_abelian' in witness:
            is_ab = bool(witness['is_abelian'])
        elif hasattr(witness, 'is_abelian'):
            is_ab = bool(witness.is_abelian)
            
        if isinstance(witness, dict) and 'is_Q_vs' in witness:
            q_vs = bool(witness['is_Q_vs'])
        elif hasattr(witness, 'is_Q_vs'):
            q_vs = bool(witness.is_Q_vs)
        elif hasattr(witness, 'is_isomorphic_to_Q_vs'):
            q_vs = bool(witness.is_isomorphic_to_Q_vs)
        elif is_ab is False:
            q_vs = False
        elif hasattr(witness, 'order'):
            q_vs = (witness.order() == 1)
        else:
            w_str = str(witness).lower()
            if 'heisenberg' in w_str or 'unipotent' in w_str:
                q_vs = False
    except Exception:
        q_vs = False

    try:
        # The conclusion is an equivalence: G is torsion-free and divisible iff G is isomorphic to a Q-vector space.
        p = tf and div
        conclusion = (p == q_vs)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G is not (torsion-free and divisible iff isomorphic to a Q-vector space)"
]
N_HYP = 0
NEG_Q_INDEX = 0