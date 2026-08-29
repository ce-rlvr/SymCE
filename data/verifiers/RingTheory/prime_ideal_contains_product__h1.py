import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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
    Given a witness object, evaluates the hypotheses and the negated conclusion.
    The witness can be a tuple, dict, or object representing the ring R and ideals P, I, J.
    """
    try:
        # Unpack witness
        R = P = I = J = IJ = None
        if isinstance(witness, tuple):
            if len(witness) == 4:
                R, P, I, J = witness
            elif len(witness) == 3:
                P, I, J = witness
            elif len(witness) == 5:
                R, P, I, J, IJ = witness
            else:
                return [False] * 5
        elif isinstance(witness, dict):
            R = witness.get('R')
            P = witness.get('P')
            I = witness.get('I')
            J = witness.get('J')
            IJ = witness.get('IJ')
        else:
            R = getattr(witness, 'R', None)
            P = getattr(witness, 'P', None)
            I = getattr(witness, 'I', None)
            J = getattr(witness, 'J', None)
            IJ = getattr(witness, 'IJ', None)

        if P is None or I is None or J is None:
            return [False] * 5

        # Helper to evaluate predicates safely
        def check_pred(obj, names, *args):
            if obj is None: return None
            for name in names:
                if hasattr(obj, name):
                    attr = getattr(obj, name)
                    if callable(attr):
                        try:
                            return attr(*args)
                        except TypeError:
                            try:
                                return attr()
                            except Exception:
                                pass
                    else:
                        return attr
            return None

        # H1: P is a prime ideal
        h1_ok = check_pred(P, ['is_prime_ideal', 'is_prime'], R)
        if h1_ok is None and R is not None:
            h1_ok = check_pred(R, ['is_prime_ideal'], P)
        if h1_ok is None:
            if isinstance(P, int):
                h1_ok = sympy.isprime(P) or P == 0
            else:
                h1_ok = False

        # H2: I is an ideal
        h2_ok = check_pred(I, ['is_ideal'], R)
        if h2_ok is None and R is not None:
            h2_ok = check_pred(R, ['is_ideal'], I)
        if h2_ok is None:
            h2_ok = True  # Assume true if not explicitly checkable but passed as ideal

        # H3: J is an ideal
        h3_ok = check_pred(J, ['is_ideal'], R)
        if h3_ok is None and R is not None:
            h3_ok = check_pred(R, ['is_ideal'], J)
        if h3_ok is None:
            h3_ok = True

        # H4: IJ \subseteq P
        if IJ is None:
            if hasattr(I, '__mul__'):
                try:
                    IJ = I * J
                except Exception:
                    pass
            if IJ is None and R is not None:
                IJ = check_pred(R, ['multiply_ideals', 'mul_ideals'], I, J)
        
        h4_ok = False
        if IJ is not None:
            h4_ok = check_pred(IJ, ['issubset', 'subset'], P)
            if h4_ok is None:
                h4_ok = check_pred(P, ['issuperset', 'superset'], IJ)
            if h4_ok is None and R is not None:
                h4_ok = check_pred(R, ['is_subset', 'subset'], IJ, P)
            if h4_ok is None:
                if isinstance(IJ, int) and isinstance(P, int):
                    h4_ok = (IJ % P == 0) if P != 0 else (IJ == 0)
                elif isinstance(IJ, set) and isinstance(P, set):
                    h4_ok = IJ.issubset(P)
        
        # neg_Q: Neither I nor J is a subset of P
        q_I = check_pred(I, ['issubset', 'subset'], P)
        if q_I is None and R is not None:
            q_I = check_pred(R, ['is_subset', 'subset'], I, P)
        if q_I is None:
            if isinstance(I, int) and isinstance(P, int):
                q_I = (I % P == 0) if P != 0 else (I == 0)
            elif isinstance(I, set) and isinstance(P, set):
                q_I = I.issubset(P)

        q_J = check_pred(J, ['issubset', 'subset'], P)
        if q_J is None and R is not None:
            q_J = check_pred(R, ['is_subset', 'subset'], J, P)
        if q_J is None:
            if isinstance(J, int) and isinstance(P, int):
                q_J = (J % P == 0) if P != 0 else (J == 0)
            elif isinstance(J, set) and isinstance(P, set):
                q_J = J.issubset(P)

        q = bool(q_I) or bool(q_J)
        neg_q_ok = not q

        return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(h4_ok), bool(neg_q_ok)]

    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "H_4: The product ideal IJ is a subset of P",
    "¬Q: Neither I nor J is a subset of P"
]

N_HYP = 4
NEG_Q_INDEX = 4