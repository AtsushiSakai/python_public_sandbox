from contextlib import contextmanager


@contextmanager
def context_manager_sample():
    print('enter')
    yield "yield"
    print('exit')


def main():
    with context_manager_sample() as e:
        print(f'hello context manager:{e}')


if __name__ == '__main__':
    # === Output ===
    # enter
    # hello context manager:yield
    # exit
    main()
