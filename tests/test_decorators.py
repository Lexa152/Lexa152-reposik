import os
import pytest
from src.decorators import log


def test_log_success_to_console(capsys):
    @log()
    def add(x, y):
        return x + y

    result = add(1, 2)
    assert result == 3

    captured = capsys.readouterr()
    # Теперь логи в stdout, проверяем captured.out
    assert "add start" in captured.out
    assert "add ok" in captured.out


def test_log_error_to_console(capsys):
    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "divide start" in captured.out
    assert "divide error: ZeroDivisionError" in captured.out


def test_log_success_to_file(tmp_path):
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def multiply(x, y):
        return x * y

    result = multiply(3, 4)
    assert result == 12

    content = log_file.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    assert len(lines) == 2
    assert lines[0] == "multiply start"
    assert lines[1] == "multiply ok"


def test_log_error_to_file(tmp_path):
    log_file = tmp_path / "errorlog.txt"

    @log(filename=str(log_file))
    def bad_func(x, y):
        if y == 0:
            raise ValueError("y cannot be zero")
        return x // y

    with pytest.raises(ValueError):
        bad_func(10, 0)

    content = log_file.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    assert len(lines) == 2
    assert lines[0] == "bad_func start"
    assert lines[1].startswith("bad_func error: ValueError")
    assert "Inputs: (10, 0)" in lines[1]


def test_log_with_kwargs(capsys):
    @log()
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")
    assert result == "Hi, Alice!"

    captured = capsys.readouterr()
    assert "greet start" in captured.out
    assert "greet ok" in captured.out


def test_log_preserves_function_metadata():
    @log()
    def sample(x):
        """Sample function docstring."""
        return x

    assert sample.__name__ == "sample"
    assert sample.__doc__ == "Sample function docstring."


