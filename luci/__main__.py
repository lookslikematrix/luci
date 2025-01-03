import logging

from pathlib import Path

import click
import trimesh
import miney
import numpy as np

def get_object_matrix(filename: str, scale: float):
    stl_file = Path(filename)
    click.echo("[%s] 📃 Read STL file." % stl_file.absolute())
    stl_mesh = trimesh.load_mesh(stl_file)

    click.echo("🎲 Create a matrix from the STL file.")
    if scale == 0:
        raise ValueError("[%s] scale could not be zero." % scale)
    logging.debug("[%s] scale value." % scale)
    voxel_size = 1 / scale
    voxelized = stl_mesh.voxelized(voxel_size)
    voxel_matrix = voxelized.matrix

    click.echo("🌍️ Object shape: %s, %s, %s (x, y, z)." % (voxel_matrix.shape))
    x_dim = voxel_matrix.shape[0]
    y_dim = voxel_matrix.shape[1]
    z_dim = voxel_matrix.shape[2]
    pixels = x_dim * y_dim * z_dim
    click.echo("🧪 We have to check %s pixels." % pixels)

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

    # separate air and object
    object_values = four_x_n_marix[3, :]
    # Find indices where the value is 1
    object_indices = np.where(object_values == 1)[0]

    object_matrix = rotated_three_x_n_matrix[:3, object_indices]
    click.echo("[ %s ] object pixels." % len(object_indices))
    return object_matrix

def init_luanti_player(mt):
    mt.time_of_day = 0.3
    mt.player["singleplayer"].speed = 50
    mt.player["singleplayer"].fly = True
    mt.player["singleplayer"].position = {
        "x": 0,
        "y": 0,
        "z": 0
    }

def build_voxels(mt, matrix, block_type):
    batch_size = 32000
    batches = list()
    batch_index = 0
    max_batches = matrix.T.shape[0] // batch_size
    click.echo("[ %s ] block type." % block_type )
    for object_pixel in matrix.T:
        if len(batches) > batch_size:
            batch_index += 1
            click.echo("[ %s/%s ] batch index." % (batch_index, max_batches))
            mt.node.set(batches, name=block_type)
            batches = list()
        batches.append(
            {
                "x": int(object_pixel[0, 0]),
                "y": int(object_pixel[0, 1]),
                "z": int(object_pixel[0, 2])
            }
        )
    mt.node.set(batches, name=block_type)

@click.group()
@click.option(
    "--loglevel",
    help="Set loglevel (default: WARNING)"
)
def cli(loglevel):
    """📦️ LuCI - Luanti Commandline Interface 📦️

    Read here for further information:\n
        https://github.com/lookslikematrix/luci

    If you've any issues report them here:\n
        https://github.com/lookslikematrix/luci/issues/new
    """
    if loglevel:
        logging.basicConfig(encoding='utf-8', level=loglevel)
    else:
        logging.disable(logging.CRITICAL)

@cli.command()
@click.argument('filename')
@click.option(
    "-s", "--scale",
    help="Specifies how the object should be scaled.",
    default=1,
    show_default=True
)
@click.option(
    "-b", "--block-type",
    help="Specifies which block-type should be used for building.",
    default="default:goldblock",
    show_default=True
)
def build(filename: str, scale: float, block_type: str):
    """Build a STL file into Luanti.

Example:

    Build a STL file.
        luci build path_to_stl_file.stl
    """
    object_matrix = get_object_matrix(filename, scale)
    mt = miney.Minetest()
    init_luanti_player(mt)
    build_voxels(mt, object_matrix, block_type)


@cli.command()
@click.argument('filename')
@click.option(
    "-s", "--scale",
    help="Specifies how the object should be scaled.",
    default=1,
    show_default=True
)
def erase(filename: str, scale: float):
    """Erase a STL file from Luanti.

Example:

    Erase a STL file.
        luci erase path_to_stl_file.stl
    """
    object_matrix = get_object_matrix(filename, scale)
    mt = miney.Minetest()
    init_luanti_player(mt)
    build_voxels(mt, object_matrix, "air")


@cli.command()
@click.option(
    "-f", "--filter",
    help="Defines a filter to reduce the output.",
    default="default",
    show_default=True
)
def blocks(filter):
    """Get all block types from current Luanti game.

Example:

    Get all default blocks.
        luci blocks

    Get all blocks.
        luci blocks --filter ""

    Get all wools.
        luci blocks --filter "wool"
    """
    mt = miney.Minetest()
    for node_type in mt.node.type:
        if filter in node_type:
            click.echo("[ %s ] node type." % node_type)

if __name__ == '__main__':
    cli()
