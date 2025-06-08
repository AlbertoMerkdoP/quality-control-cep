import tkinter as tk
from tkinter import ttk, messagebox
import spc_calculations as spc
from data import datos_univariado, diseño_univariado, datos_linea

eliminated_subgroups_indices = []
phase1_control_limits = {}
SUBGROUP_SIZE_P1 = len(datos_univariado[0]) if datos_univariado else 0
SUBGROUP_SIZE_P2 = len(datos_linea[0]) if datos_linea else 0
TOTAL_SUBGROUPS_P1 = len(datos_univariado)

# Interfaz


def add_subgroup_to_eliminate():
    try:
        subgroup_num = int(entry_subgroup.get())
        if not 1 <= subgroup_num <= TOTAL_SUBGROUPS_P1:
            raise ValueError(
                f"El número debe estar entre 1 y {TOTAL_SUBGROUPS_P1}.")
        index = subgroup_num - 1
        if index not in eliminated_subgroups_indices:
            eliminated_subgroups_indices.append(index)
            eliminated_subgroups_indices.sort()
            update_eliminated_list_display()
        else:
            messagebox.showinfo(
                "Información", "El subgrupo ya ha sido agregado.")
    except Exception as e:
        messagebox.showerror("Error de entrada", str(e))
    finally:
        entry_subgroup.delete(0, tk.END)


def update_eliminated_list_display():
    display_list = [i + 1 for i in eliminated_subgroups_indices]
    eliminated_list_var.set(
        f"Subgrupos a eliminar: {display_list if display_list else 'Ninguno'}")


def generate_depurated_phase1_and_analysis():
    global phase1_control_limits
    try:
        purged_data = [sg for i, sg in enumerate(
            datos_univariado) if i not in eliminated_subgroups_indices]
        if not purged_data:
            raise ValueError(
                "No quedan datos para analizar tras la depuración.")

        phase1_control_limits = spc.get_control_limits(
            purged_data, SUBGROUP_SIZE_P1)
        mu, sigma = spc.estimate_parameters(purged_data, SUBGROUP_SIZE_P1)

        spc.plot_control_charts(
            data_to_plot=purged_data,
            chart_title_suffix="- Fase I (Datos depurados)",
            limits_to_use=phase1_control_limits
        )

        mu_var.set(f"{mu:.4f}")
        sigma_var.set(f"{sigma:.4f}")

        lse, lie = diseño_univariado['lse'], diseño_univariado['lie']
        cp = spc.calculate_cp(lse, lie, mu, sigma)
        cpk, cpk_shift = spc.calculate_cpk(lse, lie, mu, sigma)

        cp_var.set(f"{cp:.3f}")
        cpk_var.set(f"{cpk:.3f}")
        cpk_shift_var.set(cpk_shift)

        if cp < 1:
            label_cp_interpretation.config(
                text="Proceso incapaz de cumplir con espec.", bg="#ff4d4d", fg="white")
        elif cp == 1:
            label_cp_interpretation.config(
                text="Proceso estrictamente capaz de cumplir con espec.", bg="#ffff66", fg="black")
        else:
            label_cp_interpretation.config(
                text="Proceso capaz de cumplir con espec.", bg="#4dff4d", fg="black")

        btn_monitor_phase2.config(state="normal")

    except Exception as e:
        messagebox.showerror("Error en el cálculo", str(e))


def monitor_online_data():
    if not phase1_control_limits:
        messagebox.showerror(
            "Error de flujo", "Primero debe generar el análisis de Fase I.")
        return
    if SUBGROUP_SIZE_P1 != SUBGROUP_SIZE_P2:
        messagebox.showerror(
            "Error de datos", "El tamaño de subgrupo de Fase I y Fase II no coincide.")
        return
    try:
        spc.plot_control_charts(
            data_to_plot=datos_linea,
            chart_title_suffix="- Fase II (Monitoreo en línea)",
            limits_to_use=phase1_control_limits
        )
    except Exception as e:
        messagebox.showerror("Error en monitoreo", str(e))


# Ventana principal
root = tk.Tk()
root.title("Control Estadístico de Procesos (CEP) - Análisis Univariado")
root.geometry("600x600")
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TLabelframe.Label", font=("Helvetica", 14, "bold"))
style.configure("Sub.TLabelframe.Label", font=("Helvetica", 12, "bold"))

main_title = ttk.Label(
    root, text="Control Estadístico de Procesos (CEP)", font=("Helvetica", 20, "bold"))
main_title.pack(pady=15)

