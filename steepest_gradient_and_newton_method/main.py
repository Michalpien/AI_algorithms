import numpy as np


def main():
    p = (1, 2)
    p = newton_method(10000, 10**-3, p)
    print(p)
    z = calculate_z(p[0], p[1])
    print(z)


def calculate_gradient_value_in_p(p: tuple[float]) -> tuple[float]:
    x = p[0]
    y = p[1]

    grad = [
        2*x-2-400*x*y+400*x**3,
        200*y-200*x**2
    ]

    return grad


def calculate_hesian_value_in_p(p: tuple[float]) -> tuple[tuple[float]]:
    x = p[0]
    y = p[1]

    hesian = [
        [2-400*y+1200*x**2, -400*x],
        [-400*x, 200]
    ]

    return hesian


def calculate_gradient_multiply_epsilon(gradient, epsilon):
    result = (gradient[0] * epsilon, gradient[1] * epsilon)
    return result


def calculate_sum_vectors(vector1, vector2):
    new_vector = (vector1[0] + vector2[0], vector1[1] + vector2[1])
    return new_vector


def calculate_subtraction_vectors(vector1, vector2):
    new_vector = (vector1[0] - vector2[0], vector1[1] - vector2[1])
    return new_vector


def calculate_z(x: float, y: float) -> float:
    z = (1-x)**2 + 100*(y-x**2)**2
    return z


def get_invert_hesian(hesian:  tuple[tuple[float]]) -> tuple[tuple[float]]:
    inv_hes = np.linalg.inv(hesian)
    return inv_hes


def calculate_hesian_multiply_gradient(hesian: tuple[tuple[float]],
                                       gradient: tuple[float]):
    result = (
        (hesian[0][0]*gradient[0] + hesian[0][1]*gradient[1]),
        (hesian[1][0]*gradient[0] + hesian[1][1]*gradient[1])
    )
    return result


def steepest_gradient_descent(iteration_number: int, epsilon: float):
    p = (5, 5, 0)
    i = 0
    while i < iteration_number:
        grad_p = calculate_gradient_value_in_p(p)
        grad_p_e = calculate_gradient_multiply_epsilon(grad_p, epsilon)
        p = calculate_subtraction_vectors(p, grad_p_e)
        i += 1
    return p


def newton_method(iteration_number: int, epsilon: float, p):
    i = 0
    while i < iteration_number:
        grad_p = calculate_gradient_value_in_p(p)
        hes_p = calculate_hesian_value_in_p(p)
        inv_hes_p = get_invert_hesian(hes_p)
        d = calculate_hesian_multiply_gradient(inv_hes_p, grad_p)
        grad_p_e = calculate_gradient_multiply_epsilon(d, epsilon)
        p = calculate_subtraction_vectors(p, grad_p_e)
        i += 1
    return p


if __name__ == "__main__":
    main()
