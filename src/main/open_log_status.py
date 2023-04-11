from log.log import Log


class OpenLogStatus:
    def __init__(self):
        self._log: Log | None = None
        self._model_name = ""

    def open_log(self, log: Log, model_name: str):
        self._log = log
        self._model_name = model_name

    def get_log(self):
        return self._log

    def get_model_name(self):
        return self._model_name


