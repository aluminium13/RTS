import simpy
import random
from math import log
from numpy import linspace
import matplotlib.pyplot as plt

solution_time1 = 0.04542405128479004
solution_time2 = 0.06445979595184326

SIMULATION_TIME = 10

completed = []
generated = 0

statistics = {
    'intencities': [],
    'avg_wait': [],
    'avg_idle': [],
    'avg_len': [],
    'pri_wait': dict()
}


class Job:

    def __init__(self, pid, arrive_t, env):
        self.id = pid
        self.env = env
        self.arrive_t = arrive_t
        self.deadline_t = self.arrive_t + solution_time1 * random.randint(2, 10)
        self.service_t = solution_time1
        self.finish_t = 0
        self.remain_t = self.service_t
        self.trnd_t = 0
        self.wait_t = 0
        self.initial_wait = 0
        self.priority = 0
        self.avg_len = 0

    def get_turnaround(self, finish_t):
        self.finish_t = finish_t
        self.trnd_t = self.finish_t - self.arrive_t
        self.wait_t = self.trnd_t - self.service_t
        return self.trnd_t, self.wait_t


def rate_monotonic(env, cpu, process):
    with cpu.request(process.priority) as req:
        current = env.now
        try:
            yield req

            terminated = env.process(cpu.do_job(env, process))
            rejection_t = process.deadline_t - env.now
            if rejection_t < 0:
                return
            rejection = env.timeout(process.deadline_t - env.now)

            yield terminated | rejection

            if not terminated.triggered:
                terminated.interrupt('rejected')
                cpu.waiting -= 1
            else:
                process.get_turnaround(env.now)
                cpu.waiting -= 1
                process.avg_len = cpu.waiting
                print('task %i finished at %d' % (process.id, env.now))
                completed.append(process)
        except simpy.Interrupt:
            processed = env.now - current
            process.remain_t -= processed
            print('priority overcome, processed this task for %d,(%s)' %
                  (processed))


class CPU(simpy.PriorityResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = args
        self.waiting = 0
        self.total_t = 0
        self.rejected = [[0, 0]]

    def request(self, *args, **kwargs):
        self.waiting += 1
        before_cleaning = len(self.queue)
        self.queue = list(filter(lambda x: x.deadline_t > env.now, self.queue))
        if len(self.queue) - before_cleaning != 0:
            self.rejected.append([env.now, self.rejected[-1][1] + before_cleaning - len(self.queue)])
        self.queue = sorted(self.queue, key=lambda x: -x.service_t)
        for i, _ in enumerate(self.queue):
            self.queue[i].priority = i
        return super().request(*args, **kwargs)

    def release(self, *args, **kwargs):
        self.total_t += self._env.now - args[0].usage_since
        return super().release(*args, **kwargs)

    def do_job(self, env, pid):
        try:
            yield env.timeout(pid.remain_t)
        except simpy.Interrupt as i:
            print('interrupted', i.cause)
            self.rejected.append([env.now, self.rejected[-1][1] + 1])


def simulation(env, cpu, intensity):
    global generated
    i = 0
    while True:
        next_time = -1/intensity * log(random.uniform(0, 1))
        yield env.timeout(next_time)
        process = Job(i, env.now, env)
        generated += 1
        env.process(rate_monotonic(env, cpu, process))

        i += 1


# intensities = [0.05 * i for i in range(1, 200)]
# for t in linspace(0.05, 10.0):
#     completed = []
#     env = simpy.Environment()
#     cpu = CPU(env)
#     env.process(simulation(env, cpu, t))
#     env.run(until=SIMULATION_TIME)

#     statistics['intencities'].append(t)
#     statistics['avg_wait'].append(sum(proc.wait_t for proc in completed) / len(completed))
#     statistics['avg_len'].append(sum(proc.avg_len for proc in completed) / len(completed))
#     statistics['avg_idle'].append(100 - (cpu.total_t / SIMULATION_TIME) * 100)

# fig, (ax0, ax1, ax2) = plt.subplots(3, 1)

# statistics['avg_len'] = [x for _,x in sorted(zip(statistics['avg_wait'], statistics['avg_len']))]
# statistics['avg_wait'] = sorted(statistics['avg_wait'])

# ax0.plot(statistics['intencities'], statistics['avg_wait'])
# ax0.set_xlabel('intencities')
# ax0.set_ylabel('avg wait')

# ax1.plot(statistics['intencities'], statistics['avg_idle'])
# ax1.set_xlabel('intencities')
# ax1.set_ylabel('avg idle %')

# ax2.plot(statistics['avg_wait'], statistics['avg_len'])
# ax2.set_xlabel('avg wait')
# ax2.set_ylabel('avg queue len')

# plt.show()
# plt.savefig("RM.png")

env = simpy.Environment()
cpu = CPU(env)
env.process(simulation(env, cpu, 10))
env.run(until=1000)

data = list(zip(*cpu.rejected))
plt.plot(data[0], data[1])
plt.show()