rows = 5
cols = 5

def test_function():
    for row in range(rows):
        for item in range(cols):
            target = (100 + item * 100, 100 + item * 70)
            print(target)


test_function()