from functools import wraps
def a_new_decorator(a_func):
    """Decorator outer function"""
    @wraps(a_func)
    def deepak():
        """Inner function"""
        print("I am doing some boring work before executing a_func()")

        a_func()

        print("I am doing some boring work after executing a_func()")

    return deepak

@a_new_decorator
def a_function_requiring_decoration():
    """My function"""
    print("I am the function which needs some decoration to remove my foul smell")

print(a_function_requiring_decoration.__doc__)
