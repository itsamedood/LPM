<div align="center">
	<img src="https://github.com/itsamedood/LPM/assets/74739472/d22cffc8-58e9-43bc-958c-bf84dcbd3e21" width="500"><hr>
</div><br>

## What is LPM?
> LPM is a **l**ocal **p**assword **m**anager that can be used from the command line or with a GUI.

## How does it work?
> Your data is written to a certain file after being encrypted with Fernet. When you need this data, it's decrypted and printed for you! There are other commands such as `edit` and `rm`, but for a full list, run `lpm` or `lpm --help`.

## How do I download it?
<!-- > ### Easy Install (recommended):
> - Install package from the releases page.
> - Run the LPM executable for the GUI version, and if you want to use it from the command line, run the `.sh` file. -->
>
> ### From source (advanced):
> - Install PyInstaller 5.13.0.
> - Clone the repository and `cd` into it.
> - Run `pyinstaller --onefile --distpath bin --name lpm src/main.py` (or use the `tasks.json` method if you're using VSCode).
> - Add the path to the executable to your PATH variable.
> - Run `lpm` and enjoy :)
