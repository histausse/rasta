import re
from pathlib import Path
from more_itertools import peekable
from typing import Any, Optional, Type


class LoggedError:
    """A class representing an error parsed from a log file."""

    def __str__(self):
        pass

    def get_dict(self) -> dict:  # type: ignore
        pass

    def set_logfile_name(self, file: str):
        """Register the name of the file containing the error log"""
        self.logfile_name = file

    @staticmethod
    def parse_error(logs: "peekable[tuple[int, str]]") -> Optional["LoggedError"]:  # type: ignore
        pass


class JavaError(LoggedError):
    java_error_re = re.compile(
        r"(?:Exception in thread \".+?\"|Caused by:) ([a-zA-Z0-9.$]+?)(?:: *(.*))?(?: *~\[.*\])?$"
    )
    java_stack_re = re.compile(r"[ \t]*at (.*)\((.*?)(?::(\d*))?\)(?: *~\[.*\])?$")
    # TODO: link "Caused  by:" to exception?

    def __init__(
        self,
        first_line_nb: int,
        last_line_nb: int,
        error: str,
        msg: str,
        stack: list,
        logfile_name: str = "",
    ):
        self.first_line_nb = first_line_nb
        self.last_line_nb = last_line_nb
        self.error = error
        self.msg = msg
        self.stack = stack
        self.logfile_name = logfile_name

    def __str__(self):
        stack = "\n    at ".join(
            map(lambda e: f"{e['method']}({e['class']}:{e['line']})", self.stack)
        )
        return f"{self.error}: {self.msg}{stack}\n"

    def get_dict(self) -> dict:
        return {
            "error_type": "Java",
            "error": self.error,
            "msg": self.msg,
            "stack": self.stack,
            "first_line": self.first_line_nb,
            "last_line": self.last_line_nb,
            "logfile_name": self.logfile_name,
        }

    @staticmethod
    def parse_error(logs: "peekable[tuple[int, str]]") -> Optional["JavaError"]:
        """Return the JavaError at the begenning of the logs if there is one, else return None.
        If there is a JavaError at the begenning of the logs, the iterator of the logs will
        consume all the lines of the error, else the iterator will not be modified."""
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return None
        match = JavaError.java_error_re.match(line)
        if match is None:
            return None
        if match.group(2) is None:
            msg = ""
        else:
            msg = match.group(2)
        error = JavaError(line_nb, line_nb, match.group(1), msg, [])
        next(logs)
        while True:
            line_nb, line = logs.peek((None, None))
            if line is None or line_nb is None:
                return error
            match = JavaError.java_stack_re.match(line)
            if match is None:
                return error
            line_dsc = {
                "method": match.group(1),
                "class": match.group(2),
                "line": match.group(3),
            }
            if len(error.stack) == 0 or (
                error.stack[-1]["method"] != line_dsc["method"]
                and error.stack[-1]["class"] != line_dsc["method"]
            ):
                error.stack.append(line_dsc)
            error.last_line_nb = line_nb
            next(logs)


class NoPrefixJavaError(JavaError):
    java_error_re = re.compile(r"([a-zA-Z0-9.$]+?)(?:: *(.*))?(?: *~\[.*\])?$")
    java_stack_re = re.compile(r"[ \t]*at (.*)\((.*?)(?::(\d*))?\)(?: *~\[.*\])?$")

    @staticmethod
    def parse_error(
        logs: "peekable[tuple[int, str]]",
    ) -> Optional["NoPrefixJavaError"]:
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return None
        match = NoPrefixJavaError.java_error_re.match(line)
        if match is None:
            return None
        if match.group(2) is None:
            msg = ""
        else:
            msg = match.group(2)
        error = NoPrefixJavaError(line_nb, line_nb, match.group(1), msg, [])
        # Check that the next line match java_stack_re to reduce false possitives
        try:
            line_nb, line = logs[1]
        except IndexError:
            return None
        if NoPrefixJavaError.java_stack_re.match(line) is None:
            return None
        next(logs)
        while True:
            line_nb, line = logs.peek((None, None))
            if line is None or line_nb is None:
                return error
            match = NoPrefixJavaError.java_stack_re.match(line)
            if match is None:
                return error
            line_dsc = {
                "method": match.group(1),
                "class": match.group(2),
                "line": match.group(3),
            }

            if len(error.stack) == 0 or (
                error.stack[-1]["method"] != line_dsc["method"]
                and error.stack[-1]["class"] != line_dsc["method"]
            ):
                error.stack.append(line_dsc)
            error.last_line_nb = line_nb
            next(logs)
        return None


