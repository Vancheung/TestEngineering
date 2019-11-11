from re import match
from codecs import open

from src.master import turn_datetimestr_to_timestamp

PATTERN = {
    'PROC': r'(\d+)\s*(\w+)',
    'TIME': r'top\s*-\s*(\d+):(\d+):(\d+)',
    'TOTAL_CPU': r'Cpu.*(\d+).(\d+)%us',
    'TOTAL_MEM': r'Mem:\s*(\d+)M\stotal,\s*(\d+)M\s*used'
}
DAY_PATTERN = r'.*top_(\d+).log'


class PatternMatch:
    def __init__(self, line: str, daytime, process):
        self.line = line
        self.daytime = daytime
        self.process = process

    def string_to_process(self):
        for key in PATTERN:
            if match(PATTERN.get(key), self.line):
                return key, self._process_key(key)
        return None, None

    def _process_key(self, key):
        if key == 'PROC':
            PID, USER, *_, PROC_CPU, PROC_MEM, _, COMMAND = self.line.split()
            return [PID, USER, PROC_CPU, PROC_MEM,
                    COMMAND] if COMMAND in self.process else None

        pattern = PATTERN.get(key)
        match_result = match(pattern, self.line)
        if key == 'TIME':
            hh, mm, ss = match(pattern, self.line).groups()
            return turn_datetimestr_to_timestamp(self.daytime, hh, mm, ss)

        if key == 'TOTAL_CPU':
            return float(
                '{}.{}'.format(match_result.group(1), match_result.group(2)))

        if key == 'TOTAL_MEM':
            return int(match_result.group(2)) / int(match_result.group(1)) * 100


class LinuxRecord:
    def __init__(self, db, process):
        self.db = db
        self.process = process

    def record_data(self, slave_ip, filepath):
        self.db.create_slave(slave_ip)
        daytime = match(DAY_PATTERN, filepath).group(1)

        with open(filepath, 'r+') as f:
            for line in f:
                matchobj = PatternMatch(line.strip(), daytime, self.process)
                key, value = matchobj.string_to_process()
                if key and value:
                    self.__setattr__(key, value)
                try:
                    if self.PROC:
                        self.db.insert_to_slave_proc_single(slave_ip, tuple(
                            [self.TIME] + self.PROC))
                        self.PROC = None
                    if self.TOTAL_CPU and self.TOTAL_MEM:
                        self.db.insert_to_slave_total_single(slave_ip, item=(
                            self.TIME, self.TOTAL_CPU, self.TOTAL_MEM))
                        self.TOTAL_CPU = None
                        self.TOTAL_MEM = None
                except Exception:
                    pass
