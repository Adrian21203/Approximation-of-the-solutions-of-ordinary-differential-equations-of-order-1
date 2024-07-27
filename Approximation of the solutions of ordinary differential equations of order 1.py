import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sympy as sp
import pandas as pd
import csv
import random
import scipy.optimize as opt
import re
from tkinter import messagebox, filedialog, ttk, simpledialog,font
from matplotlib.figure import Figure

#Metode de calcul:
#Metoda Euler explicita

def euler_explicit(f, y0, t):
    y = np.zeros(len(t))
    y[0] = y0

    for i in range(len(t) - 1):
        dt = t[i + 1] - t[i]
        y[i + 1] = y[i] + dt * f(y[i], t[i])

    return y

#Metoda Euler implicita

def euler_implicit(f, y0, t):
    y = np.zeros(len(t))
    y[0] = y0

    def implicit_eq(ynext, t, y, dt): # functia ce reprez ecuatia implicita care trb rezolvata pt gasirea lui y la pasul urm
        return ynext - y - dt * f(ynext,t + dt)

    for i in range(len(t) - 1):
        dt = t[i + 1] - t[i]
        y_next = opt.fsolve(implicit_eq, y[i], args=(t[i], y[i], dt))[0]
        y[i + 1] = y_next

    return y

#Metoda Runge-Kutta de ordin 2
def runge_kutta_2(f, y0, t):

    y = np.zeros(len(t))
    y[0] = y0

    for i in range(len(t) - 1):
        dt = t[i + 1] - t[i]
        k1 = f(y[i], t[i])
        k2 = f(y[i] + k1 * dt / 2, t[i] + dt / 2)
        y[i + 1] = y[i] + k2 * dt

    return y

#Metoda Runge-Kutta de ordin 4
def runge_kutta_4(f, y0, t):

    y = np.zeros(len(t))
    y[0] = y0

    for i in range(len(t) - 1):
        dt = t[i + 1] - t[i]
        k1 = f(y[i], t[i])
        k2 = f(y[i] + k1 * dt / 2, t[i] + dt / 2)
        k3 = f(y[i] + k2 * dt / 2, t[i] + dt / 2)
        k4 = f(y[i] + k3 * dt, t[i] + dt)
        y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6

    return y

#variabila globala in care stocam f,y0 si t si metoda selectata
date_stocate = {}
metoda_selectata= None  

#citire date din fisier txt
def citeste_fisier():
    cale_fisier = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    if not cale_fisier:
        messagebox.showerror("Eroare", "Nu a fost selectat niciun fișier TXT")
        return None, None, None
    
    try:
        with open(cale_fisier, 'r') as file:
            lines = file.readlines()

        if len(lines) != 3:
            raise ValueError("Fișierul trebuie să conțină exact 3 linii")

        f_line = lines[0].strip().split(':')
        if len(f_line) != 2 or not re.match(r"^[+\-]?\d+\*t([+\-*/]\d+)?$", f_line[1].strip()):
            raise ValueError("Funcția nu este specificată corect. Trebuie sa fie de format +-a*t sau +-a*t+-*/b")
        f_value = f_line[1].strip()

        # Citirea și validarea liniei y0
        y0_line = lines[1].strip().split(':')
        if len(y0_line) != 2 or not y0_line[1].strip().isdigit():
            raise ValueError("y0 trebuie să fie un număr valid pozitiv")
        y0_value = int(y0_line[1].strip())

        # Citirea și validarea liniei t
        t_line = lines[2].strip().split(':')
        if len(t_line) != 2:
            raise ValueError("Valoarea pentru t trebuie să fie specificată corect")
        
        t_values = t_line[1].strip().split(',')
        if len(t_values) != 2 or not all(v.strip().isdigit() for v in t_values):
            raise ValueError("Valoarea pentru t trebuie să fie în formatul 't_end,nr_pasi'")
        t_end = int(t_values[0].strip())
        nr_pasi = int(t_values[1].strip())

        date_stocate['f'] = f_value
        date_stocate['y0'] = y0_value
        date_stocate['t'] = prelucrare_t(t_end,nr_pasi)
        messagebox.showinfo("Date stocate", "Datele din fisier au fost stocate cu succes.")
        dy_dt_entry.delete(0, tk.END)
        dy_dt_entry.insert(tk.END, f_value)
        y0_entry.delete(0, tk.END)
        y0_entry.insert(tk.END, str(y0_value))
        t_entry.delete(0, tk.END)
        t_entry.insert(tk.END, f"{t_end},{nr_pasi}")
    
    except Exception as e:
        messagebox.showerror("Eroare", str(e))
        
    
