import subprocess


def run_command(command: str) -> None:
    """Run a shell command and print its output."""
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e.stderr)
        exit(e.returncode)


def main() -> None:
    """Initialize the project with Poetry."""
    commands = ["poetry install --no-root", "poetry config virtualenvs.in-project true", "poetry shell", "exit"]

    for command in commands:
        run_command(command)


if __name__ == "__main__":
    main()
