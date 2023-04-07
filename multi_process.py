from multiprocessing import Pool
import os, time


def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))
    return end - start



if __name__ == '__main__':
    q = list()

    print('Parent process %s.' % os.getpid())

    p = Pool()
    for i in range(15):
        q.append(p.apply_async(long_time_task, args=(i,)))
    print('Waiting for all subprocesses done...')

    p.close()
    p.join()
    print('All subprocesses done.')

    for res in q:
        print(res.get())