class PythonError(LoggedError):
    python_error_traceback_re = re.compile(r"Traceback \(most recent call last\):$")
    python_error_file_re = re.compile(r"  File \"(.+?)\", line (\d+?), in (.*)$")
    python_error_code_re = re.compile(r"    (.*)$")
    python_error_msg_re = re.compile(r"(.*?)(?:: (.*))?$")

    def __init__(
        self,
        first_line_nb: int,
        last_line_nb: int,
        error: str,
        msg: str,
        stack: list,
        logfile_name: str = "",
    ):
        self.first_line_nb = first_line_nb
        self.last_line_nb = last_line_nb
        self.error = error
        self.msg = msg
        self.stack = stack
        self.logfile_name = logfile_name

    def __str__(self):
        stack = "\n".join(
            map(
                lambda d: (
                    f"  File \"{d['file']}\", line {d['line']}, in {d['module']}\n"
                    f"    {d['code']}"
                ),
                self.stack,
            )
        )
        return (
            "Traceback (most recent call last):\n"
            f"{stack}\n"
            f"{self.error}: {self.msg}\n"
        )

    def get_dict(self) -> dict:
        return {
            "error_type": "Python",
            "error": self.error,
            "msg": self.msg,
            "stack": self.stack,
            "first_line": self.first_line_nb,
            "last_line": self.last_line_nb,
            "logfile_name": self.logfile_name,
        }

    # TODO: why peekable[str] crashes?
    @staticmethod
    def parse_error(logs: "peekable[tuple[int, str]]") -> Optional["PythonError"]:
        """Return the PythonError at the begenning of the logs if there is one, else return None.
        If there is a PythonError at the begenning of the logs, the iterator of the logs will
        consume all the lines of the error, else the iterator will not be modified."""
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return None
        match = PythonError.python_error_traceback_re.match(line)
        if match is None:
            return None
        error = PythonError(line_nb, line_nb, "", "", [])
        next(logs)
        while True:
            line_nb, line = logs.peek((None, None))
            if line is None or line_nb is None:
                break
            match = PythonError.python_error_file_re.match(line)
            if match is None:
                break
            new_stack_line = {
                "file": match.group(1),
                "line": match.group(2),
                "module": match.group(3),
                "code": "",
            }
            if len(error.stack) == 0 or error.stack[-1] != new_stack_line:
                error.stack.append(new_stack_line)
            error.last_line_nb = line_nb
            next(logs)
            line_nb, line = logs.peek((None, None))
            if line is None or line_nb is None:
                break
            match = PythonError.python_error_code_re.match(line)
            if match is None:
                break
            new_stack_line["code"] = match.group(1)
            error.last_line_nb = line_nb
            next(logs)
        line_nb, line = logs.peek((None, None))
        if line is None:
            raise RuntimeError("Found EOF before en of Python trackback")
        match = PythonError.python_error_msg_re.match(line)
        if match is None:
            raise RuntimeError("Last line of python traceback not found")
        error.error = match.group(1)
        error.msg = str(match.group(2))
        return error


class Python311Error(PythonError):
    python_code_marker_re = re.compile(r"^ *~*\^+~* *$")

    @staticmethod
    def parse_error(logs: "peekable[tuple[int, str]]") -> Optional["Python311Error"]:
        """Return the PythonError at the begenning of the logs if there is one, else return None.
        If there is a PythonError at the begenning of the logs, the iterator of the logs will
        consume all the lines of the error, else the iterator will not be modified."""
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return None
        match = PythonError.python_error_traceback_re.match(line)
        if match is None:
            return None
        error = PythonError(line_nb, line_nb, "", "", [])
        next(logs)
        while True:
            line_nb, line = logs.peek((None, None))
            if line is None or line_nb is None:
                break
            match = PythonError.python_error_file_re.match(line)
            if match is None:
                break
            new_stack_line = {
                "file": match.group(1),
                "line": match.group(2),
                "module": match.group(3),
                "code": "",
            }
            if len(error.stack) == 0 or error.stack[-1] != new_stack_line:
                error.stack.append(new_stack_line)
            error.last_line_nb = line_nb
            next(logs)
            line_nb, line = logs.peek((None, None))
            if line is None or line_nb is None:
                break
            match = PythonError.python_error_code_re.match(line)
            if match is None:
                break
            new_stack_line["code"] = match.group(1)
            error.last_line_nb = line_nb
            next(logs)
            line_nb, line = logs.peek((None, None))
            if line is None or line_nb is None:
                break
            match = Python311Error.python_code_marker_re.match(line)
            if match is not None:
                next(logs)
        line_nb, line = logs.peek((None, None))
        if line is None:
            raise RuntimeError("Found EOF before en of Python trackback")
        match = PythonError.python_error_msg_re.match(line)
        if match is None:
            raise RuntimeError("Last line of python traceback not found")
        error.error = match.group(1)
        error.msg = str(match.group(2))
        return error


