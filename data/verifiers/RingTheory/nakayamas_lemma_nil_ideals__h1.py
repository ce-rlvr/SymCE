import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    """
    # 1. Try if witness is a dictionary with boolean flags
    if isinstance(witness, dict) and 'I_is_nil' in witness:
        try:
            h1 = bool(witness.get('I_is_nil', False))
            h2 = bool(witness.get('M_is_fg', False))
            h3 = bool(witness.get('IM_eq_M', False))
            neg_q = not bool(witness.get('M_is_zero', True))
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 2. Try if witness is an object with specific methods
    if hasattr(witness, 'is_nil_ideal'):
        try:
            h1 = bool(witness.is_nil_ideal())
            h2 = bool(witness.is_finitely_generated())
            h3 = bool(witness.IM_equals_M())
            neg_q = not bool(witness.is_zero_module())
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 3. Try if witness is a dictionary defining a finite ring and module
    if isinstance(witness, dict) and 'R' in witness and 'M' in witness:
        try:
            R = witness['R']
            I = witness['I']
            M = witness['M']
            R_add = witness['R_add']
            R_mult = witness['R_mult']
            M_add = witness['M_add']
            action = witness['action']
            
            # H_1: I is a nil ideal of R
            is_ideal = all(i in R for i in I)
            if is_ideal:
                for i in I:
                    for j in I:
                        if R_add(i, j) not in I: 
                            is_ideal = False
                    for r in R:
                        if R_mult(r, i) not in I or R_mult(i, r) not in I: 
                            is_ideal = False
            
            is_nil = True
            for i in I:
                curr = i
                nil = False
                for _ in range(len(R)):
                    # Check if curr is the additive identity
                    is_zero = all(R_add(curr, e) == e for e in R)
                    if is_zero:
                        nil = True
                        break
                    curr = R_mult(curr, i)
                if not nil:
                    is_nil = False
                    break
            h1 = is_ideal and is_nil
            
            # H_2: M is a finitely generated R-module (finite implies finitely generated)
            is_mod = True
            for m1 in M:
                for m2 in M:
                    if M_add(m1, m2) not in M: 
                        is_mod = False
            for r in R:
                for m1 in M:
                    for m2 in M:
                        if action(r, M_add(m1, m2)) != M_add(action(r, m1), action(r, m2)): 
                            is_mod = False
            for r1 in R:
                for r2 in R:
                    for m in M:
                        if action(R_add(r1, r2), m) != M_add(action(r1, m), action(r2, m)): 
                            is_mod = False
                        if action(R_mult(r1, r2), m) != action(r1, action(r2, m)): 
                            is_mod = False
            h2 = is_mod
            
            # H_3: The submodule IM is equal to M
            IM_elements = set()
            for i in I:
                for m in M:
                    IM_elements.add(action(i, m))
            closure = list(IM_elements)
            changed = True
            while changed:
                changed = False
                for a in closure:
                    for b in closure:
                        c = M_add(a, b)
                        if c not in closure:
                            closure.append(c)
                            changed = True
            h3 = (set(closure) == set(M))
            
            # ¬Q: M is not the zero module
            neg_q = len(M) > 1
            
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 4. Try if witness is a callable returning the booleans
    if callable(witness):
        try:
            res = witness()
            if isinstance(res, list) and len(res) == 4:
                return res
        except Exception:
            pass

    # 5. Try if witness is directly a list/tuple of booleans
    if isinstance(witness, (list, tuple)) and len(witness) == 4 and all(isinstance(x, bool) for x in witness):
        return list(witness)

    # Fallback if witness format is unrecognized or evaluation fails
    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: I is a nil ideal of R",
    "H_2: M is a finitely generated R-module",
    "H_3: The submodule IM is equal to M",
    "¬Q: M is not the zero module"
]

N_HYP = 3
NEG_Q_INDEX = 3