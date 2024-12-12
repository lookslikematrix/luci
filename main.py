import trimesh
import logging
import miney
import numpy as np

logging.basicConfig(level="INFO")

logging.info("📃 Read STL file.")
stl_mesh = trimesh.load_mesh("3DBenchy.stl")

logging.info("🎲 Create a matrix from the STL file.")
voxel_size = 0.7
voxelized = stl_mesh.voxelized(voxel_size)
voxel_matrix = voxelized.matrix

logging.info("🌍️ Object shape: %s, %s, %s (x, y, z)." % (voxel_matrix.shape))
x_dim = voxel_matrix.shape[0]
y_dim = voxel_matrix.shape[1]
z_dim = voxel_matrix.shape[2]
pixels = x_dim * y_dim * z_dim
logging.info("🧪 We have to check %s pixels." % pixels)

# create a 4xN matrix
x_coords, y_coords, z_coords = np.indices((x_dim, y_dim, z_dim))
x_flat = x_coords.flatten()
y_flat = y_coords.flatten()
z_flat = z_coords.flatten()
values_flat = voxel_matrix.flatten()
four_x_n_marix = np.vstack((x_flat, y_flat, z_flat, values_flat))

# create rotation matrix
rotation_matrix = np.matrix([
    [1, 0, 0],
    [0, 0, -1],
    [0, 1, 0]
])

# multiply with rotation matrix
rotated_three_x_n_matrix = np.dot(four_x_n_marix[:3].T, rotation_matrix).T

# print in luanti
# separate air and object
object_values = four_x_n_marix[3, :]
# Find indices where the value is 1
object_indices = np.where(object_values == 1)[0]
air_indices = np.where(object_values == 0)[0]

object_matrix = rotated_three_x_n_matrix[:3, object_indices]
air_matrix = rotated_three_x_n_matrix[:3, air_indices]
logging.info("[ %s ] object pixels.", len(object_indices))
logging.info("[ %s ] air pixels.", len(air_indices))

def print_voxels(mt, matrix, type):
    batch_size = 32000
    batches = list()
    batch_index = 0
    for object_pixel in matrix.T:
        if len(batches) > batch_size:
            batch_index += 1
            logging.info("[ %s ] batch index.", batch_index)
            mt.node.set(batches, name=type)
            batches = list()
        batches.append(
            {
                "x": int(object_pixel[0, 0]),
                "y": int(object_pixel[0, 1]),
                "z": int(object_pixel[0, 2])
            }
        )
    mt.node.set(batches, name=type)

mt = miney.Minetest()
mt.time_of_day = 0.3
mt.player["singleplayer"].fly = True

print_voxels(mt, object_matrix, "default:dirt")
print_voxels(mt, air_matrix, "air")
