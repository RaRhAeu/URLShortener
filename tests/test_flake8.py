from subprocess import CalledProcessError
from subprocess import check_output as run

FLAKE8_CMD = "flake8"
FLAKE8_INPUT = ["urlshortener", "tests"]


def test_flake8():
    """Run package through flake8"""
    try:
        run([FLAKE8_CMD, FLAKE8_INPUT[0]])
    except CalledProcessError as e:
        raise AssertionError("flake8 has found errors.\n\n" + e.output.decode("utf-8"))
    except OSError:
        raise OSError("Failed to run flake8. "
                      "Please check that you have installed it properly.")
