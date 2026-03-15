"""Hello World CLI demonstration using Typer."""

import typer

app = typer.Typer(
    name="hello",
    help="Simple Hello World CLI demonstration",
    add_completion=False,
)

GREETING_MESSAGE = "Hello, world!"


def hello() -> None:
    """Print a greeting message to the console.

    This is a simple demonstration function that prints
    "Hello, world!" to stdout.
    """
    print(GREETING_MESSAGE)


@app.command()
def main() -> None:
    """Main command that prints Hello, world!

    This is the default command executed when running the CLI.
    """
    hello()


if __name__ == "__main__":
    app()
