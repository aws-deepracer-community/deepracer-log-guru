from src.log.log_meta import LogMeta

def analyze_episode_details(episodes, log_meta :LogMeta):

    log_meta.episode_stats.episode_count = len(episodes)
    log_meta.episode_stats.iteration_count = episodes[-1].iteration + 1

    total_success_steps = 0
    total_success_distance = 0.0
    total_percent_complete = 0.0

    for e in episodes:
        total_percent_complete += e.percent_complete

        if e.lap_complete:
            log_meta.episode_stats.success_count += 1

            total_success_steps += e.step_count
            total_success_distance += e.distance_travelled

            if log_meta.episode_stats.best_steps == 0 or e.step_count < log_meta.episode_stats.best_steps:
                log_meta.episode_stats.best_steps = e.step_count

            if log_meta.episode_stats.worst_steps < e.step_count:
                log_meta.episode_stats.worst_steps = e.step_count

            if log_meta.episode_stats.best_distance == 0.0 or e.distance_travelled < log_meta.episode_stats.best_distance:
                log_meta.episode_stats.best_distance = e.distance_travelled

            if log_meta.episode_stats.worst_distance < e.distance_travelled:
                log_meta.episode_stats.worst_distance = e.distance_travelled

    if log_meta.episode_stats.success_count > 0:
        log_meta.episode_stats.average_steps = int(round(total_success_steps / log_meta.episode_stats.success_count))
        log_meta.episode_stats.average_distance = total_success_distance / log_meta.episode_stats.success_count

    if log_meta.episode_stats.episode_count > 0:
        log_meta.episode_stats.average_percent_complete = total_percent_complete / log_meta.episode_stats.episode_count

