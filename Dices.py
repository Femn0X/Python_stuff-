import secrets
import time as t

def secure_dice(sides):
    return secrets.randbelow(sides) + 1

def ex_dice(sides, buffer=1):
    """
    Generates a random number between 1 and 'sides' (inclusive)
    with a buffer to prevent returning the same number within a certain history.

    Args:
        sides (int): The number of sides on the die.
        buffer (int): The buffer size:
            - 0: Acts like secure_dice (no restriction).
            - 1: Cannot return the same number twice in a row (n != current).
            - 2: Cannot return the same number within the last 2 rolls (not n, k, n).
            - 3: Cannot return the same number within the last 3 rolls (not n, k, j, n).
            - ... and so on.
    """
    if buffer <= 0:
        return secure_dice(sides)

    if not hasattr(ex_dice, 'history'):
        ex_dice.history = []
    if sides < buffer:
      raise ValueError(f"Buffer size ({buffer}) cannot be greater than the number of sides ({sides}).")

    while True:
        roll = secrets.randbelow(sides) + 1
        if roll not in ex_dice.history[-buffer:]:
            ex_dice.history.append(roll)
            return roll

while True:
    print(f"Secure Dice (1-100): {secure_dice(100)}")
    print(f"Exclusive Dice (buffer=0, 1-10): {ex_dice(10, buffer=0)}")
    print(f"Exclusive Dice (buffer=1, 1-10): {ex_dice(10, buffer=1)}")
    print(f"Exclusive Dice (buffer=2, 1-10): {ex_dice(10, buffer=2)}")
    print(f"Exclusive Dice (buffer=3, 1-10): {ex_dice(10, buffer=3)}")
    try:
        print(f"Exclusive Dice (buffer=4, 1-10): {ex_dice(10, buffer=4)}")
    except ValueError as e:
        print(f"Exclusive Dice (buffer=4, 1-10): Error - {e}")
    # Example of how to use it with a specific buffer value:
    # buffer_value = 4
    # print(f"Exclusive Dice (buffer={buffer_value}, 1-10): {ex_dice(10, buffer=buffer_value)}")
    t.sleep(1)
