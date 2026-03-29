import cv2
import numpy as np
import time

print("Program started...")

start_time = time.time()

# Load image
image = cv2.imread("road.jpeg")

if image is None:
    print("❌ Error: Image not found")
    exit()

# Resize
image = cv2.resize(image, (1280, 720))

# ---------------- BEV TRANSFORMATION ----------------
src = np.float32([
    [200, 720],
    [1080, 720],
    [750, 450],
    [530, 450]
])

dst = np.float32([
    [300, 720],
    [1000, 720],
    [1000, 0],
    [300, 0]
])

matrix = cv2.getPerspectiveTransform(src, dst)
bev = cv2.warpPerspective(image, matrix, (1280, 720))

# Add title
cv2.putText(bev, "Bird's Eye View", (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# ---------------- OCCUPANCY MAP ----------------
gray = cv2.cvtColor(bev, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

_, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
binary = cv2.bitwise_not(binary)

kernel = np.ones((7, 7), np.uint8)
binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
binary = cv2.medianBlur(binary, 5)

cv2.putText(binary, "Occupancy Map", (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# ---------------- GRID CONVERSION ----------------
grid_size = 20
h, w = binary.shape

h_new = (h // grid_size) * grid_size
w_new = (w // grid_size) * grid_size

binary = binary[:h_new, :w_new]

grid = binary.reshape(h_new//grid_size, grid_size,
                      w_new//grid_size, grid_size)

grid = grid.mean(axis=(1, 3))
grid = (grid > 127).astype(int)

print("Grid shape:", grid.shape)
print("Sample grid:\n", grid[:5, :5])

# ---------------- GRID VISUALIZATION ----------------
# Black-white grid
grid_img = (grid * 255).astype(np.uint8)
grid_img = cv2.resize(grid_img, (640, 360), interpolation=cv2.INTER_NEAREST)

# Colored grid (RED = occupied, GREEN = free)
color_grid = np.zeros((grid.shape[0], grid.shape[1], 3), dtype=np.uint8)

for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        if grid[i][j] == 1:
            color_grid[i][j] = [0, 0, 255]  # red
        else:
            color_grid[i][j] = [0, 255, 0]  # green

color_grid = cv2.resize(color_grid, (640, 360), interpolation=cv2.INTER_NEAREST)

# ---------------- DRAW GRID ON BEV ----------------
bev_with_grid = bev.copy()

for i in range(0, h_new, grid_size):
    cv2.line(bev_with_grid, (0, i), (w_new, i), (0, 255, 0), 1)

for j in range(0, w_new, grid_size):
    cv2.line(bev_with_grid, (j, 0), (j, h_new), (0, 255, 0), 1)

# ---------------- LEGEND ----------------
legend = np.zeros((120, 300, 3), dtype=np.uint8)

cv2.putText(legend, "Green = Free", (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

cv2.putText(legend, "Red = Occupied", (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# ---------------- SAVE OUTPUT ----------------
cv2.imwrite("bev_output.jpg", bev)
cv2.imwrite("occupancy_map.jpg", binary)
cv2.imwrite("grid_map.jpg", grid_img)
cv2.imwrite("final_bev_grid.jpg", bev_with_grid)

print("✅ Outputs saved!")

# ---------------- PERFORMANCE ----------------
end_time = time.time()
print("Processing time:", round(end_time - start_time, 3), "seconds")

# ---------------- SHOW ----------------
cv2.imshow("Original", image)
cv2.imshow("BEV", bev)
cv2.imshow("Occupancy Map", binary)
cv2.imshow("BEV with Grid", bev_with_grid)
cv2.imshow("Grid Map (BW)", grid_img)
cv2.imshow("Colored Grid Map", color_grid)
cv2.imshow("Legend", legend)

cv2.waitKey(0)
cv2.destroyAllWindows()