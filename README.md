<div align="center">
	<img src="https://github.com/itsamedood/LPM/assets/74739472/d22cffc8-58e9-43bc-958c-bf84dcbd3e21" width="500"><hr>
</div><br>

## What is LPM?
> LPM is a local password manager used via the Command Line Interface (CLI).
>

## How does it work?
> Your data is written to a certain file after being encrypted. When you need this data, it's decrypted and printed for you! The various other commands such as `edit`, `rm`, and `search` have their own methods but if you really want to know how everything works under the hood, just read the code!

## How do I download it?
> 1) Install PyInstaller 5.13.0.
> 2) Clone the repository and `cd` into it.
> 3) Run `pyinstaller --onefile --distpath bin --name lpm src/main.py` (or use the `tasks.json` method if you're using VSCode).
> 5) Add the path to the executable to your PATH variable.
> 6) Run `lpm` and enjoy :)