# Frame Fase I
phase1_frame = ttk.LabelFrame(
    root, text="Fase I: depuración y análisis", padding=(10, 5))
phase1_frame.pack(padx=20, pady=5, fill="x")
input_frame = ttk.Frame(phase1_frame)
input_frame.pack(fill="x", pady=5)
ttk.Label(input_frame, text="Eliminar subgrupo N°:").pack(
    side="left", padx=(0, 10))
entry_subgroup = ttk.Entry(input_frame, width=5)
entry_subgroup.pack(side="left", padx=(0, 10))
ttk.Button(input_frame, text="Agregar",
           command=add_subgroup_to_eliminate).pack(side="left")
eliminated_list_var = tk.StringVar(value="Subgrupos a eliminar: Ninguno")
ttk.Label(phase1_frame, textvariable=eliminated_list_var,
          font=("Helvetica", 10, "italic")).pack(pady=5)
ttk.Button(phase1_frame, text="Generar cartas depuradas Fase I y análisis",
           command=generate_depurated_phase1_and_analysis).pack(pady=5)

# Resultados
results_frame = ttk.LabelFrame(
    root, text="Resultados del proceso (basado en Fase I depurada)", padding=(10, 5))
results_frame.pack(padx=20, pady=5, fill="x", expand=True)

# Parámetros
params_sub_frame = ttk.LabelFrame(
    results_frame, text="Parámetros", style="Sub.TLabelframe", padding=(10, 5))
params_sub_frame.pack(fill="x", padx=5, pady=5)

mu_var = tk.StringVar(value="N/A")
sigma_var = tk.StringVar(value="N/A")
ttk.Label(params_sub_frame, text="Media muestral (μ):").grid(
    row=0, column=0, sticky="w", padx=5, pady=2)
ttk.Label(params_sub_frame, textvariable=mu_var).grid(
    row=0, column=1, sticky="w", padx=5, pady=2)
ttk.Label(params_sub_frame, text="Desviación estándar (σ):").grid(
    row=1, column=0, sticky="w", padx=5, pady=2)
ttk.Label(params_sub_frame, textvariable=sigma_var).grid(
    row=1, column=1, sticky="w", padx=5, pady=2)

# Indices de Capacidad
capacity_sub_frame = ttk.LabelFrame(
    results_frame, text="Índices de Capacidad (CP)", style="Sub.TLabelframe", padding=(10, 5))
capacity_sub_frame.pack(fill="x", padx=5, pady=5)

cp_var = tk.StringVar(value="N/A")
cpk_var = tk.StringVar(value="N/A")
cpk_shift_var = tk.StringVar(value="N/A")

ttk.Label(capacity_sub_frame, text=f"USL: {diseño_univariado['lse']} | LSL: {diseño_univariado['lie']}").grid(
    row=0, column=0, columnspan=3, sticky="w", padx=5, pady=2)
ttk.Label(capacity_sub_frame, text="CP:").grid(
    row=1, column=0, sticky="w", padx=5, pady=2)
ttk.Label(capacity_sub_frame, textvariable=cp_var).grid(
    row=1, column=1, sticky="w", padx=5, pady=2)
label_cp_interpretation = tk.Label(
    capacity_sub_frame, text="...", font=("Helvetica", 10, "bold"), bg="lightgrey")
label_cp_interpretation.grid(row=1, column=2, sticky="ew", padx=10, pady=2)
ttk.Label(capacity_sub_frame, text="CPk:").grid(
    row=2, column=0, sticky="w", padx=5, pady=2)
ttk.Label(capacity_sub_frame, textvariable=cpk_var).grid(
    row=2, column=1, sticky="w", padx=5, pady=2)
ttk.Label(capacity_sub_frame, textvariable=cpk_shift_var, font=(
    "Helvetica", 10, "italic")).grid(row=2, column=2, sticky="w", padx=10, pady=2)
capacity_sub_frame.columnconfigure(2, weight=1)

phase2_frame = ttk.LabelFrame(
    root, text="Fase II: datos en línea", padding=(10, 5))
phase2_frame.pack(padx=20, pady=10, fill="x")
btn_monitor_phase2 = ttk.Button(
    phase2_frame, text="Monitorear datos en línea (Fase II)", command=monitor_online_data, state="disabled")
btn_monitor_phase2.pack(pady=5)

if __name__ == "__main__":
    initial_limits = spc.get_control_limits(datos_univariado, SUBGROUP_SIZE_P1)
    spc.plot_control_charts(
        datos_univariado, "- Fase I (Datos originales)", initial_limits)
    root.mainloop()
