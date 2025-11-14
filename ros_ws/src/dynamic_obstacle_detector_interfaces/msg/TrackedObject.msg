# Rappresenta un singolo oggetto tracciato

uint32 id                     # ID univoco dell'ostacolo

geometry_msgs/Point position  # Posizione stimata (dal filtro di Kalman)
geometry_msgs/Vector3 velocity # Velocità stimata (dal filtro di Kalman)

# Matrice di covarianza dello stato [x, y, vx, vy] 4x4
# Rappresenta l'incertezza della stima.
# Ordine: (x, y, vx, vy)
# Row-major order.
float64[36] covariance
