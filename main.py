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


latex_str = ""


def show_latex(str):
    plt.text(0, 1, str, fontsize=18)
    plt.axis('off')
    plt.show()


def generate_equation(coefs):
    res = ""
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


n = int(input("Degree: ")) + 1
coefs = input("Coefficients: ").strip().split()
if n != len(coefs):
    print("Not enough or too many coefs")
    exit(1)
coefs = list(map(lambda x: float(x), coefs))
latex_str += f'$${generate_equation(coefs)}$$'

coefs = np.array(coefs, dtype=complex)
x = np.roots(coefs)
x, d = np.unique(x.round(precision), return_counts=True)
m = len(x)
print("Roots number:", m)
print("Unique roots:", x)
print("D:", d)
c_index = 1
latex_str += "$$"
processed = set()
for l in range(0, m):
    if np.conj(x[l]) in processed:
        continue
    processed.add(x[l])
    nu = np.imag(x[l])
    lambda_ = np.real(x[l])

    answer = ""

    q, c_index = get_q(d[l], c_index)
    if is_zero(nu):
        answer += f'{q.strip("()")} + '
    else:
        answer += f'{q}\cos({abs(nu)}t) + '

    requires_quotes = d[l] > 1
    if not is_zero(nu):
        requires_quotes = True
        q, c_index = get_q(d[l], c_index)
        answer += f'{q}\sin({abs(nu)}t)'

    answer = answer.strip(' +')
    if requires_quotes:
        answer = f'({answer})'
    answer += f'e^[{lambda_}t]'
    latex_str += answer.replace('[', '{').replace(']', '}').strip('+ ').replace(' + -', ' - ') + ' + '
latex_str = latex_str.strip(' +') + "$$"

print(latex_str)
show_latex(latex_str)
