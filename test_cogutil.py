from cogutil import include_file, run_command

def test_file():
    me = __file__.rstrip("c")
    with open(me) as f:
        expected = f.read()
    assert include_file(me) == expected


def test_cmd():
    tp = run_command("seq 3")
    assert tp == "$ seq 3\n1\n2\n3\n"


def test_bad_cmd():
    tp = run_command("exit 17")
    assert tp == "$ exit 17\n(exit code: 17)\n"
