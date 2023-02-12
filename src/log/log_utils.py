#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import os

from main.version import VERSION
from src.log.log import LOG_FILE_SUFFIX, Log, META_FILE_SUFFIX, CONSOLE_LOG_SUFFIX
from tracks.track import Track
from ui.please_wait import PleaseWait


#
# Public Interface
#

def get_model_info_for_open_model_dialog(track: Track, log_directory: str, please_wait: PleaseWait):
    _refresh_meta(log_directory, please_wait)
    return _get_model_info(track, log_directory)


def get_world_names_of_existing_logs(log_directory: str, please_wait: PleaseWait):
    _refresh_meta(log_directory, please_wait)
    world_names = set()
    for f in os.listdir(log_directory):
        if f.endswith(META_FILE_SUFFIX):
            log = Log(log_directory)
            log.load_meta(f)
            world_names.add(log.get_log_meta().track_name.get())
    return world_names


#
# PRIVATE Implementation Helpers
#

def _refresh_meta(log_directory: str, please_wait: PleaseWait):
    _remove_invalid_meta_files(log_directory)
    logs_without_meta = _get_log_files_without_meta(log_directory)
    _import_logs_without_meta(logs_without_meta, please_wait, log_directory)


def _remove_invalid_meta_files(log_directory: str) -> None:
    all_files = os.listdir(log_directory)
    for f in all_files:
        if f.endswith(META_FILE_SUFFIX):
            if not _is_log_valid(f, all_files, log_directory):
                os.remove(os.path.join(log_directory, f))


def _is_log_valid(file: str, all_files: list, log_directory: str):
    if file[:-len(META_FILE_SUFFIX)] not in all_files:
        return False
    try:
        log = Log(log_directory)
        log.load_meta(file)
        return log.get_log_meta().guru_version.get() == VERSION
    except Exception:       # TODO proper exception class for Guru
        return False


def _get_log_files_without_meta(log_directory: str):
    log_files = []

    all_files = os.listdir(log_directory)
    for f in all_files:
        if f.endswith(LOG_FILE_SUFFIX) or f.endswith(CONSOLE_LOG_SUFFIX):
            expected_meta = f + META_FILE_SUFFIX
            if expected_meta not in all_files:
                log_files.append(f)

    return log_files


def _import_logs_without_meta(log_files: list, please_wait: PleaseWait, log_directory: str):
    please_wait.start("Importing")
    total_count = len(log_files)
    for i, f in enumerate(log_files):
        log = Log(log_directory)
        log.parse(f, please_wait, i / total_count * 100, (i + 1) / total_count * 100)
        log.save()
    please_wait.stop()


def _get_model_info(track: Track, log_directory: str):
    all_logs_count = 0
    model_names = []
    model_logs = {}
    for f in os.listdir(log_directory):
        if f.endswith(META_FILE_SUFFIX):
            all_logs_count += 1
            log = Log(log_directory)
            log.load_meta(f)

            if track.has_world_name(log.get_log_meta().track_name.get()):
                model_name = log.get_log_meta().model_name.get()
                model_names.append(model_name)
                model_logs[model_name] = log
    return model_logs, model_names, all_logs_count


