import subprocess


def test_run():
    command = "python3 run.py"
    try:
        subprocess.check_call(command, shell=True)
        assert True
    except subprocess.CalledProcessError:
        assert False