class RubyError(LoggedError):
    ruby_error_re = re.compile(r"(.*?\.rb):(\d*):in `(.*?)'(?:: (.*))?$")
    ruby_stack_re = re.compile(r"[ \t]*from (.*?\.rb):(\d*):in `(.*?)'")

    def __init__(
        self,
        first_line_nb: int,
        last_line_nb: int,
        file: str,
        line: str,
        function: str,
        msg: str,
        stack: list,
        logfile_name: str = "",
    ):
        self.first_line_nb = first_line_nb
        self.last_line_nb = last_line_nb
        self.file = file
        self.line = line
        self.function = function
        self.msg = msg
        self.stack = stack
        self.logfile_name = logfile_name

    def __str__(self):
        stack = "\n    at ".join(
            map(
                lambda e: f"from {e['file']}:({e['line']}:in `{e['function']}')",
                self.stack,
            )
        )
        return f"{self.file}:{self.line}:in `{self.function}':{self.msg}{stack}\n"

    def get_dict(self) -> dict:
        return {
            "error_type": "Ruby",
            "file": self.file,
            "line": self.line,
            "function": self.function,
            "msg": self.msg,
            "stack": self.stack,
            "first_line": self.first_line_nb,
            "last_line": self.last_line_nb,
            "logfile_name": self.logfile_name,
        }

    @staticmethod
    def parse_error(logs: "peekable[tuple[int, str]]") -> Optional["RubyError"]:
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return None
        match = RubyError.ruby_error_re.match(line)
        if match is None:
            return None
        if match.group(4) is None:
            msg = ""
        else:
            msg = match.group(4)
        error = RubyError(
            line_nb, line_nb, match.group(1), match.group(2), match.group(3), msg, []
        )
        next(logs)
        while True:
            line_nb, line = logs.peek((None, None))
            if line is None or line_nb is None:
                return error
            match = RubyError.ruby_stack_re.match(line)
            if match is None:
                return error
            line_dsc = {
                "file": match.group(1),
                "line": match.group(2),
                "function": match.group(3),
            }
            if len(error.stack) == 0 or error.stack[-1] != line_dsc:
                error.stack.append(line_dsc)
            error.last_line_nb = line_nb
            next(logs)


class FlowdroidLog4jError(LoggedError):
    error_re = re.compile(r"\[.*?\] (ERROR|FATAL) (.*?) - (.*)$")

    def __init__(
        self,
        first_line_nb: int,
        last_line_nb: int,
        level: str,
        origin: str,
        msg: str,
        logfile_name: str = "",
    ):
        self.first_line_nb = first_line_nb
        self.last_line_nb = last_line_nb
        self.level = level
        self.origin = origin
        self.msg = msg
        self.logfile_name = logfile_name

    def __str__(self) -> str:
        return f"{self.level} {self.origin} {self.msg}"

    def get_dict(self) -> dict:
        return {
            "error_type": "Log4j",
            "level": self.level,
            "origin": self.origin,
            "msg": self.msg,
            "first_line": self.first_line_nb,
            "last_line": self.last_line_nb,
            "logfile_name": self.logfile_name,
        }

    @staticmethod
    def parse_error(logs: peekable) -> Optional["FlowdroidLog4jError"]:
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return None
        match = FlowdroidLog4jError.error_re.match(line)
        if match is None:
            return None
        error = FlowdroidLog4jError(
            line_nb, line_nb, match.group(1), match.group(2), match.group(3)
        )
        next(logs)
        return error


class DroidsafeLog4jError(LoggedError):
    error_re = re.compile(r"(ERROR|FATAL): (.*)")

    def __init__(
        self,
        first_line_nb: int,
        last_line_nb: int,
        level: str,
        msg: str,
        logfile_name: str = "",
    ):
        self.first_line_nb = first_line_nb
        self.last_line_nb = last_line_nb
        self.level = level
        self.msg = msg
        self.logfile_name = logfile_name

    def __str__(self) -> str:
        return f"{self.level}: {self.msg}"

    def get_dict(self) -> dict:
        return {
            "error_type": "Log4jSimpleMsg",
            "level": self.level,
            "msg": self.msg,
            "first_line": self.first_line_nb,
            "last_line": self.last_line_nb,
            "logfile_name": self.logfile_name,
        }

    @staticmethod
    def parse_error(logs: peekable) -> Optional["DroidsafeLog4jError"]:
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return None
        match = DroidsafeLog4jError.error_re.match(line)
        if match is None:
            return None
        error = DroidsafeLog4jError(line_nb, line_nb, match.group(1), match.group(2))
        next(logs)
        return error


# def get_errors(path: Path, error_types: list[Type[LoggedError]]) -> list[LoggedError]:
def get_errors(path: Path, error_types: list) -> list:
    """List the errors found in the logs collected from the analusis of an apk.
    The file containing the error traces must be located at `path`, and the list
    of type of error expected must be provided in `error_types`."""
    if not path.exists():
        raise RuntimeError(f"Error log {path} not found")
    if not error_types:
        return []
    errors = []
    with path.open("r", errors="replace") as file:
        logs = peekable(enumerate(file))
        while logs.peek(None) is not None:
            new_errors = []
            for error_type in error_types:
                error = error_type.parse_error(logs)
                if error is not None:
                    new_errors.append(error)
            if new_errors:
                errors.extend(new_errors)
            else:
                next(logs)
    for error in errors:
        error.set_logfile_name(path.name)
    return errors
