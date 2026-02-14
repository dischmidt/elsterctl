"""Entrypoint for the elsterctl CLI."""

from dotenv import load_dotenv

from elsterctl.cli.root import main


load_dotenv(override=False)


if __name__ == "__main__":
    main()
