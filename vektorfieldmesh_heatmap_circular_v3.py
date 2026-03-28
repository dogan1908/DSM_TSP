"""
Zirkulär interpolierte Vektor-Heatmap aus Koordinatenmatrix
===========================================================
Korrigierte Version: Löst das Wrapping-Problem bei 360°→0°

Problem der linearen Interpolation:
  Zwischen 350° und 10° liegt eigentlich 0° (kurzer Weg: 20°)
  Lineare Interpolation: 350→180→10 (langer Weg: 340° = FALSCH)
  → Erzeugt künstliche Regenbogen-Streifen

Lösung:
  1. Winkel in sin(θ) und cos(θ) zerlegen
  2. sin und cos separat interpolieren (linear, kein Wrapping)
  3. Winkel rekonstruieren via atan2(sin, cos)

Autor: Dogan Balban, 2026
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. CSV laden
# ---------------------------------------------------------
df = pd.read_csv("d:/koordinaten3.csv", sep=",", decimal=".", dtype=str)
df = df.set_index(df.columns[0])

def to_float(x):
    if isinstance(x, (float, int)):
        return float(x)
    if isinstance(x, str):
        return float(x.strip().replace(",", "."))
    raise ValueError(f"Unbekannter Typ: {type(x)}")

values = np.zeros(df.shape, dtype=float)
for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        values[i, j] = to_float(df.iloc[i, j])

X = values[0]
Y = values[1]
labels = df.columns.tolist()
n = len(labels)

# ---------------------------------------------------------
# 2. Winkelmatrix berechnen
# ---------------------------------------------------------
W = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        dx = X[j] - X[i]
        dy = Y[j] - Y[i]
        W[i, j] = (np.degrees(np.arctan2(dy, dx)) + 360) % 360

# ---------------------------------------------------------
# 3. ZIRKULÄRE Interpolation (statt linear)
# ---------------------------------------------------------
def circular_interpolate(W_deg, factor=10):
    """
    Interpoliert eine Winkelmatrix KORREKT über die 360°-Grenze.
    
    Methode:
      θ → (sin θ, cos θ) → interpoliere beide → atan2 → θ_neu
    
    Das garantiert: zwischen 350° und 10° kommt 0° raus,
    nicht 180° wie bei linearer Interpolation.
    """
    h, w = W_deg.shape
    R = np.radians(W_deg)
    S = np.sin(R)
    C = np.cos(R)
    
    new_h = h * factor
    new_w = w * factor
    
    # Interpolationsgitter
    y_new = np.linspace(0, h - 1, new_h)
    x_new = np.linspace(0, w - 1, new_w)
    xx_new, yy_new = np.meshgrid(x_new, y_new)
    
    y0 = np.floor(yy_new).astype(int)
    x0 = np.floor(xx_new).astype(int)
    y1 = np.clip(y0 + 1, 0, h - 1)
    x1 = np.clip(x0 + 1, 0, w - 1)
    
    dy = yy_new - y0
    dx = xx_new - x0
    
    def bilinear(M):
        return (M[y0, x0] * (1 - dy) * (1 - dx) +
                M[y1, x0] * dy * (1 - dx) +
                M[y0, x1] * (1 - dy) * dx +
                M[y1, x1] * dy * dx)
    
    S_interp = bilinear(S)
    C_interp = bilinear(C)
    
    # Rekonstruiere Winkel
    W_result = (np.degrees(np.arctan2(S_interp, C_interp)) + 360) % 360
    return W_result

W_interp = circular_interpolate(W, factor=10)

# ---------------------------------------------------------
# 4. Vektoren berechnen
# ---------------------------------------------------------
R = np.radians(W_interp)
U = np.cos(R)
V = np.sin(R)

# ---------------------------------------------------------
# 5. Plot
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(5, 4.5), dpi=80)
fig.subplots_adjust(top=0.88, bottom=0.12, left=0.12, right=0.9)

im = ax.imshow(W_interp, cmap="hsv", origin="lower", vmin=0, vmax=360)

h, w = W_interp.shape
xx, yy = np.meshgrid(np.arange(w), np.arange(h))

# Weniger Pfeile (jeder 3.) für Lesbarkeit
step = 3
ax.quiver(xx[::step, ::step], yy[::step, ::step],
          U[::step, ::step], V[::step, ::step],
          color="black", alpha=0.35, scale=80, width=0.002)

# Stadt-Labels auf den Achsen
ticks = [i * 10 + 5 for i in range(n)]
ax.set_xticks(ticks)
ax.set_xticklabels(labels, fontsize=9)
ax.set_yticks(ticks)
ax.set_yticklabels(labels, fontsize=9)

ax.set_title("Zirkulär interpolierte Vektor-Heatmap\n(korrekte 360°-Interpolation)")
plt.colorbar(im, label="Winkel (Grad)", shrink=0.85)
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# OPTIONAL: Vergleich linear vs zirkulär
# ---------------------------------------------------------
if False:  # Auf True setzen um Vergleich zu sehen
    # Lineare Version (mit Artefakten)
    def linear_interpolate(M, factor=10):
        h, w = M.shape
        new_h, new_w = h * factor, w * factor
        y_new = np.linspace(0, h-1, new_h)
        x_new = np.linspace(0, w-1, new_w)
        xx_n, yy_n = np.meshgrid(x_new, y_new)
        y0 = np.floor(yy_n).astype(int)
        x0 = np.floor(xx_n).astype(int)
        y1 = np.clip(y0+1, 0, h-1)
        x1 = np.clip(x0+1, 0, w-1)
        dy = yy_n - y0; dx = xx_n - x0
        return (M[y0,x0]*(1-dy)*(1-dx) + M[y1,x0]*dy*(1-dx) +
                M[y0,x1]*(1-dy)*dx + M[y1,x1]*dy*dx)
    
    W_lin = linear_interpolate(W, 10)
    
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
    fig.subplots_adjust(top=0.85, bottom=0.14, left=0.06, right=0.94, wspace=0.3)
    a1.imshow(W_lin, cmap='hsv', origin='lower', vmin=0, vmax=360)
    a1.set_title('Linear (mit Artefakten)')
    a2.imshow(W_interp, cmap='hsv', origin='lower', vmin=0, vmax=360)
    a2.set_title('Zirkulär (korrigiert)')
    plt.tight_layout()
    plt.show()
