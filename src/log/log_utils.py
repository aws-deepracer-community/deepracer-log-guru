#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import os

from log.log_meta import LogMeta
from main.version import VERSION
from src.log.log import LOG_FILE_SUFFIX, Log, META_FILE_SUFFIX, CONSOLE_LOG_SUFFIX, make_new_log_meta
from tracks.track import Track
from ui.please_wait import PleaseWait


#
# Public Interface
#

class OpenFileInfo:
    def __init__(self, display_name: str, log_meta: LogMeta, source_meta_files: list[str]):
        self.display_name = display_name
        self.log_meta = log_meta
        self.source_files = source_meta_files


def get_model_info_for_open_model_dialog(track: Track, log_directory: str, please_wait: PleaseWait) -> (list[OpenFileInfo], int):
    _refresh_meta(log_directory, please_wait)
    log_info, excluded_log_count = _get_open_file_model_info(track, log_directory)
    _add_multi_worker_log_info(log_info)
    _fix_worker_log_info_duplicates(log_info)
    _fix_remaining_log_info_duplicates(log_info)
    return _sorted_log_info(log_info), excluded_log_count


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


def _is_log_valid(meta_file: str, all_files: list, log_directory: str):
    log_file = meta_file[:-len(META_FILE_SUFFIX)]
    if log_file not in all_files:
        return False
    try:
        log = Log(log_directory)
        log.load_meta(meta_file)
        return log.get_log_meta().guru_version.get() == VERSION and log.get_log_meta().matches_os_stats(
            os.stat(os.path.join(log_directory, log_file)))
    except Exception:  # TODO proper exception class for Guru
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
        try:
            log.parse(f, please_wait, i / total_count * 100, (i + 1) / total_count * 100)
            log.save()
        except Exception as ex:  # TODO - Trapping specific exceptions not working (Python issue?)
            print("Skipping file <{}> due to processing error <{}>".format(f, ex))
    please_wait.stop()


def _get_open_file_model_info(track: Track, log_directory: str) -> (list[OpenFileInfo], int):
    excluded_log_count = 0
    log_info = []

    for f in os.listdir(log_directory):
        if f.endswith(META_FILE_SUFFIX):
            log = Log(log_directory)
            log.load_meta(f)
            if track.has_world_name(log.get_log_meta().track_name.get()):
                log_meta = log.get_log_meta()
                display_name = log_meta.model_name.get()
                meta_filenames = [f]
                log_info.append(OpenFileInfo(display_name, log_meta, meta_filenames))
            else:
                excluded_log_count += 1

    return log_info, excluded_log_count


def _add_multi_worker_log_info(log_info: list[OpenFileInfo]):
    model_workers = {}
    for log in log_info:
        log_meta = log.log_meta
        if log_meta.workers.get() >= 2:
            model_name = log_meta.model_name.get()
            if model_name in model_workers:
                model_workers[model_name][log_meta.worker_id.get()] = log
            else:
                model_workers[model_name] = {log_meta.worker_id.get(): log}
    for model_name, workers in model_workers.items():
        keys = list(workers.keys())
        if len(keys) > 1:
            source_files = []
            log_metas = []
            for i in sorted(keys):
                source_files.append(workers[i].source_files[0])
                log_metas.append(workers[i].log_meta)
            meta_data = make_new_log_meta()
            meta_data.merge_from_multi_logs(log_metas)
            log_info.append(OpenFileInfo(model_name + " (multi-worker)", meta_data, source_files))


def _fix_worker_log_info_duplicates(log_info: list[OpenFileInfo]):
    used_names = []
    duplicate_names = []
    for log in log_info:
        if log.display_name in used_names:
            duplicate_names.append(log.display_name)
        else:
            used_names.append(log.display_name)
    for log in log_info:
        if log.display_name in duplicate_names and log.log_meta.workers.get() > 1:
            log.display_name += f" (worker {log.log_meta.worker_id.get() + 1} / {log.log_meta.workers.get()})"


def _fix_remaining_log_info_duplicates(log_info: list[OpenFileInfo]):
    used_names = []
    for log in log_info:
        old_name = log.display_name
        new_name = old_name
        i = 1
        while new_name in used_names:
            new_name = f"{old_name} ({i})"
            i += 1
        log.display_name = new_name
        used_names.append(new_name)


def _sorted_log_info(log_info: list[OpenFileInfo]):
    all_names = []
    indexed_logs = {}

    for log in log_info:
        all_names.append(log.display_name)
        indexed_logs[log.display_name] = log

    result = []
    for name in sorted(all_names):
        result.append(indexed_logs[name])

    return result
