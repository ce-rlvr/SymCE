import sympy
import itertools
import functools
import operator

# Top-level setup
x, y, z, t = sympy.symbols('x y z t')
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    h1 = False
    neg_q = False

    try:
        R = None
        I = None
        rad_I_provided = None

        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                R, I = witness
            elif len(witness) == 3:
                R, I, rad_I_provided = witness
            else:
                R = ZZ
                I = witness
        else:
            R = ZZ
            I = witness

        # Check H1: R is a commutative Noetherian ring
        if hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        elif R == ZZ or R == QQ:
            h1 = True
        else:
            h1 = False

        # Check neg_Q: For all k > 0, (\sqrt{I})^k \not\subseteq I
        if rad_I_provided is not None:
            if not rad_I_provided:
                neg_q = False
            else:
                neg_q = True
                for k in range(1, 21):
                    all_in_I = True
                    for p in itertools.combinations(rad_I_provided, min(k, len(rad_I_provided))):
                        g = sympy.Mul(*p)
                        if k > len(rad_I_provided):
                            g *= rad_I_provided[0]**(k - len(rad_I_provided))
                        _, rem = sympy.polys.polytools.reduced(g, I)
                        if rem != 0:
                            all_in_I = False
                            break
                    if all_in_I:
                        neg_q = False
                        break

        elif isinstance(I, (list, tuple)) and all(isinstance(gen, sympy.Expr) for gen in I):
            is_monomial_powers = True
            rad_I = []
            for gen in I:
                if gen.is_Pow and gen.base.is_Symbol and gen.exp.is_Integer and gen.exp > 0:
                    rad_I.append(gen.base)
                elif gen.is_Symbol:
                    rad_I.append(gen)
                else:
                    is_monomial_powers = False
                    break
            
            if is_monomial_powers:
                if not rad_I:
                    neg_q = False
                else:
                    neg_q = True
                    for k in range(1, 21):
                        all_in_I = True
                        for p in itertools.combinations(rad_I, min(k, len(rad_I))):
                            g = sympy.Mul(*p)
                            if k > len(rad_I):
                                g *= rad_I[0]**(k - len(rad_I))
                            _, rem = sympy.polys.polytools.reduced(g, I)
                            if rem != 0:
                                all_in_I = False
                                break
                        if all_in_I:
                            neg_q = False
                            break
            else:
                neg_q = False

        elif isinstance(I, (set, list, tuple)) and all(isinstance(val, (int, sympy.Integer)) for val in I):
            I_set = set(int(val) for val in I)
            rad_I = set()
            for val in range(-100, 101):
                for m in range(1, 20):
                    if val**m in I_set:
                        rad_I.add(val)
                        break
            
            neg_q = True
            for k in range(1, 21):
                all_in_I = True
                if not rad_I:
                    all_in_I = True
                else:
                    for p in itertools.product(rad_I, repeat=k):
                        if int(sympy.Mul(*p)) not in I_set:
                            all_in_I = False
                            break
                if all_in_I:
                    neg_q = False
                    break

        elif isinstance(I, (int, sympy.Integer)):
            I_val = int(I)
            if I_val == 0:
                neg_q = False
            else:
                rad_I = sympy.ntheory.factor_.rad(abs(I_val))
                neg_q = True
                for k in range(1, 21):
                    if (rad_I**k) % I_val == 0:
                        neg_q = False
                        break
        else:
            if hasattr(witness, 'conclusion'):
                neg_q = not witness.conclusion()
            elif hasattr(witness, 'neg_q'):
                neg_q = bool(witness.neg_q())
            else:
                neg_q = False

    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: For all positive integers k, (\\sqrt{I})^k \\not\\subseteq I"
]

N_HYP = 1
NEG_Q_INDEX = 1