import sympy as sp

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def is_zero(val):
    try:
        if type(val).__name__ == 'Quaternion':
            return is_zero(val.a) and is_zero(val.b) and is_zero(val.c) and is_zero(val.d)
        if hasattr(val, 'is_Matrix') and val.is_Matrix:
            return all(is_zero(v) for v in val)
        val = sp.simplify(val)
        if val == 0:
            return True
        if hasattr(val, 'is_zero') and val.is_zero:
            return True
        if isinstance(val, sp.Mod):
            if sp.simplify(val.args[0] % val.args[1]) == 0:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, A = witness
        else:
            F = None
            A = witness

        if isinstance(A, list):
            A = sp.Matrix(A)

        if not hasattr(A, 'is_Matrix') or not A.is_Matrix:
            return [False, False, False]
        if A.shape[0] != A.shape[1]:
            return [False, False, False]

        # H1: F is a field
        h1 = False
        if F is not None:
            if hasattr(F, 'is_Field') and F.is_Field:
                h1 = True
            elif hasattr(F, 'is_field') and F.is_field:
                h1 = True
            elif F in ['QQ', 'RR', 'CC']:
                h1 = True
        else:
            moduli = []
            for val in A:
                if isinstance(val, sp.Mod):
                    moduli.append(val.args[1])
                elif hasattr(val, 'has') and val.has(sp.Mod):
                    for arg in val.atoms(sp.Mod):
                        moduli.append(arg.args[1])
            if moduli:
                from sympy.ntheory import isprime
                h1 = all(isprime(m) for m in moduli)
            else:
                h1 = True

        # H2: A is a nilpotent matrix
        n = A.shape[0]
        try:
            A_n = A**n
            h2 = all(is_zero(val) for val in A_n)
        except Exception:
            h2 = False

        # neg_Q: The trace of A is not zero
        try:
            trace_A = A.trace()
            neg_q = not is_zero(trace_A)
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is a nilpotent matrix",
    "¬Q: The trace of A is not zero"
]

N_HYP = 2
NEG_Q_INDEX = 2