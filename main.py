import trimesh
import logging
import miney

print("📃 Read STL file.")
stl_mesh = trimesh.load_mesh("3DBenchy.stl")

print("🎲 Create a matrix from the STL file.")
voxel_size = 0.3
voxelized = stl_mesh.voxelized(voxel_size)
voxel_matrix = voxelized.matrix

print("🌍️ World shape: %s, %s, %s (x, y, z)." % (voxel_matrix.shape))
pixels = voxel_matrix.shape[0] * voxel_matrix.shape[1] * voxel_matrix.shape[2]
print("🧪 We have to check %s pixels." % pixels)

batch_size = 32000
print("🔪 We creating batches of %s pixels." % batch_size)

print("🏃 Iterate over matrix.")
batches = list()
air_batches = list()
batch = list()
air_batch = list()
start_position = {'z': 0, 'x': -256, 'y': 9}

print("🚜 Calculate base plate.")
for x_offset in range(voxel_matrix.shape[0]):
    logging.debug("Edit x: %s/%s" % (x_offset, voxel_matrix.shape[0]))
    for z_offset in range(voxel_matrix.shape[2]):
        logging.debug("Edit z: %s/%s" % (z_offset, voxel_matrix.shape[2]))
        voxel = {
            "x": start_position["x"] + x_offset,
            "y": start_position["y"] + -1,
            "z": start_position["z"] + z_offset
        }
        if len(batch) >= batch_size:
            batches.append(batch)
            batch = list()
        batch.append(voxel)
batches.append(batch)

for y_offset in range(voxel_matrix.shape[1]):
    logging.debug("Edit y: %s/%s" % (y_offset, voxel_matrix.shape[1]))
    for x_offset in range(voxel_matrix.shape[0]):
        logging.debug("Edit x: %s/%s" % (x_offset, voxel_matrix.shape[0]))
        for z_offset in range(voxel_matrix.shape[2]):
            logging.debug("Edit z: %s/%s" % (z_offset, voxel_matrix.shape[2]))
            voxel = {
                "x": start_position["x"] + x_offset,
                "y": start_position["y"] + y_offset,
                "z": start_position["z"] + z_offset
            }
            if len(air_batch) >= batch_size:
                air_batches.append(air_batch)
                air_batch = list()
            air_batch.append(voxel)
            if voxel_matrix[x_offset][y_offset][z_offset]:
                if len(batch) >= batch_size:
                    batches.append(batch)
                    batch = list()
                batch.append(voxel)
air_batches.append(air_batch)
batches.append(batch)

print("💨 We have to clear the air in %s batches." % len(air_batches))
print("📦️ We have to print %s batches." % len(batches))
mt = miney.Minetest()
mt.time_of_day = 0.3
mt.player["singleplayer"].fly = True
for increment in range(len(air_batches)):
    print("☁️ Place air: %s/%s" % (increment + 1, len(air_batches)))
    mt.node.set(air_batches[increment], name="air")
for increment in range(len(batches)):
    print("📦️ Print batch: %s/%s" % (increment + 1, len(batches)))
    mt.node.set(batches[increment], name="default:dirt")
mt.player["singleplayer"].position = {'z': 0 + voxel_matrix.shape[2], 'x': -256 + voxel_matrix.shape[0], 'y': 9.5 + voxel_matrix.shape[1]}
