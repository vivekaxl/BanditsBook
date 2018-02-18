import random
import math

class MultiArmedBandit():
    def __init__(self, name, db):
        self.name = name
        self.db = db
        self.count = db.copy()
        self.count[:] = 0
        self.reward = db.copy()
        self.reward[:] = 0

    def init(self):
        for arm in self.count.columns:
            self.pull(arm)

    def select_arm(self):
        raise NotImplementedError()

    def pull(self, arm):
        # @TODO: needs to be workload-aware?
        count_record = self.count[arm]
        # print(arm, count_record)
        #max_count = count_record.max()
        #candidate_workloads = count_record[count_record < max_count].index
        candidate_workloads = count_record[count_record < 1].index
        if len(candidate_workloads) > 0:
            # already shuffled at initial phase
            workload = candidate_workloads[0]
            #workload = random.choice(candidate_workloads)
        else:
            # this may cause a problem when all the workloads are drawn?
            workload = random.choice(count_record.index)
        self.count.ix[workload, arm] += 1
        self.reward.ix[workload, arm] = self.db.ix[workload, arm]


    def select_pull(self, workload):
        candidate_arms = self.reward.mean(axis=0).sort(inplace=False, ascending=False).index
        for arm in candidate_arms:
            if self.count.ix[workload, arm] == 0:
                reward = self.db.ix[workload, arm]
                self.count.ix[workload, arm] += 1
                self.reward.ix[workload, arm] = reward
                break
            else:
                continue


class EpsilonGreedy(MultiArmedBandit):
    def __init__(self, db, epsilon):
        super().__init__("EpsilonGreedy-" + str(epsilon), db)
        self.epsilon = epsilon

    def select_arm(self):
        if random.random() > self.epsilon:
            arm = self.reward.sum(axis=0).idxmax()
            return arm
        else:
            return random.choice(self.reward.columns)

    def smart_pull(self):
        #print('@', self.epsilon)
        if random.random() > self.epsilon:
            # print('exploit')
            candidate_arms = self.reward.sum(axis=0).sort(inplace=False, ascending=False).index
        else:
            # print('explore')
            candidate_arms = self.reward.columns.tolist()
            random.shuffle(candidate_arms)
            # print('*', candidate_arms)

        while True:
            for arm in candidate_arms:
                # print(arm)
                count_record = self.count[arm]
                candidate_workloads = count_record[count_record < 1].index
                if len(candidate_workloads) > 0:
                    workload = random.choice(candidate_workloads)
                    reward = self.db.ix[workload, arm]
                    self.count.ix[workload, arm] += 1
                    self.reward.ix[workload, arm] = reward
                    break
                else:
                    continue
            break


class Softmax(MultiArmedBandit):
    def __init__(self, db, temperature):
        super().__init__("SoftMax-" + str(temperature), db)
        self.temperature = temperature

    @staticmethod
    def _categorical_draw(probs):
        z = random.random()
        cum_prob = 0.0
        for i in range(len(probs)):
            prob = probs[i]
            cum_prob += prob
            if cum_prob > z:
                return i
        return len(probs) - 1

    def select_arm(self):
        rewards = self.reward.mean(axis=0)
        z = sum([math.exp(r / self.temperature) for r in rewards])
        probs = [math.exp(r / self.temperature) / z for r in rewards]
        return rewards.index[Softmax._categorical_draw(probs)]


    def smart_pull(self):
        arm = self.select_arm()
        self.pull(arm)


class UCB1(MultiArmedBandit):
    def __init__(self, db):
        super().__init__("UCB1", db)


    def select_arm(self):
        counts = self.count.sum(axis=0)
        candidate_arms = counts[counts == 0].index
        if len(candidate_arms) > 0:
            return candidate_arms[0]

        ucb_values = counts.apply(lambda x: math.sqrt((2 * math.log(counts.sum())) / x))
        return ucb_values.idxmax()
        return

    def smart_pull(self):
        arm = self.select_arm()
        self.pull(arm)