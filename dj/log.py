
import os
import sys

from logbook import Logger, Processor, StreamHandler
from logbook import DEBUG, INFO, WARNING, ERROR


class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_log_color(level):
    color_by_level = {
        DEBUG: color.ENDC,
        INFO: color.OKGREEN,
        WARNING: color.WARNING,
        ERROR: color.FAIL,
    }
    return color_by_level[level]


def get_log_code(level):
    code = {
        'debug': DEBUG,
        'info': INFO,
        'warn': WARNING,
        'warning': WARNING,
        'error': ERROR,
    }
    return code[level]


formatter = {
    'screen': '' .join([
        '{record.extra[level_color]}',
        '{record.message}',
        '{record.extra[clear_color]}',
    ]),
    'screen_detail': ''.join([
        '{record.time:%Y-%m-%d %H:%M:%S}',
        ' ',
        '[',
        '{record.extra[level_color]}',
        '{record.level_name:<7}',
        '{record.extra[clear_color]}',
        ']',
        ' ',
        '({record.extra[basename]} --- {record.func_name}():{record.lineno})',
        ' : ',
        '{record.extra[level_color]}',
        '{record.message}',
        '{record.extra[clear_color]}',
    ]),
    'file': ''.join([
        '{record.time:%Y-%m-%d %H:%M:%S}',
        ' ',
        '[{record.level_name:<7}]',
        ' ',
        '({record.extra[basename]} --- {record.func_name}():{record.lineno})',
        ' : ',
        '{record.message}',
    ]),
}


def inject_extra(record):
    record.extra['basename'] = os.path.basename(record.filename)
    record.extra['level_color'] = get_log_color(record.level)
    record.extra['clear_color'] = color.ENDC


logger = Logger('root')

# extra info
processor = Processor(inject_extra)
processor.push_application()

# for screen log
screen_level = DEBUG
stream_handler = StreamHandler(sys.stdout, level=screen_level, bubble=True)
stream_handler.format_string = formatter['screen_detail']
stream_handler.push_application()


def set_level(level):
    level_list = ['debug', 'info', 'warning', 'error', 'warn']
    if level not in level_list:
        level_list.remove('warn')
        logger.error("LogLevelError: '{}'. Select in {}".format(
            level,
            level_list
        ))
        return
    code = get_log_code(level)
    stream_handler.level = code
    print(color.white('Changed log level to {}'.format(level)))


def set_mode(mode):
    mode_list = ['debug', 'normal']
    if mode not in mode_list:
        logger.error('ModeError: {}. Select in {}'.format(mode, mode_list))
        return
    if mode == 'debug':
        stream_handler.format_string = formatter['screen_detail']
        set_level('debug')
    if mode == 'normal':
        stream_handler.format_string = formatter['screen']
        set_level('info')
