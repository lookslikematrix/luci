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

def build_voxels(lt, position, matrix, block_type):
    x = round(position["x"])
    y = round(position["y"])
    z = round (position["z"])
    batch_size = 8000
    batches = list()
    batch_index = 0
    max_batches = matrix.T.shape[0] // batch_size + 1
    click.echo("[ %s ] block type." % block_type )
    for object_pixel in matrix.T:
        if len(batches) > batch_size:
            batch_index += 1
            click.echo("[ %s/%s ] batch index." % (batch_index, max_batches))
            lt.nodes.set(batches)
            batches = list()
        node = miney.Node(
            int(object_pixel[0, 0] + x),
            int(object_pixel[0, 1] + y),
            int(object_pixel[0, 2] + z),
            name=block_type
        )
        batches.append(node)
    batch_index += 1
    click.echo("[ %s/%s ] batch index." % (batch_index, max_batches))
    lt.nodes.set(batches)

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
@click.option(
    "-x",
    type=int,
    help="Specifies x-axes to start building."
)
@click.option(
    "-y",
    type=int,
    help="Specifies y-axes to start building."
)
@click.option(
    "-z",
    type=int,
    help="Specifies z-axes to start building."
)
def build(filename: str, scale: float, block_type: str, x: int, y:int, z: int):
    """Build a STL file into Luanti.

Example:

    Build a STL file.
        luci build path_to_stl_file.stl
    """
    object_matrix = get_object_matrix(filename, scale)
    with miney.Luanti() as lt:
        position = lt.players["luci"].position
        if x is not None:
            position["x"] = x
        if y is not None:
            position["y"] = y
        if z is not None:
            position["z"] = z
        build_voxels(lt, position, object_matrix, block_type)


@cli.command()
@click.argument('filename')
@click.option(
    "-s", "--scale",
    help="Specifies how the object should be scaled.",
    default=1,
    show_default=True
)
@click.option(
    "-x",
    type=int,
    help="Specifies x-axes to start building."
)
@click.option(
    "-y",
    type=int,
    help="Specifies y-axes to start building."
)
@click.option(
    "-z",
    type=int,
    help="Specifies z-axes to start building."
)
def erase(filename: str, scale: float, x: int, y:int, z: int):
    """Erase a STL file from Luanti.

Example:

    Erase a STL file.
        luci erase path_to_stl_file.stl
    """
    object_matrix = get_object_matrix(filename, scale)
    with miney.Luanti() as lt:
        position = lt.players["luci"].position
        if x is not None:
            position["x"] = x
        if y is not None:
            position["y"] = y
        if z is not None:
            position["z"] = z
        build_voxels(lt, position, object_matrix, "air")


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
    with miney.Luanti() as lt:
        for node_type in lt.nodes.names:
            if filter in node_type:
                click.echo("[ %s ] node type." % node_type)


@cli.command()
def info():
    """Get info.

Example:

    Get infos.
        luci info
    """
    with miney.Luanti() as lt:
        position = lt.players["luci"].position
        click.echo(f"x | {position["x"]}")
        click.echo(f"y | {position["y"]}")
        click.echo(f"z | {position["z"]}")

if __name__ == '__main__':
    cli()
