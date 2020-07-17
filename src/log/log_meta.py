from src.action_space.action import MAX_POSSIBLE_ACTIONS

class LogMeta:

    def __init__(self):
        self.hyper = LogMeta.HyperMeta()
        self.episode_stats = LogMeta.EpisodeStats()

        self.model_name = ""

        self.world_name = ""
        self.race_type = ""
        self.job_type = ""

        self.action_space = [None] * MAX_POSSIBLE_ACTIONS

    class EpisodeStats:
        def __init__(self):
            self.episode_count = 0
            self.success_count = 0
            self.iteration_count = 0

            self.average_percent_complete = 0.0

            self.best_steps = 0
            self.average_steps = 0
            self.worst_steps = 0

            self.best_distance = 0.0
            self.average_distance = 0.0
            self.worst_distance = 0.0

            self.best_reward = 0.0
            self.average_reward = 0.0
            self.worst_reward = 0.0

        def display_for_debug(self):
            print("    Episode count = ", self.episode_count)
            print("    Interation count = ", self.iteration_count)
            print("    Success count = ", self.success_count)
            print("    Success percent = ", round(self.success_count / self.episode_count * 100))

            print("    Average Percent Complete % = ", round(self.average_percent_complete))

            print("    Best steps = ", self.best_steps)
            print("    Average steps = ", self.average_steps)
            print("    Worst steps = ", self.worst_steps)

            print("    Best distance = ", round(self.best_distance, 2))
            print("    Average distance = ", round(self.average_distance, 2))
            print("    Worst distance = ", round(self.worst_distance, 2))



    class HyperMeta:
        def __init__(self):
            self.batch_size = 0
            self.entropy = 0.0
            self.discount_factor = 0.0
            self.loss_type = ""
            self.learning_rate = 0
            self.episodes_between_training = 0
            self.epochs = 0

        def display_for_debug(self):
            print("    Batch size = ", self.batch_size)
            print("    Entropy = ", self.entropy)
            print("    Discount factor = ", self.discount_factor)
            print("    Loss type = ", self.loss_type)
            print("    Learning rate = ", self.learning_rate)
            print("    Episodes between training = ", self.episodes_between_training)
            print("    Epochs = ", self.epochs)


    def display_for_debug(self):

        print("Model name = ", self.model_name)

        print("World name = ", self.world_name)
        print("Race type = ", self.race_type)
        print("Job type = ", self.job_type)

        print("Hyper:")
        self.hyper.display_for_debug()

        print("Episode Stats:")
        self.episode_stats.display_for_debug()