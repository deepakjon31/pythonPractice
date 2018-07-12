import cProfile
import os
import pstats

def actual_profileit(func):
    def wrapper(*args, **kwargs):
        method = func.__name__
        prof = cProfile.Profile()
        retval = prof.runcall(func, *args, **kwargs)
        stat_fname = '{}.stat'.format(method)
        prof.dump_stats(method)
        print_profiler(method, stat_fname)
        print('dump stat in {}'.format(stat_fname))
        os.remove(method)
        return retval
    return wrapper

def print_profiler(profile_input_fname, profile_output_fname, sort_field='cumtime'):
    with open(profile_output_fname, 'w') as f:
        stats = pstats.Stats(profile_input_fname, stream=f)
        stats.sort_stats(sort_field)
        stats.print_stats()