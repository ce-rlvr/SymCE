import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import re

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

def conditions(witness):
    is_orientable = True
    is_closed = True
    g = None
    
    try:
        if witness == sympy.oo:
            g = sympy.oo
        elif isinstance(witness, str):
            m = re.match(r'([SNU])_\{?(\d+)(?:,\s*(\d+))?\}?', witness)
            if m:
                surface_type = m.group(1)
                g = int(m.group(2))
                b = int(m.group(3)) if m.group(3) else 0
                if surface_type in ['N', 'U']:
                    is_orientable = False
                if b > 0:
                    is_closed = False
            elif witness in ["S_oo", "S_\infty", "S_infinity"]:
                g = sympy.oo
        elif isinstance(witness, tuple):
            if isinstance(witness[0], str) and isinstance(witness[1], int):
                g = witness[1]
                if "non" in witness[0].lower():
                    is_orientable = False
            else:
                g = witness[0]
                if len(witness) > 1:
                    if isinstance(witness[1], bool):
                        is_orientable = witness[1]
                    elif isinstance(witness[1], str):
                        if "non" in witness[1].lower():
                            is_orientable = False
                if len(witness) > 2:
                    if isinstance(witness[2], bool):
                        is_closed = witness[2]
                    elif isinstance(witness[2], str):
                        if "bound" in witness[2].lower() or "open" in witness[2].lower():
                            is_closed = False
        elif isinstance(witness, dict):
            if 'genus' in witness:
                g = witness['genus']
            elif 'g' in witness:
                g = witness['g']
            
            if 'is_orientable' in witness:
                is_orientable = witness['is_orientable']
            elif 'orientable' in witness:
                is_orientable = witness['orientable']
                
            if 'is_closed' in witness:
                is_closed = witness['is_closed']
            elif 'closed' in witness:
                is_closed = witness['closed']
        elif hasattr(witness, 'abelian_invariants'):
            invs = witness.abelian_invariants()
            zeros_count = sum(1 for x in invs if x == 0)
            twos_count = sum(1 for x in invs if x == 2)
            others_count = len(invs) - zeros_count - twos_count
            
            if others_count == 0 and twos_count == 1:
                g = zeros_count + 1
                is_orientable = False
                is_closed = True
            elif others_count == 0 and twos_count == 0 and zeros_count % 2 == 0:
                g = zeros_count // 2
                is_orientable = True
                is_closed = True
            else:
                g = witness
        elif hasattr(witness, 'genus'):
            g = witness.genus
            is_orientable = getattr(witness, 'is_orientable', True)
            is_closed = getattr(witness, 'is_closed', True)
        else:
            g = witness
    except Exception:
        pass

    try:
        if g == sympy.oo:
            h1 = True
        else:
            h1 = isinstance(g, int) and g >= 0
            if not is_orientable and g == 0:
                h1 = False
    except Exception:
        h1 = False

    try:
        if g == sympy.oo:
            q = False
        elif is_orientable and is_closed:
            q = True
        else:
            q = False
    except Exception:
        q = True

    return [h1, not q]

CONDITION_LABELS = ["H_1: G is the fundamental group pi_1(S_g)", "not Q: G does not admit the presentation"]
N_HYP = 1
NEG_Q_INDEX = 1