#generare date de intrare random
def input_date_random():
    f_str = generate_random_equation()
    y0 = random.randint(1, 100)
    t_end = random.randint(1, 100)
    nr_pasi = random.randint(1, 100)
    date_stocate['f'] = f_str
    date_stocate['y0'] = y0
    date_stocate['t'] = prelucrare_t(t_end,nr_pasi)
    messagebox.showinfo("Date stocate", "Datele aleatorii au fost memorate pentru utilizare .")
    dy_dt_entry.delete(0, tk.END)
    dy_dt_entry.insert(tk.END, f_str)    
    y0_entry.delete(0, tk.END)
    y0_entry.insert(tk.END, str(y0))    
    t_entry.delete(0, tk.END)
    t_entry.insert(tk.END, f"{t_end},{nr_pasi}")

def generate_random_equation():
    a = random.randint(1, 100)   
    b = random.randint(1, 100)   
    operator = random.choice(['+', '-'])  
    equation = f"{a}*t{operator}{b}"  
    return equation

# Functie pentru salvarea datelor introduse de la tastatura
def salvare_date():
    try:
        f_str = dy_dt_entry.get().strip()
        y0_str = y0_entry.get().strip()
        t_str = t_entry.get().strip()

        # Validarea funcției f(dy/dt)
        if not re.match(r"^[+\-]?\d+\*t([+\-*/]\d+)?$", f_str):
            raise ValueError("Funcția nu este specificată corect. Trebuie sa fie de format +-a*t sau +-a*t+-*/b")

        # Validarea valorii y0
        if not y0_str.isdigit():
            raise ValueError("y0 trebuie să fie un număr valid pozitiv")
        y0_value = int(y0_str)

        # Validarea și prelucrarea valorii t(t_end, nr_pasi)
        t_values = t_str.split(',')
        if len(t_values) != 2 or not all(v.strip().isdigit() for v in t_values):
            raise ValueError("Valoarea pentru t trebuie să fie în formatul 't_end,nr_pasi'")
        t_end = int(t_values[0].strip())
        nr_pasi = int(t_values[1].strip())

        date_stocate['f'] = f_str
        date_stocate['y0'] = y0_value
        date_stocate['t'] = prelucrare_t(t_end, nr_pasi)

        messagebox.showinfo("Date stocate", "Datele au fost salvate cu succes.")
    except Exception as e:
        messagebox.showerror("Eroare", str(e))

def reset_data(): #resetam datele de intrare, metoda selectata si plotul
    global date_stocate, metoda_selectata, ani, ax, canvas
    date_stocate = {}
    metoda_selectata.set(None)
    ani = None  

    dy_dt_entry.delete(0, tk.END)
    y0_entry.delete(0, tk.END)
    t_entry.delete(0, tk.END)
    
    eroare_absoluta_entry.config(state=tk.NORMAL)
    eroare_absoluta_entry.delete(0, tk.END)
    eroare_absoluta_entry.config(state="readonly")
    
    eroare_relativa_entry.config(state=tk.NORMAL)
    eroare_relativa_entry.delete(0, tk.END)
    eroare_relativa_entry.config(state="readonly")
    for child in methods_frame.winfo_children():
        child.deselect()

    ax.clear()
    ax.set_title("Grafic")
    ax.set_xlabel("t")
    ax.set_ylabel("y")
    canvas.draw()

    messagebox.showinfo("Date resetate", "Datele și graficul au fost resetate cu succes")


