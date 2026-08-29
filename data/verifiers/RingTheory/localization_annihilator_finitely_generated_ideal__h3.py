import sympy as sp

class NonNoetherianRing:
    """
    A representation of the non-Noetherian ring R = k[x, y_1, y_2, ...] / (x y_1, x^2 y_2, ...).
    Elements are represented as sympy polynomials.
    """
    def __init__(self):
        self.x = sp.Symbol('x')
        
    def reduce(self, expr):
        if isinstance(expr, int):
            expr = sp.Integer(expr)
        expr = sp.expand(expr)
        if expr == 0:
            return sp.Integer(0)
        
        terms = sp.Add.make_args(expr)
        new_terms = []
        for term in terms:
            c, factors = term.as_coeff_mul()
            x_deg = 0
            y_indices = []
            for factor in factors:
                if factor == self.x:
                    x_deg += 1
                elif isinstance(factor, sp.Pow) and factor.base == self.x:
                    x_deg += factor.exp
                elif factor.is_Symbol and factor.name.startswith('y'):
                    y_indices.append(int(factor.name[1:]))
                elif isinstance(factor, sp.Pow) and factor.base.is_Symbol and factor.base.name.startswith('y'):
                    y_indices.append(int(factor.base.name[1:]))
                    
            # In the ideal (x y_1, x^2 y_2, ...), a term is 0 if its x-degree >= i for any y_i it contains
            if not any(x_deg >= i for i in y_indices):
                new_terms.append(term)
                
        res = sp.Add(*new_terms)
        if res == 0:
            return sp.Integer(0)
        return res

    def S_element(self, k):
        return self.x**k

    def I_generator(self, i):
        return sp.Symbol(f'y{i}')

# Bindings for the witness expression to use
CounterexampleRing = NonNoetherianRing

def conditions(witness):
    try:
        # H1: R is a commutative ring
        x = witness.S_element(1)
        y1 = witness.I_generator(1)
        y2 = witness.I_generator(2)
        a = x + y1
        b = x * y2
        c = y1 + y2
        
        # Check distributivity and commutativity on sample elements
        h1_1 = witness.reduce((a + b) * c) == witness.reduce(a * c + b * c)
        h1_2 = witness.reduce(a * b) == witness.reduce(b * a)
        h1 = bool(h1_1 and h1_2)
    except Exception:
        h1 = False

    try:
        # H2: S is a multiplicatively closed subset of R
        s0 = witness.S_element(0)
        s2 = witness.S_element(2)
        s3 = witness.S_element(3)
        s5 = witness.S_element(5)
        
        # Check that 1 is in S and S is closed under multiplication
        h2_1 = witness.reduce(s0) == 1
        h2_2 = witness.reduce(s2 * s3) == witness.reduce(s5)
        h2 = bool(h2_1 and h2_2)
    except Exception:
        h2 = False

    try:
        # neg_Q: S^{-1}(Ann(I)) != Ann_{S^{-1}R}(S^{-1}I)
        
        # 1. Check that S^{-1} I == 0 in S^{-1}R
        # This means for each generator y_i of I, there is some s_k in S such that s_k * y_i == 0 in R.
        S_inv_I_is_zero = True
        for i in range(1, 11):
            yi = witness.I_generator(i)
            annihilated = False
            for k in range(1, 16):
                sk = witness.S_element(k)
                if witness.reduce(sk * yi) == 0:
                    annihilated = True
                    break
            if not annihilated:
                S_inv_I_is_zero = False
                break
                
        # 2. Check that 1 is NOT in S^{-1} Ann(I)
        # This means no element of S is in Ann(I).
        # So for any s_k in S, there is some y_i in I such that s_k * y_i != 0 in R.
        no_S_in_Ann_I = True
        for k in range(1, 11):
            sk = witness.S_element(k)
            kills_all = True
            for i in range(1, 16):
                yi = witness.I_generator(i)
                if witness.reduce(sk * yi) != 0:
                    kills_all = False
                    break
            if kills_all:
                no_S_in_Ann_I = False
                break
                
        # 3. Check that 0 is not in S (so S^{-1}R is not the zero ring)
        zero_in_S = False
        for k in range(1, 11):
            if witness.reduce(witness.S_element(k)) == 0:
                zero_in_S = True
                break
                
        # If S^{-1} I == 0, then Ann_{S^{-1}R}(S^{-1}I) = S^{-1}R, which contains 1.
        # If 1 is not in S^{-1} Ann(I), then the two ideals cannot be equal.
        neg_q = bool(S_inv_I_is_zero and no_S_in_Ann_I and not zero_in_S)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}(Ann(I)) != Ann_{S^{-1}R}(S^{-1}I)"
]

N_HYP = 2
NEG_Q_INDEX = 2