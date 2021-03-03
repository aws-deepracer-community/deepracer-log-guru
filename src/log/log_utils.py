import os

from src.log.log import LOG_FILE_SUFFIX, Log, META_FILE_SUFFIX


def refresh_all_log_meta(please_wait):
    please_wait.start("Refreshing")
    log_files = []
    for f in os.listdir(os.curdir):
        if f.endswith(LOG_FILE_SUFFIX):
            log_files.append(f)
    import_new_logs(log_files, please_wait)


def import_new_logs(log_files, please_wait):
    please_wait.start("Importing")
    total_count = len(log_files)
    for i, f in enumerate(log_files):
        log = Log()
        log.parse(f, please_wait, i / total_count * 100, (i + 1) / total_count * 100)
        log.save()


def get_model_info_for_open_model_dialog(track):
    model_names = []
    model_files = {}
    for f in os.listdir(os.curdir):
        if f.endswith(META_FILE_SUFFIX):
            log = Log()
            log.load_meta(f)

            if track.has_world_name(log.get_log_meta().world_name):
                model_name = log.get_log_meta().model_name
                model_names.append(model_name)
                model_files[model_name] = f
    return model_files, model_names


def get_possible_new_model_log_files():
    new_log_files = []

    all_files = os.listdir(os.curdir)
    for f in all_files:
        if f.endswith(LOG_FILE_SUFFIX):
            expected_meta = f + META_FILE_SUFFIX
            if expected_meta not in all_files:
                new_log_files.append(f)

    return new_log_files
