from state_machine import State, Event, acts_as_state_machine, after, before,InvalidStateTransition

# 使用state_machine 模块创建状态机
@acts_as_state_machine
class Process:
    # 定义状态 （状态图中节点的映射）
    created = State(initial=True) # 需要指定初始状态
    waiting = State()
    running = State()
    terminated = State()
    blocked = State()
    swapped_out_waiting = State()
    swapped_out_blocked = State()

    # 定义状态转换（Event）
    # from_states 单个状态或元组
    wait = Event(from_states=(created, running, blocked,
                              swapped_out_waiting), to_state=waiting)
    run = Event(from_states=waiting, to_state=running)
    terminate = Event(from_states=running, to_state=terminated)
    block = Event(from_states=(running, swapped_out_blocked),
                  to_state=blocked)
    swap_wait = Event(from_states=waiting, to_state=swapped_out_waiting)
    swap_block = Event(from_states=blocked, to_state=swapped_out_blocked)

    # 进程名称
    def __init__(self, name):
        self.name = name
        # 可以补充ID、优先级、状态等信息

    # @after在状态转换后执行动作
    @after('wait')
    def wait_info(self):
        print('{} entered waiting mode'.format(self.name))

    @after('run')
    def run_info(self):
        print('{} is running'.format(self.name))

    # @before在状态转换前执行动作
    @before('terminate')
    def terminate_info(self):
        print('{} terminated'.format(self.name))

    @after('block')
    def block_info(self):
        print('{} is blocked'.format(self.name))

    @after('swap_wait')
    def swap_wait_info(self):
        print('{} is swapped out and waiting'.format(self.name))

    @after('swap_block')
    def swap_block_info(self):
        print('{} is swapped out and blocked'.format(self.name))

# process：Process（）类的实例
# event：Event类的实例
# event_name: 事件名称
def transition(process, event, event_name):
    try:
        event()
    except InvalidStateTransition as err:
        # 执行错误时打印事件名称
        print('Error: transition of {} from {} to {} failed'.format(process.name,process.current_state, event_name))

# 进程当前状态
def state_info(process):
    print('state of {}: {}'.format(process.name, process.current_state))


def main():
    # event_name 参数值常量
    RUNNING = 'running'
    WAITING = 'waiting'
    BLOCKED = 'blocked'
    TERMINATED = 'terminated'

    p1, p2 = Process('process1'), Process('process2')
    [state_info(p) for p in (p1, p2)] # created
    print()

    transition(p1, p1.wait, WAITING) # created->wait可行
    transition(p2, p2.terminate, TERMINATED) # terminated只接受 running->terminated
    [state_info(p) for p in (p1, p2)]
    print()

    transition(p1, p1.run, RUNNING) # waiting->running
    transition(p2, p2.wait, WAITING) # created->waiting
    [state_info(p) for p in (p1, p2)]
    print()

    transition(p2, p2.run, RUNNING) # waiting->running
    [state_info(p) for p in (p1, p2)]
    print()

    [transition(p, p.block, BLOCKED) for p in (p1, p2)] # running->blocked
    [state_info(p) for p in (p1, p2)]
    print()

    [transition(p, p.terminate, TERMINATED) for p in (p1, p2)] # terminated只接受 running->terminated
    [state_info(p) for p in (p1, p2)]
    print()

    [transition(p, p.wait, WAITING) for p in (p1, p2)]
    [state_info(p) for p in (p1, p2)]
    print()

    [transition(p, p.run, RUNNING) for p in (p1, p2)]  
    [state_info(p) for p in (p1, p2)]
    print()

    [transition(p, p.terminate, TERMINATED) for p in (p1, p2)]  # terminated只接受 running->terminated
    [state_info(p) for p in (p1, p2)]
    print()

if __name__ == '__main__':
    main()
