import sympy
from sympy import symbols

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Localization commutes with ideal multiplication for arbitrary subsets".
    
    The dropped hypothesis is that I and J must be ideals of R.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            I = witness.get('I')
            J = witness.get('J')
        else:
            R, S, I, J = witness
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring with identity
    h1 = False
    try:
        if R in [sympy.ZZ, sympy.QQ]:
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative and hasattr(R, 'zero') and hasattr(R, 'one'):
            h1 = True
        elif hasattr(R, 'zero') and hasattr(R, 'one'):
            h1 = True
    except Exception:
        pass

    # H2: S is a multiplicatively closed subset of R
    h2 = False
    try:
        S_iter = iter(S)
        S_list = []
        for _ in range(20):
            try:
                S_list.append(next(S_iter))
            except StopIteration:
                break
        
        if len(S_list) > 0:
            h2 = True
            for a in S_list:
                for b in S_list:
                    if (a * b) not in S:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        pass

    # neg_Q: S^{-1}(IJ) != (S^{-1}I)(S^{-1}J) as ideals in S^{-1}R
    # This fails if S^{-1}(IJ) is not an ideal in S^{-1}R.
    neg_q = False
    try:
        I_iter = iter(I)
        I_list = []
        for _ in range(20):
            try:
                I_list.append(next(I_iter))
            except StopIteration:
                break
                
        J_iter = iter(J)
        J_list = []
        for _ in range(20):
            try:
                J_list.append(next(J_iter))
            except StopIteration:
                break

        # Compute the set of products IJ
        IJ = []
        for i in I_list:
            for j in J_list:
                prod = i * j
                if prod not in IJ:
                    IJ.append(prod)

        zero = getattr(R, 'zero', 0)

        # Equality of fractions in S^{-1}R: x/s == y/u iff exists t in S such that t*(x*u - y*s) == 0
        def eq(x, s, y, u):
            for t in S_list:
                if t * (x * u - y * s) == zero:
                    return True
            return False

        # Elements of S^{-1}(IJ) represented as pairs (numerator, denominator)
        S_inv_IJ = [(x, s) for x in IJ for s in S_list]

        if not S_inv_IJ:
            # Empty set is not an ideal
            neg_q = True
        else:
            s0 = S_list[0]
            zero_frac = (zero, s0)
            
            # Check if the zero element of S^{-1}R is in S^{-1}(IJ)
            has_zero = False
            for frac in S_inv_IJ:
                if eq(frac[0], frac[1], zero_frac[0], zero_frac[1]):
                    has_zero = True
                    break
            
            if not has_zero:
                neg_q = True
            else:
                # Check closure under addition for S^{-1}(IJ)
                max_checks = 1000
                checks = 0
                for f1 in S_inv_IJ:
                    for f2 in S_inv_IJ:
                        checks += 1
                        if checks > max_checks:
                            break
                        
                        # Sum of f1 and f2: x/s + y/u = (x*u + y*s) / (s*u)
                        sum_num = f1[0] * f2[1] + f2[0] * f1[1]
                        sum_den = f1[1] * f2[1]
                        
                        sum_in = False
                        for f3 in S_inv_IJ:
                            if eq(sum_num, sum_den, f3[0], f3[1]):
                                sum_in = True
                                break
                        if not sum_in:
                            neg_q = True
                            break
                    if neg_q or checks > max_checks:
                        break
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}(IJ) != (S^{-1}I)(S^{-1}J) as ideals in S^{-1}R"
]

N_HYP = 2
NEG_Q_INDEX = 2