from src.configs import VERBOSITY


# https://www.codegrepper.com/code-examples/python/python+print+error+in+red
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def log(*args, verbosity=1, rgb=(255, 255, 255)):
    if verbosity <= VERBOSITY:
        colored_args = tuple([colored(*rgb, arg) for arg in args])
        print(*colored_args)


if __name__=="__main__":
    log('lsajfalsjf')
    log('lsajfalsjf', rgb=(255, 0, 0))
    log('lsajfalsjf', rgb=(0, 255, 0))
    log('lsajfalsjf', rgb=(0, 0, 255))
    log('lsajfalsjf', rgb=(0, 0, 0))