def calculeaza_er_abs(y1, y2):
    return np.abs(y1 - y2)

def calculeaza_er_rel(y1, y2):
    abs_error = calculeaza_er_abs(y1, y2)
    abs_y1 = np.abs(y1)
    rel_error = np.zeros_like(abs_y1)

    nonzero_indices = abs_y1 != 0
    rel_error[nonzero_indices] = abs_error[nonzero_indices] / abs_y1[nonzero_indices] # folosim astfel pentru evitarea impartirii la 0

    return rel_error

def prelucrare_t(t,nr_pasi):
    t_final = np.linspace(0, t, nr_pasi)
    return t_final

def creeaza_functie(f_str):
    def f(y, t):
        return eval(f_str)
    return f

def generare_tabel():
    global date_stocate, metoda_selectata

    if not date_stocate:
        messagebox.showerror("Eroare", "Datele nu au fost încă introduse sau citite din fișier.")
        return

    if not metoda_selectata:
        messagebox.showerror("Eroare", "Nu a fost selectată nicio metodă.")
        return

    method_name = metoda_selectata.get()

    df = pd.DataFrame(columns=['Nr_pas', 't', 'y_odeint',  f'y_{method_name}', 'Eroare_absoluta', 'Eroare_relativa'])

    f_str = date_stocate['f']
    y0 = date_stocate['y0']
    t = date_stocate['t']

    f = creeaza_functie(f_str)

    y_odeint = odeint(f, y0, t).flatten()

    if method_name == "euler_explicit":
        method_func = euler_explicit
    elif method_name == "euler_implicit":
        method_func = euler_implicit
    elif method_name == "rk2":
        method_func = runge_kutta_2
    elif method_name == "rk4":
        method_func = runge_kutta_4
    else:
        messagebox.showerror("Eroare", "Metoda selectată nu este recunoscută.")
        return

    y_method = method_func(f, y0, t)

    # Calcularea erorilor absolută și relativă
    err_abs = calculeaza_er_abs(y_odeint, y_method)
    err_rel = calculeaza_er_rel(y_odeint, y_method)

    # Adăugarea datelor în DataFrame
    df['Nr_pas'] = np.arange(1, len(t) + 1)
    df['t'] = t
    df['y_odeint'] = y_odeint
    df[f'y_{method_name}'] = y_method
    df['Eroare_absoluta'] = err_abs
    df['Eroare_relativa'] = err_rel

    tabel_window = tk.Toplevel()
    tabel_window.title("Tabel")
    tabel_window.geometry("800x800")

    # Crearea unui Treeview
    tree = ttk.Treeview(tabel_window)
    tree["columns"] = ['Nr_pas', 't', 'y_odeint', f'y_{method_name}', 'Eroare_absoluta', 'Eroare_relativa']
    tree["show"] = "headings"

    # Setarea titlurilor pentru coloane
    for col in tree["columns"]:
        tree.heading(col, text=col)

    # Adăugarea datelor în Treeview
    for index, row in df.iterrows():
        tree.insert("", "end", values=row.tolist())

    # Scrollbar pentru Treeview
    vsb = ttk.Scrollbar(tabel_window, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    # Afisarea Treeview
    tree.pack(expand=True, fill='both')

ani = None
fig = None
ax = None
def start_animatie():
    global ani

    if not date_stocate:
        messagebox.showerror("Eroare", "Datele nu au fost încă introduse sau citite din fișier.")
        return

    if not metoda_selectata.get():
        messagebox.showerror("Eroare", "Nu a fost selectată nicio metodă.")
        return

    method_name = metoda_selectata.get()

    if method_name == "euler_explicit":
        method_func = euler_explicit
    elif method_name == "euler_implicit":
        method_func = euler_implicit
    elif method_name == "rk2":
        method_func = runge_kutta_2
    elif method_name == "rk4":
        method_func = runge_kutta_4
    else:
        messagebox.showerror("Eroare", "Metoda selectată nu este recunoscută.")
        return

    f_str = date_stocate['f']
    y0 = date_stocate['y0']
    t = date_stocate['t']

    f = creeaza_functie(f_str)
    y_method = method_func(f, y0, t)
    y_odeint = odeint(lambda y, t: f(y, t), y0, t).flatten()

    ax.clear()
    ax.set_title(f"Soluția aproximată folosind {method_name}")
    ax.set_xlabel("t")
    ax.set_ylabel("y")
    ax.set_xlim(0, max(t))
    ax.set_ylim(min(y_method) - 0.1 * abs(min(y_method)), max(y_method) + 0.1 * abs(max(y_method)))

    line, = ax.plot([], [], label=method_name)
    ax.legend()

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        if frame == 0:
            line.set_data([], [])
            return line,

        line.set_data(t[:frame], y_method[:frame])
        abs_error = np.abs(y_odeint[frame-1] - y_method[frame-1])
        rel_error = abs_error / np.abs(y_odeint[frame-1]) if y_odeint[frame-1] != 0 else 0
        eroare_absoluta_entry.config(state='normal')
        eroare_absoluta_entry.delete(0, tk.END)
        eroare_absoluta_entry.insert(0, f"{abs_error:.20f}")
        eroare_absoluta_entry.config(state='readonly')
        eroare_relativa_entry.config(state='normal')
        eroare_relativa_entry.delete(0, tk.END)
        eroare_relativa_entry.insert(0, f"{rel_error:.20f}")
        eroare_relativa_entry.config(state='readonly')
        return line,

    ani = animation.FuncAnimation(fig, update, frames=len(t)+1, init_func=init, blit=True, repeat=False, interval=500)
    canvas.draw()

def stop_animatie():
    global ani
    if ani:
        ani.event_source.stop()

def reia_animatie():
        ani.event_source.start()

def salveaza_animatie():
    global ani

    if not ani:
        messagebox.showerror("Eroare", "Nu a fost începută nicio animație.")
        return

    cale_fisier = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])

    if not cale_fisier:
        return

    ani.save(cale_fisier, writer="imagemagick", fps=10) 

    messagebox.showinfo("Salvare", f"Animația a fost salvată cu succes în '{cale_fisier}'.")



