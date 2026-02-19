""" Contains the `Cli` class that handles command-line stuff. """


class Cli:
  """
  Handles command-line stuff like flags & arguments.
  """

  VERSION = "0.0.1-dev"  # Initial release. Shit does NOT work yet.

  FLAGS = {
  """ Easy way to know what flags are set for runtime. """
    # "help": False,
    # "version": False,
    "parent": False,
    "email": False,
    "username": False,
    "password": False,
    "import": False,
    "export": False,
    "plaintext": False,
    "wipe": False,
    "reforge": False,
    "oldkey": False,
    "newkey": False,
  }

  HELP = """
          optional | required
Usage: lpm [-flags] <action>
Flags:
  -help     | -h    Help menu.
  -version  | -v    Version info.
  -verbose  | -vb   Verbose output.
  -parent   | -p    Input parent name.
  -email    | -e    Input email address.
  -username | -u    Input username.
  -password | -pw   Input password.
  -import   | -im   Import data with the old key. It will be re-encrypted with your current key.
  -export   | -ex   Export data as-is or to plaintext.
  -wipe     | -w    Deletes ALL saved data and the key. You will have to set up a new one.
  -reforge  | -rf   Prompts you with the current key, then for a new one, then re-encrypts everything with the new key.
"""

  @staticmethod
  def parse_args(argv: list[str]) -> tuple[list[str], str]:
    """ Reads flags and the action the user wants to perform. """

    flags = [arg[1:] for arg in argv if arg[0] == '-']  # Strip the '-' from arg.
    action = argv[-1] if argv[-1][0] != '-' else None

    return flags, action

  @staticmethod
  def process_args(flags: list[str]) -> None:
    """
    Sets corresponding flags in `Cli.FLAGS` to `True`,
    or does something based on the flag (like print `Cli.HELP` for `-help` / `-h`.)
    """

    for flag in flags:
      match flag:
        case "help"     | 'h': print(Cli.HELP)
        case "version"  | 'v': print(Cli.VERSION)
        case "verbose"  | 'vb': Cli.FLAGS["verbose"]  = True
        case "parent"   | 'p': Cli.FLAGS["parent"]    = True
        case "email"    | 'e': Cli.FLAGS["email"]     = True
        case "username" | 'u': Cli.FLAGS["username"]  = True
        case "password" | 'pw': Cli.FLAGS["password"] = True
        case "import"   | 'i': Cli.FLAGS["import"]    = True
        case "export"   | 'e': Cli.FLAGS["export"]    = True
        case "wipe"     | 'w': Cli.FLAGS["wipe"]      = True
        case "reforge"  | 'r': Cli.FLAGS["reforge"]   = True
        case _: ...
