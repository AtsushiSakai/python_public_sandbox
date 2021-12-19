class MyContextManager:
    def __enter__(self):
        print('enter')
        return "yield"

    def __exit__(self, exc_type, exc_value, traceback):
        print('exit')


def main():
    with MyContextManager() as e:
        raise IOError
        print(f'hello context manager:{e}')


if __name__ == '__main__':
    main()
