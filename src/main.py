""" Entry point. """


from cli import Cli
from sys import argv

if __name__ == "__main__":
  flags, action = Cli.parse_args(argv)  # Unpack.
