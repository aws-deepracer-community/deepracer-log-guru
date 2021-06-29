#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import os

from src.log.log import LOG_FILE_SUFFIX, Log, META_FILE_SUFFIX


def refresh_all_log_meta(please_wait, log_directory):
    please_wait.start("Refreshing")
    log_files = []
    for f in os.listdir(log_directory):
        if f.endswith(LOG_FILE_SUFFIX):
            log_files.append(f)
    import_new_logs(log_files, please_wait, log_directory)


def import_new_logs(log_files, please_wait, log_directory):
    please_wait.start("Importing")
    total_count = len(log_files)
    for i, f in enumerate(log_files):
        log = Log(log_directory)
        log.parse(f, please_wait, i / total_count * 100, (i + 1) / total_count * 100)
        log.save()


def get_model_info_for_open_model_dialog(track, log_directory):
    all_logs_count = 0
    model_names = []
    model_logs = {}
    for f in os.listdir(log_directory):
        if f.endswith(META_FILE_SUFFIX):
            all_logs_count += 1
            log = Log(log_directory)
            log.load_meta(f)

            if track.has_world_name(log.get_log_meta().world_name):
                model_name = log.get_log_meta().model_name
                model_names.append(model_name)
                model_logs[model_name] = log
    return model_logs, model_names, all_logs_count


def get_possible_new_model_log_files(log_directory: str):
    new_log_files = []

    all_files = os.listdir(log_directory)
    for f in all_files:
        if f.endswith(LOG_FILE_SUFFIX):
            expected_meta = f + META_FILE_SUFFIX
            if expected_meta not in all_files:
                new_log_files.append(f)

    return new_log_files


def get_world_names_of_existing_logs(log_directory):
    world_names = set()
    for f in os.listdir(log_directory):
        if f.endswith(META_FILE_SUFFIX):
            log = Log(log_directory)
            log.load_meta(f)
            world_names.add(log.get_log_meta().world_name)
    return world_names
