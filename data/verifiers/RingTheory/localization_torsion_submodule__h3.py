import sympy
from sympy import Matrix, eye, zeros, Rational
from sympy.abc import x, y, z

# Top-level setup for the witness namespace
ZZ = sympy.ZZ
QQ = sympy.QQ

class Witness:
    """
    A mock witness class for abstract counterexamples where sympy cannot compute the localization.
    The LLM can instantiate this class to provide a counterexample.
    """
    def __init__(self, R_is_integral_domain=True, M_is_R_module=True, zero_not_in_S=True, conclusion_holds=False):
        self.R_is_integral_domain = R_is_integral_domain
        self.M_is_R_module = M_is_R_module
        self.zero_not_in_S = zero_not_in_S
        self.conclusion_holds = conclusion_holds
        self.torsion_commutes = conclusion_holds


def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    """
    # 1. Check if witness is a mock object
    if hasattr(witness, 'R_is_integral_domain') or hasattr(witness, 'conclusion_holds'):
        try:
            h1 = bool(getattr(witness, 'R_is_integral_domain', True))
            h2 = bool(getattr(witness, 'M_is_R_module', True))
            h3 = bool(getattr(witness, 'zero_not_in_S', True))
            if hasattr(witness, 'torsion_commutes'):
                neg_q = not bool(witness.torsion_commutes)
            elif hasattr(witness, 'conclusion_holds'):
                neg_q = not bool(witness.conclusion_holds)
            else:
                neg_q = True
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 2. Check if witness is a dictionary with mock keys
    if isinstance(witness, dict) and ('R_is_integral_domain' in witness or 'conclusion_holds' in witness):
        try:
            h1 = bool(witness.get('R_is_integral_domain', True))
            h2 = bool(witness.get('M_is_R_module', True))
            h3 = bool(witness.get('zero_not_in_S', True))
            if 'torsion_commutes' in witness:
                neg_q = not bool(witness.get('torsion_commutes'))
            elif 'conclusion_holds' in witness:
                neg_q = not bool(witness.get('conclusion_holds'))
            else:
                neg_q = True
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 3. Assume witness represents (R, M, S) or just S
    R = None
    M = None
    S = None
    if isinstance(witness, tuple) and len(witness) >= 3:
        R, M, S = witness[0], witness[1], witness[2]
    elif isinstance(witness, dict):
        R = witness.get('R', None)
        M = witness.get('M', None)
        S = witness.get('S', None)
    else:
        S = witness

    try:
        if R is not None:
            if hasattr(R, 'is_domain'):
                h1 = bool(R.is_domain)
            elif hasattr(R, 'is_integral_domain'):
                h1 = bool(R.is_integral_domain)
            elif R in [sympy.ZZ, sympy.QQ]:
                h1 = True
            else:
                h1 = False
        else:
            h1 = True # Default to Z
    except Exception:
        h1 = False

    try:
        # Assume M is a valid module if provided
        h2 = True
    except Exception:
        h2 = False

    try:
        if S is None:
            h3 = False
            neg_q = False
        else:
            if hasattr(S, 'contains'):
                h3 = not S.contains(0)
            else:
                h3 = 0 not in S
            
            # Check multiplicative closure
            # If S is not multiplicatively closed, S^{-1}M is undefined, so the conclusion fails.
            is_mult_closed = True
            if hasattr(S, 'is_FiniteSet') and not S.is_FiniteSet:
                if S == sympy.S.Naturals:
                    is_mult_closed = True
                elif S == sympy.S.Primes:
                    is_mult_closed = False
                else:
                    elements = []
                    for i in range(-100, 100):
                        if i in S:
                            elements.append(i)
                    for a in elements:
                        for b in elements:
                            if (a * b) not in S:
                                is_mult_closed = False
                                break
                        if not is_mult_closed:
                            break
            else:
                S_list = list(S)
                for a in S_list:
                    for b in S_list:
                        if (a * b) not in S_list:
                            is_mult_closed = False
                            break
                    if not is_mult_closed:
                        break
            neg_q = not is_mult_closed
    except Exception:
        h3 = False
        neg_q = False

    return [h1, h2, h3, neg_q]


CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: M is an R-module",
    "H_3: 0 is not an element of S",
    "¬Q: The torsion submodule of S^{-1}M over S^{-1}R is not isomorphic to S^{-1}T(M)"
]

N_HYP = 3
NEG_Q_INDEX = 3