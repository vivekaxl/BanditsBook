import random
import math

import pandas as pd

class MultiArmedBandit():
    def __init__(self, name, db):
        self.name = name
        self.db = db
        self.count = db.copy()
        self.count[:] = 0
        self.reward = db.copy()
        self.reward[:] = 0

    def init(self):
        # Try to pull each arm, i.e., VM type
        for arm in self.count.columns:
            # @TODO: each workload will be drawn only once
            #workload_counts = self.count.sum(axis=1).sort(ascending=True, inplace=False).index
            workload_counts = self.count.sum(axis=1).astype(int)
            workload_counts = workload_counts[workload_counts == workload_counts.min()]
            self._pull(arm, workload_counts.index[0])
            #workload_counts = self.count.sum(axis=1).astype(int)
            #workload_counts = workload_counts[workload_counts <= 4]
            #self._pull(arm, random.choice(workload_counts.index))

    def select_arm(self):
        raise NotImplementedError()

    def _pull(self, arm, workload):
        # update records
        self.count.at[workload, arm] += 1
        self.reward.at[workload, arm] = self.db.at[workload, arm]
        # print('pull:', workload, arm)

    def smart_pull(self):
        workload_counts = self.count.sum(axis=1).astype(int)
        workload_counts = workload_counts[workload_counts == workload_counts.min()]
        for workload in workload_counts.index:
            arm = self.select_arm()
            # check the workload is already executed
            if self.count.at[workload, arm]:
                continue
            else:
                self._pull(arm, workload)
                break

    def xpull(self, arm):
        # @TODO: needs to be workload-aware? by per arm or aggregate counts?
        workload_pulled = self.count[arm]
        workload_pulled = workload_pulled[workload_pulled > 0]
        workload_counts = self.count.sum(axis=1).astype(int)
        workload_counts = workload_counts[workload_counts == workload_counts.min()]
        #print('pulled:', workload_pulled.index.tolist())
        #print('minimum:', workload_counts.index.tolist())
        candidate_workloads = workload_counts.index.difference(workload_pulled.index)
        if len(candidate_workloads) == 0:
            display(self.count.sum().sort(inplace=False))
            display(self.reward.mean().sort(inplace=False))
            #display(self.count)
        self._pull(arm, candidate_workloads[0])

    def xpull2(self, arm):
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

        self._pull(arm, workload)

    def xselect_pull(self, workload):
        candidate_arms = self.reward.mean(axis=0).sort(inplace=False, ascending=False).index
        # make sure each arm will be selected only once
        for arm in candidate_arms:
            if self.count.ix[workload, arm] == 0:
                reward = self.db.ix[workload, arm]
                self.count.ix[workload, arm] += 1
                self.reward.ix[workload, arm] = reward
                print('select pull:', workload, arm)
                break
            else:
                continue


class EpsilonGreedy(MultiArmedBandit):
    def __init__(self, db, epsilon):
        super().__init__("EpsilonGreedy-" + str(epsilon), db)
        self.epsilon = epsilon

    def select_arm(self):
        if random.random() > self.epsilon:
            # print('exploit')
            arm = self.reward.mean(axis=0).idxmax()
            return arm
        else:
            # print('explore')
            return random.choice(self.reward.columns)


    def smart_pull2(self):
        # not choosing only one arm to
        if random.random() > self.epsilon:
            # print('exploit')
            candidate_arms = self.reward.mean(axis=0).sort(inplace=False, ascending=False).index
        else:
            # print('explore')
            candidate_arms = self.reward.columns.tolist()
            random.shuffle(candidate_arms)
            # print('*', candidate_arms)

        while True:
            for arm in candidate_arms:
                workload_counts = self.count.sum(axis=1)
                workload_counts = workload_counts[workload_counts == workload_counts.min()]
                workload = random.choice(workload_counts.index)
                self._pull(arm, workload)
                break
                #count_record = self.count[arm]
                #candidate_workloads = count_record[count_record < 1].index
                #if len(candidate_workloads) > 0:
                #    workload = random.choice(candidate_workloads)
                #    reward = self.db.ix[workload, arm]
                #    self.count.ix[workload, arm] += 1
                #    self.reward.ix[workload, arm] = reward
                #    break
                #else:
                #    continue
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
        # @TODO: using sum might cause exp too large to compute
        rewards = self.reward.mean(axis=0)
        z = sum([math.exp(r / self.temperature) for r in rewards])
        probs = [math.exp(r / self.temperature) / z for r in rewards]
        arm = rewards.index[Softmax._categorical_draw(probs)]
        return arm


class UCB1(MultiArmedBandit):
    def __init__(self, db):
        super().__init__("UCB1", db)


    def select_arm(self):
        # make sure each arm is selected at least once
        counts = self.count.sum(axis=0)
        candidate_arms = counts[counts == 0].index
        if len(candidate_arms) > 0:
            return candidate_arms[0]

        # @TODO: sum makes it very slow
        rewards = self.reward.mean(axis=0)
        print(rewards)
        ucb_values = pd.Series([0.0 for _ in range(len(counts))], index=counts.index)
        total_counts = counts.sum()
        #for arm in counts.index:
        #    bonus = math.sqrt((2 * math.log(total_counts)) / float(counts[arm]))
        #    ucb_values[arm] = rewards[arm] + bonus
        # ucb_values = counts.apply(lambda x: math.sqrt((2 * math.log(counts.sum())) / x))
        # print('%', ucb_values)
        # print(ucb_values)
        ucb_values = pd.Series([rewards[arm] + math.sqrt((2 * math.log(total_counts)) / float(counts[arm])) for arm in counts.index], index=counts.index)
        arm = ucb_values.idxmax()
        print('selected:', arm)
        return arm


class RandomSearch:
    def __init__(self, name, db):
        self.name = name
        self.db = db
        self.count = db.copy()
        self.count[:] = 0
        self.reward = db.copy()
        self.reward[:] = 0

    def pull(self):
        while True:
            arm = random.choice(self.count.columns)
            workload = random.choice(self.count.index)
            if not self.count.at[workload, arm]:
                self.count.at[workload, arm] += 1
                self.reward.at[workload, arm] = self.db.at[workload, arm]
                break