from random import randint


def colored_text():
    print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(255, 100, 150, "example text in pink"))
    print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(255, 255, 100, "example text in yellow"))
    print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(randint(0, 255), randint(0, 255), randint(0, 255),
                                                                "example text in any random color"))


def fstrings():
    variable_to_debug = 'example value'
    print(f"print variable name and value easily: {variable_to_debug=}")

    float_variable = 0.123456789
    print(f"customise number of decimals: {float_variable:0.3f}")

    text_variable = 'a random text'
    print(f"Fill right space with # to fix length at 20: {text_variable:#<20}")
    print(f"Fill left space with _ to fix length at 20: {text_variable:_>20}")
    print(f"Fill left and right with * to fix length at 20: {text_variable:*^20}")


if __name__ == "__main__":
    colored_text()
    fstrings()
