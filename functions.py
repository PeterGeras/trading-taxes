

def runtime(start, end):
    diff_time = end - start
    secs = diff_time.total_seconds()
    hrs = secs//3600
    mins = secs//60
    runtime_msg = ''

    if hrs > 0:
        runtime_msg += f'{int(hrs)}h'
    if mins > 0:
        mins -= hrs*60
        runtime_msg += f'{int(mins)}m'

    secs -= hrs*3600 + mins*60
    if hrs + mins > 0:
        runtime_msg += f'{int(secs)}s'
    else:
        runtime_msg += f'{secs:.2f}s'

    print(f'runtime: {runtime_msg}')

    return runtime_msg
