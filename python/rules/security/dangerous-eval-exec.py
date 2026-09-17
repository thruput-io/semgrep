import ast

def run_code(user_input):
    # ruleid: python-dangerous-eval-exec
    res1 = eval(user_input)

    # ruleid: python-dangerous-eval-exec
    exec(user_input)

    # ok: python-dangerous-eval-exec
    res2 = eval("1 + 1")

    # ok: python-dangerous-eval-exec
    res3 = ast.literal_eval(user_input)

    return res1, res2, res3