root = tk.Tk()
root.title("Aproximarea solutiilor ecualtiilor liniare de ordin I")
root.geometry("1300x650")
root.configure(bg="#f0f0f0")

bold_font = font.Font(family="Helvetica", size=12, weight="bold")

graph_frame = tk.Frame(root, bg="white", padx=10, pady=10)
graph_frame.grid(row=0, column=0, rowspan=14, padx=10, pady=10)

fig = Figure(figsize=(6, 6), dpi=100)
ax = fig.add_subplot(111)
ax.set_title("Grafic")
ax.set_xlabel("t")
ax.set_ylabel("y")

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

input_frame = tk.LabelFrame(root, text="Introduceți Datele", font=bold_font, padx=10, pady=10, bg="#f0f0f0")
input_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

tk.Label(input_frame, text="f(dy/dt):", font=bold_font, bg="#f0f0f0").grid(row=0, column=0, sticky="e", pady=5)
dy_dt_entry = tk.Entry(input_frame)
dy_dt_entry.grid(row=0, column=1, pady=5)

tk.Label(input_frame, text="y0:", font=bold_font, bg="#f0f0f0").grid(row=1, column=0, sticky="e", pady=5)
y0_entry = tk.Entry(input_frame)
y0_entry.grid(row=1, column=1, pady=5)

