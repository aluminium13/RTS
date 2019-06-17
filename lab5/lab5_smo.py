import simpy
import random
from math import log
from collections import Counter
import matplotlib.pyplot as plt
from numpy import linspace

solution_time = [0.04542405128479004, 0.06445979595184326]

SIMULATION_TIME = 100

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
        self.service_t = solution_time[random.randint(0,1)]
        self.finish_t = 0
        self.remain_t = self.service_t
        self.trnd_t = 0
        self.wait_t = 0
        self.initial_wait = 0
        self.priority = 0
        self.avg_len = 0
        self.deadline = self.arrive_t + self.service_t * random.randint(2, 10)

    def get_turnaround(self, finish_t):
        self.finish_t = finish_t
        self.trnd_t = self.finish_t - self.arrive_t
        self.wait_t = self.trnd_t - self.service_t
        return self.trnd_t, self.wait_t


def rm(env, cpu, process):
    with cpu.request(process.priority) as req:
        current = env.now
        try:
            yield req
            yield env.timeout(process.remain_t)
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


def simulation(env, cpu, intensity):
    global generated
    i = 0
    while True:
        next_time = -1/intensity * log(random.uniform(0, 1))
        yield env.timeout(next_time)
        process = Job(i, env.now, env)
        generated += 1
        print('task %i comes at %d' % (i, env.now), end=' ')
        env.process(rm(env, cpu, process))
        i += 1


class CPU(simpy.PreemptiveResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = args
        self.waiting = 0
        self.total_t = 0

    def request(self, *args, **kwargs):
        self.waiting += 1
        self.queue = sorted(self.queue, key=lambda x: -x.service_t)
        self.queue = list(filter(lambda x: x.deadline_t > env.now, self.queue))
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


for t in linspace(0.01, 1, num=20):
    completed = []
    env = simpy.Environment()
    cpu = CPU(env)
    env.process(simulation(env, cpu, t))
    env.run(until=SIMULATION_TIME)
    
    statistics['intencities'].append(t)
    statistics['avg_wait'].append(sum(proc.wait_t for proc in completed) / len(completed))
    statistics['avg_len'].append(sum(proc.avg_len for proc in completed) / len(completed))
    statistics['avg_idle'].append(100 - (cpu.total_t / SIMULATION_TIME) * 100)

fig, (ax0, ax1, ax2) = plt.subplots(3, 1)

statistics['avg_len'] = [x for _,x in sorted(zip(statistics['avg_wait'], statistics['avg_len']))]
statistics['avg_wait'] = sorted(statistics['avg_wait'])

ax0.plot(statistics['intencities'], statistics['avg_wait'])
ax0.set_xlabel('avg wait')
ax0.set_ylabel('avg queue len')

ax1.plot(statistics['intencities'], statistics['avg_wait'])
ax1.set_xlabel('intencities')
ax1.set_ylabel('avg wait')

ax2.plot(statistics['intencities'], statistics['avg_idle'])
ax2.set_xlabel('intencities')
ax2.set_ylabel('avg idle %')

plt.show()