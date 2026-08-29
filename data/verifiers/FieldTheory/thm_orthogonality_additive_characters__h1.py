import sympy
from sympy import simplify
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices

# Top-level setup for potential witness elements
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def check_equal(a, b):
    if a == b:
        return True
    try:
        if simplify(a - b) == 0:
            return True
    except Exception:
        pass
    return False

def check_zero(a):
    if a == 0:
        return True
    try:
        if simplify(a) == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness should provide the addition table of F and the character values.
    Supported formats for witness:
      - tuple: (F_add_table, psi_values)
      - tuple: (elements, F_add_table, psi_values)
      - dict: {'add_table': ..., 'psi': ..., 'elements': ...}
      - object with attributes: add_table, psi, elements
    """
    try:
        elements = None
        if isinstance(witness, tuple):
            if len(witness) == 3:
                elements, F_add, psi = witness
            elif len(witness) == 2:
                F_add, psi = witness
            else:
                return [False, False]
        elif hasattr(witness, 'add_table') and hasattr(witness, 'psi'):
            F_add = witness.add_table
            psi = witness.psi
            if hasattr(witness, 'elements'):
                elements = witness.elements
        elif isinstance(witness, dict):
            F_add = witness.get('add_table')
            psi = witness.get('psi')
            elements = witness.get('elements')
        else:
            return [False, False]

        if elements is None:
            if isinstance(F_add, dict):
                elements = list(F_add.keys())
            elif isinstance(psi, dict):
                elements = list(psi.keys())
            elif isinstance(psi, (list, tuple)):
                elements = list(range(len(psi)))
            else:
                return [False, False]

        # Normalize psi to a dictionary mapping element -> value
        if callable(psi):
            psi_dict = {x: psi(x) for x in elements}
        elif isinstance(psi, (list, tuple)):
            psi_dict = {elements[i]: psi[i] for i in range(len(elements))}
        elif isinstance(psi, dict):
            psi_dict = psi
        else:
            return [False, False]

        # Normalize F_add to a dictionary of dictionaries mapping (x, y) -> x+y
        if callable(F_add):
            F_add_dict = {x: {y: F_add(x, y) for y in elements} for x in elements}
        elif isinstance(F_add, (list, tuple)):
            F_add_dict = {elements[i]: {elements[j]: F_add[i][j] for j in range(len(elements))} for i in range(len(elements))}
        elif isinstance(F_add, dict):
            F_add_dict = F_add
        else:
            return [False, False]

        # H1: psi is a non-trivial additive character of F
        is_hom = True
        for x in elements:
            for y in elements:
                if x not in F_add_dict or y not in F_add_dict[x]:
                    is_hom = False
                    break
                sum_xy = F_add_dict[x][y]
                if sum_xy not in psi_dict:
                    is_hom = False
                    break
                if not check_equal(psi_dict[sum_xy], psi_dict[x] * psi_dict[y]):
                    is_hom = False
                    break
            if not is_hom:
                break
                
        is_non_trivial = any(not check_equal(p, 1) for p in psi_dict.values())
        is_nonzero = all(not check_zero(p) for p in psi_dict.values())
        
        h1 = bool(is_hom and is_non_trivial and is_nonzero)
    except Exception:
        h1 = False

    try:
        # ¬Q: The sum ∑_{x ∈ F} ψ(x) is NOT equal to 0
        values = list(psi_dict.values())
        if not values:
            total = 0
        else:
            total = values[0]
            for v in values[1:]:
                total = total + v
                
        neg_q = not check_zero(total)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: ψ is a non-trivial additive character of F",
    "¬Q: The sum ∑_{x ∈ F} ψ(x) is not equal to 0"
]

N_HYP = 1
NEG_Q_INDEX = 1