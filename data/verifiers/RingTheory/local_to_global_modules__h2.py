import sympy
from sympy import S, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for standard algebra objects
Z = S.Integers
Q = S.Rationals
R = S.Reals
C = S.Complexes

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: For every maximal ideal m of R, the localized module M_m is the zero module",
    "¬Q: M is not the zero module"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The conjecture drops the hypothesis that M is a unitary R-module.
    """
    def check(obj, attrs, default):
        for attr in attrs:
            if hasattr(obj, attr):
                try:
                    val = getattr(obj, attr)
                    if callable(val):
                        return bool(val())
                    return bool(val)
                except Exception:
                    pass
        return default

    h1, h2, neg_q = False, False, False

    # 1. Handle dictionary-based mock witnesses
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('R_is_commutative_ring_with_identity', 
                      witness.get('is_commutative_ring_with_identity', False)))
            h2 = bool(witness.get('M_m_is_zero', 
                      witness.get('localized_module_is_zero', False)))
            neg_q = not bool(witness.get('M_is_zero', 
                             witness.get('is_zero_module', True)))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. Handle tuple-based witnesses (Ring, Module)
    if isinstance(witness, tuple) and len(witness) == 2:
        try:
            ring, module = witness
            h1 = check(ring, ['is_commutative_ring_with_identity'], False)
            if not h1:
                is_comm = check(ring, ['is_commutative'], False)
                has_id = check(ring, ['has_identity', 'is_unital'], False)
                h1 = is_comm and has_id
                
            h2 = check(module, ['M_m_is_zero', 'localized_module_is_zero'], False)
            neg_q = not check(module, ['is_zero', 'is_zero_module', 'M_is_zero'], True)
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 3. Handle object-based mock witnesses
    try:
        h1 = check(witness, ['R_is_commutative_ring_with_identity', 'is_commutative_ring_with_identity'], False)
        if not h1:
            is_comm = check(witness, ['is_commutative'], False)
            has_id = check(witness, ['has_identity', 'is_unital'], False)
            h1 = is_comm and has_id

        h2 = check(witness, ['M_m_is_zero', 'localized_module_is_zero'], False)
        neg_q = not check(witness, ['M_is_zero', 'is_zero_module', 'is_zero'], True)
    except Exception:
        pass

    return [h1, h2, neg_q]