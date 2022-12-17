from .position import Position
##################################
# ERRORS
##################################


class Error:
    def __init__(self, pos_start: Position, pos_end: Position, error_name: str, details: str) -> None:
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        return f'{self.error_name}: {self.details}\n' \
            f'File {self.pos_start.filename}, Line {self.pos_start.line+1}'


class IllegalCharError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details: str) -> None:
        super().__init__(pos_start, pos_end, 'Illegal Character', details)
