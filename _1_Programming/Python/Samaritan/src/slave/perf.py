from psutil import net_io_counters, disk_io_counters, disk_usage, \
    virtual_memory, cpu_percent, process_iter


def total_perf():
    """
    整机性能数据记录
    :return:
    """
    return (cpu_percent(),
            virtual_memory().percent,
            disk_usage('/').percent)
    # 预留功能
    # disk_io_counters().read_count,
    # disk_io_counters().write_count,
    # net_io_counters().packets_sent,
    # net_io_counters().packets_recv))


def proc_perf(pname):
    """
    单进程性能记录
    :param pname:
    :return:
    """
    target = [p for p in process_iter(attrs=['pid', 'name']) if
              pname in p.info['name']]
    result = []
    for p in target:
        with p.oneshot():
            result.append((p.name(), p.cpu_percent(), p.memory_info()))
    return str(result)
