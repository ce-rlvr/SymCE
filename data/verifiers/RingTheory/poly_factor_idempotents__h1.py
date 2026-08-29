import sympy as sp
import itertools

# Top-level setup
x = sp.Symbol('x')
y = sp.Symbol('y')
z = sp.Symbol('z')

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 2:
            f_val, k = witness
            if hasattr(f_val, 'domain') and hasattr(f_val, 'gens'):
                f = f_val
                domain = f.domain
                x_gen = f.gens[0]
            else:
                free = f_val.free_symbols if hasattr(f_val, 'free_symbols') else set()
                x_gen = list(free)[0] if free else sp.Symbol('x')
                f = sp.Poly(f_val, x_gen, domain='ZZ')
                domain = f.domain
        elif len(witness) == 3:
            f_val, domain_val, k = witness
            if hasattr(f_val, 'domain') and hasattr(f_val, 'gens'):
                f = f_val
                domain = f.domain
                x_gen = f.gens[0]
            else:
                free = f_val.free_symbols if hasattr(f_val, 'free_symbols') else set()
                x_gen = list(free)[0] if free else sp.Symbol('x')
                f = sp.Poly(f_val, x_gen, domain=domain_val)
                domain = f.domain
        else:
            return [False, False, False]
            
        # H1: f(x) is a non-constant polynomial
        try:
            h1 = f.degree() > 0
        except Exception:
            h1 = False
            
        # H2: f(x) has exactly k distinct monic irreducible factors
        try:
            factors = f.factor_list()
            distinct_factors = factors[1]
            
            monic_irreducible_factors = []
            for fact, mult in distinct_factors:
                if fact.degree() > 0 and fact.LC() == 1:
                    monic_irreducible_factors.append(fact)
                    
            h2 = (len(monic_irreducible_factors) == k) and (len(distinct_factors) == k) and (abs(f.LC()) == 1)
        except Exception:
            h2 = False
            
        # ¬Q: The factor ring does NOT contain exactly 2^k idempotent elements
        try:
            if domain == sp.ZZ:
                f_QQ = f.set_domain(sp.QQ)
                factors_QQ = f_QQ.factor_list()[1]
                k_QQ = len(factors_QQ)
                
                q = [fact**mult for fact, mult in factors_QQ]
                
                idempotents_count = 0
                if k_QQ == 0:
                    idempotents_count = 1
                else:
                    for target in itertools.product([0, 1], repeat=k_QQ):
                        if len(target) == 1:
                            e = sp.Poly(target[0], x_gen, domain='QQ')
                        else:
                            r = sp.sympify(target[0])
                            m = q[0].as_expr()
                            for i in range(1, len(target)):
                                r2 = sp.sympify(target[i])
                                m2 = q[i].as_expr()
                                s, t, g = sp.gcdex(m, m2, x_gen, domain='QQ')
                                r = (r * t * m2 + r2 * s * m)
                                m = (m * m2).expand()
                                r = sp.rem(r, m, x_gen, domain='QQ')
                            e = sp.Poly(r, x_gen, domain='QQ')
                        
                        is_int = True
                        for c in e.coeffs():
                            if not c.is_integer:
                                is_int = False
                                break
                        if is_int:
                            idempotents_count += 1
                            
                neg_q = (idempotents_count != 2**k)
            elif domain.is_Field:
                idempotents_count = 2 ** len(distinct_factors)
                neg_q = (idempotents_count != 2**k)
            else:
                neg_q = False
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f(x) is a non-constant polynomial",
    "H_2: f(x) has exactly k distinct monic irreducible factors",
    "¬Q: The factor ring does NOT contain exactly 2^k idempotent elements"
]

N_HYP = 2
NEG_Q_INDEX = 2