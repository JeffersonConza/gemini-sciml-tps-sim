import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# SCIML: PHYSICS-INFORMED NEURAL NETWORK (PINN) PARA ESCUDOS TÉRMICOS
# =============================================================================
# Este script utiliza PyTorch para entrenar una red neuronal que APRENDE a 
# resolver la Ecuación del Calor 1D, guiada por las leyes de la física
# sin necesidad de una malla discreta (mesh-free approach).

# Fijar semilla para reproducibilidad
torch.manual_seed(42)

# --- PARÁMETROS FÍSICOS ---
alpha = 0.005 # Difusividad térmica ablativa
L = 1.0       # Grosor del escudo (m)
t_max = 10.0  # Ventana de tiempo a aprender (s)

# --- ARQUITECTURA DE LA RED NEURONAL ---
class PINN(nn.Module):
    def __init__(self):
        super().__init__()
        # Red: 2 entradas (x, t) -> 4 capas ocultas de 32 -> 1 salida (T_norm)
        self.net = nn.Sequential(
            nn.Linear(2, 32), nn.Tanh(),
            nn.Linear(32, 32), nn.Tanh(),
            nn.Linear(32, 32), nn.Tanh(),
            nn.Linear(32, 32), nn.Tanh(),
            nn.Linear(32, 1)
        )

    def forward(self, x, t):
        return self.net(torch.cat([x, t], dim=1))

model = PINN()
optimizer = torch.optim.Adam(model.parameters(), lr=2e-3)

# --- GENERACIÓN DE DATOS (COLLOCATION POINTS) ---
# Usamos normalización térmica para estabilizar el entrenamiento de la IA
# T_norm = (T - 25) / 1475 => T(1500) = 1.0, T(25) = 0.0

# 1. Puntos internos (Collocation Points) para evaluar la EDP
N_pde = 2000
x_pde = torch.rand(N_pde, 1, requires_grad=True) * L
t_pde = torch.rand(N_pde, 1, requires_grad=True) * t_max

# 2. Frontera Exterior (Plasma): x=0, T_norm=1.0 (1500°C)
N_bc = 500
x_bc1 = torch.zeros(N_bc, 1)
t_bc1 = torch.rand(N_bc, 1) * t_max
T_bc1 = torch.ones(N_bc, 1) * 1.0

# 3. Frontera Interior (Cabina): x=L, T_norm=0.0 (25°C)
x_bc2 = torch.ones(N_bc, 1) * L
t_bc2 = torch.rand(N_bc, 1) * t_max
T_bc2 = torch.zeros(N_bc, 1)

# 4. Condición Inicial: t=0, T_norm=0.0 (25°C en todo el escudo)
N_ic = 500
x_ic = torch.rand(N_ic, 1) * L
t_ic = torch.zeros(N_ic, 1)
T_ic = torch.zeros(N_ic, 1)

# --- BUCLE DE ENTRENAMIENTO (OPTIMIZACIÓN SciML) ---
epochs = 3000
print("🚀 Entrenando Physics-Informed Neural Network (PINN)...")
print("La IA está aprendiendo termodinámica sin simulación discreta.")

for epoch in range(epochs):
    optimizer.zero_grad()
    
    # Pérdida 1: Cumplimiento de la Física (Residual de la Ecuación del Calor)
    T_pred = model(x_pde, t_pde)
    
    # Diferenciación Automática (Autograd) de PyTorch
    dT_dt = torch.autograd.grad(T_pred, t_pde, grad_outputs=torch.ones_like(T_pred), create_graph=True)[0]
    dT_dx = torch.autograd.grad(T_pred, x_pde, grad_outputs=torch.ones_like(T_pred), create_graph=True)[0]
    d2T_dx2 = torch.autograd.grad(dT_dx, x_pde, grad_outputs=torch.ones_like(dT_dx), create_graph=True)[0]
    
    f_pde = dT_dt - alpha * d2T_dx2 # Residual de la Ecuación del Calor
    loss_pde = torch.mean(f_pde**2)
    
    # Pérdida 2: Cumplimiento de Condiciones de Frontera e Iniciales
    loss_bc1 = torch.mean((model(x_bc1, t_bc1) - T_bc1)**2)
    loss_bc2 = torch.mean((model(x_bc2, t_bc2) - T_bc2)**2)
    loss_ic = torch.mean((model(x_ic, t_ic) - T_ic)**2)
    
    # Loss Function compuesta (Física + Datos de Frontera)
    loss = loss_pde + loss_bc1 + loss_bc2 + loss_ic
    
    loss.backward()
    optimizer.step()
    
    if epoch % 500 == 0:
        print(f"Epoch {epoch:4d} | Loss Total: {loss.item():.5f} | Física (PDE): {loss_pde.item():.5f}")

print("✅ Entrenamiento completado.")

# --- VALIDACIÓN VISUAL DEL MODELO PREDICTIVO ---
print("Generando inferencia con la red neuronal entrenada...")

x_test = torch.linspace(0, L, 100).view(-1, 1)
# Predecir perfil térmico a t = 5 segundos
t_test = torch.ones_like(x_test) * 5.0 

with torch.no_grad():
    T_pred_norm = model(x_test, t_test)
    T_pred_real = T_pred_norm * 1475.0 + 25.0

plt.style.use('dark_background')
plt.figure(figsize=(8, 5))
plt.plot(x_test.numpy(), T_pred_real.numpy(), color='#00ffcc', lw=3, label='Inferencia IA (t=5s)')
plt.title('Inferencia Térmica de PINN (Mesh-free)', fontweight='bold', color='white')
plt.xlabel('Profundidad (m)')
plt.ylabel('Temperatura (°C)')
plt.grid(True, alpha=0.3, linestyle='--')
plt.legend()
plt.tight_layout()
plt.savefig('prediccion_pinn.png', dpi=150)
print("Gráfico predictivo de la IA guardado como 'prediccion_pinn.png'.")
