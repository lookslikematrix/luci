# 📦️ LuCI - Luanti Commandline Interface

This Commandline Interface allows you to build CAD-Objects in [**luanti**](https://www.luanti.org/). For example the benchy from here: https://www.thingiverse.com/thing:763622. The game used to be called minetest, but now it's called luanti, so this description is a mixture of minetest and luanti.

![Benchy](assets/benchy.png)

It's depending on [`miney`](https://miney.readthedocs.io/en/latest/) a python interface for luanti. 

## Usage

Getting help.

```bash
luci --help
```

Build a CAD-Object in the STL format with `luci`.

```bash
luci build --help
luci build data/some_stl_file.stl
# get all wool blocks
luci blocks --filter wool
# build object with green wool
luci build data/some_stl_file.stl --block-type wool:green
# scale by factor 2
luci build data/some_stl_file.stl --scale 2
# build object at exact position. Default is at the players position.
luci build data/some_stl_file.stl -x 100 -y 150 -z 50
```

Erase this CAD-Object.

```bash
luci erase --help
luci erase data/some_stl_file.stl
# erase scale by factor 2
luci erase data/some_stl_file.stl --scale 2
```


## Installation

If you like to use `luci` you have to follow this steps.

1. Install **luanti** (see here: https://www.luanti.org/downloads/) and the `miney` mod. I use Debian and therefore install it like this:

    ```bash
    sudo apt update
    sudo apt install luanti -y
    ```

    You should now be possible to start luanti.

    ```bash
    luanti
    ```

2. Install `luci` with pipx.

    ```bash
    sudo apt install pipx -y
    pipx ensurepath
    pipx install git+https://github.com/lookslikematrix/luci.git
    pipx upgrade luci
    ```

3. (Optional) Install `Minetest Game` as the classic game. This is required in newer versions of `luanti`.

    ![Install game](assets/install_game.png)

    ![Minetest game](assets/install_minetest_game.png)

    ![Install Button](assets/install_button.png)

    You now can click twice *Back* and are ready to play `luanti` without `luci`.

5. Create game, install `miney` mod, enable `miney` mod, enable server and start game.

    ![New game](assets/new_game.png)

    ![Create game](assets/create_game.png)

    ![Select mods](assets/select_mods.png)

    ![Find and install miney](assets/find_and_install_miney.png)

    ![Select miney and save](assets/select_miney.png)

    ![Enable host and start](assets/enable_host.png)

5. Build a STL-Object.

    ```bash
    luci build data/some_stl_file.stl
    # and erase it
    luci erase data/some_stl_file.stl
    ```

## Development

```bash
git clone https://github.com/lookslikematrix/luci
cd luci
sudo apt install pipx
pipx install poetry
poetry install
poetry shell
```

---

❤️ A thousand thanks to the developers of [`miney`](https://github.com/miney-py/miney) Python interface: https://github.com/miney-py

❤️ Everyone is welcome to make a contribution to this project.
