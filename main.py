import math

import numpy as np
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)

precision = 4


def get_q(degree, constant_index):
    res = ""
    for i in reversed(range(1, degree)):
        res += f'C_{constant_index}t^{i} + '
        constant_index = constant_index + 1
    res += f'C_{constant_index}'
    constant_index = constant_index + 1
    if degree > 1:
        res = f'({res})'
    return res.replace('^1', ''), constant_index


def is_zero(a):
    return abs(a) < 10 ** (-precision)


def generate_equation(coefs):
    res = "Equation: "
    for i in range(0, len(coefs)):
        if is_zero(coefs[i]):
            continue
        if i > 0:
            if coefs[i] > 0:
                res += ' + '
            else:
                res += ' - '

        if not is_zero(coefs[i] - 1.):
            res += f'{abs(coefs[i])}'
        res += f'D^{len(coefs) - i - 1}x'
    return res.strip('+ ') + ' = 0'


def get_solution(x, d):
    result = ""
    constant_index = 1
    processed = set()
    for l in range(0, len(d)):
        if np.conj(x[l]) in processed:
            continue
        processed.add(x[l])
        nu = np.imag(x[l])
        lambda_ = np.real(x[l])

        term = ""

        q, constant_index = get_q(d[l], constant_index)
        if is_zero(nu):
            term += f'{q.strip("()")} + '
        else:
            term += f'{q}\cos({abs(nu)}t) + '

        requires_quotes = d[l] > 1
        if not is_zero(nu):
            requires_quotes = True
            q, constant_index = get_q(d[l], constant_index)
            term += f'{q}\sin({abs(nu)}t)'

        term = term.strip(' +')
        if requires_quotes:
            term = f'({term})'
        term += f'e^[{lambda_}t]'
        result += term.replace('[', '{').replace(']', '}').strip('+ ').replace(' + -', ' - ') + ' + '
    return result.strip(' +')


def generate_characteristic_equation(coefs):
    res = r"Characteristic Equation: "
    for i in range(0, len(coefs)):
        if is_zero(coefs[i]):
            continue
        if i > 0:
            if coefs[i] > 0:
                res += ' + '
            else:
                res += ' - '

        if not is_zero(coefs[i] - 1.):
            res += f'{abs(coefs[i])}'
        if len(coefs) - i - 1 > 0:
            res += r'\nu'
        if len(coefs) - i - 1 > 1:
            res += f'^{len(coefs) - i - 1}'
    return res.strip('+ ') + ' = 0'


def show_latex(str):
    plt.figure(figsize=(10, 3))
    plt.text(0, 1, str, fontsize=18)
    plt.axis('off')
    plt.show()


n = int(input("Degree: ")) + 1
if n == 0:
    print("Degree must be > 0")
    exit(1)
coefs = input("Coefficients: ").strip().split()
if is_zero(float(coefs[0])):
    print("First coef cant be 0")
    exit(1)
if n != len(coefs):
    print("Not enough or too many coefs")
    exit(1)

coefs = list(map(lambda x: float(x) / float(coefs[0]), coefs))
latex_str = f'$${generate_equation(coefs)}$$'
latex_str += f'$${generate_characteristic_equation(coefs)}$$'
coefs = np.array(coefs, dtype=complex)

x = np.roots(coefs)
x, d = np.unique(x.round(precision), return_counts=True)
print("Unique roots:", x)
print("D:", d)
latex_str += f'$$x(t) = {get_solution(x, d)}$$'
print(latex_str)
show_latex(latex_str)
