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

1. Install **luanti** (see here: https://www.luanti.org/downloads/) and dependencies for `miney-socket`. I use Debian and therefore install it like this:

    ```bash
    sudo apt update
    sudo apt install minetest lua-socket lua-cjson -y
    ```

    You should now be possible to start luanti.

    ```bash
    minetest
    ```

2. (Optional) Install `Minetest Game` as the classic game. This is required in newer versions of `luanti`.

    ![Install game](assets/install_game.png)

    ![Minetest game](assets/install_minetest_game.png)

    ![Install Button](assets/install_button.png)

    You now can click twice *Back* and are ready to play `luanti` without `luci`.

3. Close `luanti` and install the `miney-socket` mod, which is needed for the `miney` python interface.

    ```bash
    mkdir -p ~/.minetest/mods
    # via git
    git clone https://github.com/miney-py/mineysocket ~/.minetest/mods/mineysocket
    echo "secure.trusted_mods = mineysocket" >> ~/.minetest/minetest.conf
    ```

4. Install `luci` with pipx.

    ```bash
    sudo apt install pipx -y
    pipx ensurepath
    pipx install git+https://github.com/lookslikematrix/luci.git
    pipx upgrade luci
    ```

5. Create game, enable `mineysocket` mod and start game.

    ![New game](assets/new_game.png)

    ![Select mods](assets/select_mods.png)

    ![Enable mineysocket](assets/enable_mineysocket.png)

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

❤️ A thousand thanks to the developers of the [`miney-socket`](https://github.com/miney-py/mineysocket) and [`miney`](https://github.com/miney-py/miney) Python interface: https://github.com/miney-py

❤️ Everyone is welcome to make a contribution to this project.
