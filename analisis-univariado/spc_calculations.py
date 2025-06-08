import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy.stats import norm

# Constantes
A2_FACTORS = {2: 1.880, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483, 7: 0.419, 8: 0.373, 9: 0.337, 10: 0.308, 11: 0.285, 12: 0.266, 13: 0.249,
              14: 0.235, 15: 0.223, 16: 0.212, 17: 0.203, 18: 0.194, 19: 0.187, 20: 0.180, 21: 0.173, 22: 0.167}
D3_FACTORS = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.076, 8: 0.136, 9: 0.184, 10: 0.223, 11: 0.256, 12: 0.283, 13: 0.307, 14: 0.328,
              15: 0.347, 16: 0.363, 17: 0.378, 18: 0.391, 19: 0.403, 20: 0.415, 21: 0.425, 22: 0.434}
D4_FACTORS = {2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004, 7: 1.924, 8: 1.864, 9: 1.816, 10: 1.777, 11: 1.744, 12: 1.717, 13: 1.693,
              14: 1.672, 15: 1.653, 16: 1.637, 17: 1.622, 18: 1.608, 19: 1.597, 20: 1.585, 21: 1.575, 22: 1.566}
d2_FACTORS = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 7: 2.704, 8: 2.847, 9: 2.970, 10: 3.078, 11: 3.173, 12: 3.258, 13: 3.336,
              14: 3.407, 15: 3.472, 16: 3.532, 17: 3.588, 18: 3.640, 19: 3.689, 20: 3.735, 21: 3.778, 22: 3.819}


def get_control_limits(data_for_limits, subgroup_size):
    if subgroup_size < 2 or subgroup_size > 22:
        raise ValueError("El tamaño del subgrupo debe estar entre 2 y 22.")
    data_matrix = np.array(data_for_limits)
    if data_matrix.shape[0] == 0:
        raise ValueError("No hay datos para calcular los límites.")
    calc_x_bars, calc_ranges = np.mean(
        data_matrix, axis=1), np.ptp(data_matrix, axis=1)
    x_double_bar, r_bar = np.mean(calc_x_bars), np.mean(calc_ranges)
    A2, D3, D4 = A2_FACTORS[subgroup_size], D3_FACTORS[subgroup_size], D4_FACTORS[subgroup_size]
    return {
        "UCL_xbar": x_double_bar + A2 * r_bar, "LCL_xbar": x_double_bar - A2 * r_bar, "CL_xbar": x_double_bar,
        "UCL_r": D4 * r_bar, "LCL_r": D3 * r_bar, "CL_r": r_bar
    }


def plot_control_charts(data_to_plot, chart_title_suffix, limits_to_use):
    """Genera las cartas de control para un conjunto de datos dado, usando límites pre-calculados."""
    data_matrix = np.array(data_to_plot)
    x_bars, ranges = np.mean(data_matrix, axis=1), np.ptp(data_matrix, axis=1)
    subgroup_numbers = np.arange(1, len(x_bars) + 1)

    fig, (ax_xbar, ax_r) = plt.subplots(2, 1, figsize=(8, 8.5))
    fig.suptitle(
        f'Cartas de control de Shewhart {chart_title_suffix}', fontsize=16)

    def plot_single_chart(ax, values, limits, title, ylabel):
        ucl, lcl, cl = limits['UCL'], limits['LCL'], limits['CL']

        ax.plot(subgroup_numbers, values, linestyle='-', marker='o',
                color='b', label=f'{ylabel} del subgrupo')

        ax.axhline(ucl, color='r', linestyle='--', label=f'LCS = {ucl:.3f}')
        ax.axhline(cl, color='g', linestyle='-', label=f'LC = {cl:.3f}')
        ax.axhline(lcl, color='r', linestyle='--', label=f'LCI = {lcl:.3f}')

        out_of_control_mask = (values > ucl) | ((values < lcl) & (lcl > 0))
        if np.any(out_of_control_mask):
            ax.plot(subgroup_numbers[out_of_control_mask], values[out_of_control_mask],
                    'ro', markersize=8, label='Fuera de control')

        ax.set_title(title)
        ax.set_xlabel('Número de subgrupo')
        ax.set_ylabel(ylabel)
        ax.grid(True)
        if len(subgroup_numbers) < 25:
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.legend(loc='best')

    plot_single_chart(ax_xbar, x_bars, {'UCL': limits_to_use['UCL_xbar'], 'LCL': limits_to_use['LCL_xbar'],
                      'CL': limits_to_use['CL_xbar']}, 'Gráfico de control X̄ (promedio)', 'Promedio')
    plot_single_chart(ax_r, ranges, {'UCL': limits_to_use['UCL_r'], 'LCL': limits_to_use['LCL_r'],
                      'CL': limits_to_use['CL_r']}, 'Gráfico de control R (rango)', 'Rango')

    fig.tight_layout(pad=3.0)
    plt.show(block=False)


def estimate_parameters(purged_data, subgroup_size):
    if subgroup_size not in d2_FACTORS:
        raise ValueError(f"No hay factor d2 para tamaño {subgroup_size}.")
    d2 = d2_FACTORS[subgroup_size]
    purged_matrix = np.array(purged_data)
    mu, sigma = np.mean(purged_matrix), np.ptp(
        purged_matrix, axis=1).mean() / d2
    return mu, sigma


def calculate_cp(lse, lie, media, desv_est):
    if desv_est <= 0:
        raise ValueError("La desviación estándar debe ser > 0.")
    cp = (lse-lie)/(6*desv_est)
    return cp if cp >= 0 else 0.0


def calculate_cpk(lse, lie, media, desv_est):
    if desv_est <= 0:
        raise ValueError("La desviación estándar debe ser > 0.")
    cpu = (lse - media) / (3 * desv_est)
    cpl = (media - lie) / (3 * desv_est)
    cpk = np.min([cpu, cpl])
    shift = "Centrado" if np.isclose(
        cpu, cpl, atol=0.01) else "Desplazado hacia el límite superior (USL)" if cpk == cpu else "Desplazado hacia el límite inferior (LSL)"
    return cpk, shift