tk.Label(input_frame, text="t(t_end,nr_pasi):", font=bold_font, bg="#f0f0f0").grid(row=2, column=0, sticky="e", pady=5)
t_entry = tk.Entry(input_frame)
t_entry.grid(row=2, column=1, pady=5)

tk.Button(input_frame, text="Memorează Datele", command=salvare_date, font=bold_font).grid(row=4, column=0, columnspan=2, pady=10)

data_frame = tk.LabelFrame(root, text="Gestionare Date", font=bold_font, padx=10, pady=6, bg="#f0f0f0")
data_frame.grid(row=1, column=1, padx=10, pady=6, sticky="ew")

tk.Button(data_frame, text="Generază Funcție Random", command=input_date_random, font=bold_font).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
tk.Button(data_frame, text="Citește Funcție din Fișier", command=citeste_fisier, font=bold_font).grid(row=1, column=0, padx=5, pady=5, sticky="ew")

methods_frame = tk.LabelFrame(root, text="Alege Metoda", font=bold_font, padx=10, pady=10, bg="#f0f0f0")
methods_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

metoda_selectata= tk.StringVar()
metoda_selectata.set(None)

tk.Radiobutton(methods_frame, text="Metoda Euler implicită", variable=metoda_selectata, value="euler_implicit", font=bold_font, bg="#f0f0f0").grid(row=0, column=0, sticky="w")
tk.Radiobutton(methods_frame, text="Metoda Euler explicită", variable=metoda_selectata, value="euler_explicit", font=bold_font, bg="#f0f0f0").grid(row=1, column=0, sticky="w")
tk.Radiobutton(methods_frame, text="Metoda Runge-Kutta ordin 2", variable=metoda_selectata, value="rk2", font=bold_font, bg="#f0f0f0").grid(row=2, column=0, sticky="w")
tk.Radiobutton(methods_frame, text="Metoda Runge-Kutta ordin 4", variable=metoda_selectata, value="rk4", font=bold_font, bg="#f0f0f0").grid(row=3, column=0, sticky="w")

action_frame = tk.LabelFrame(root, text="Acțiuni", font=bold_font, padx=10, pady=10, bg="#f0f0f0")
action_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nw")

tk.Button(action_frame, text="Start Animatie", command=start_animatie, font=bold_font, width=25).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
tk.Button(action_frame, text="Stop Animatie", command=stop_animatie, font=bold_font, width=25).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
tk.Button(action_frame, text="Reia Animatie", command=reia_animatie, font=bold_font, width=25).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
tk.Button(action_frame, text="Afișează Tabel", command=generare_tabel, font=bold_font, width=25).grid(row=3, column=0, padx=5, pady=5, sticky="ew")
tk.Button(action_frame, text="Salvează Animație", command=salveaza_animatie, font=bold_font, width=25).grid(row=4, column=0, padx=5, pady=5, sticky="ew")

error_frame = tk.LabelFrame(root, text="Erori", font=bold_font, padx=10, pady=10, bg="#f0f0f0")
error_frame.grid(row=2, column=1, padx=10, pady=0, sticky="nw")

tk.Label(error_frame, text="Eroare absolută:", font=bold_font, bg="#f0f0f0").grid(row=0, column=0, sticky="e", pady=5)
eroare_absoluta_entry = tk.Entry(error_frame,state="readonly",readonlybackground="white")
eroare_absoluta_entry.grid(row=0, column=1, pady=5)

tk.Label(error_frame, text="Eroare relativă:", font=bold_font, bg="#f0f0f0").grid(row=1, column=0, sticky="e", pady=5)
eroare_relativa_entry = tk.Entry(error_frame,state="readonly",readonlybackground="white")
eroare_relativa_entry.grid(row=1, column=1, pady=5)

btn_reset = tk.Button(root, text="Reset", command=reset_data, font=bold_font)
btn_reset.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

root.mainloop()


