from typing import Callable


def strict(
    function: Callable[..., bool | int | float | str],
) -> Callable[..., bool | int | float | str]:
    """Checks wrapped function arguments against their type hints"""

    def wrapper(*args, **kwargs):
        arguments_with_types = function.__annotations__
        arguments_with_types.pop(
            "return", None
        )  # dunder also exposes return of function; remove it

        # throws error if any argument is not annotated
        if len(arguments_with_types) < (len(args) + len(kwargs)):
            raise TypeError

        for kwarg in kwargs:
            if not isinstance(kwargs[kwarg], arguments_with_types[kwarg]):
                raise TypeError
            arguments_with_types.pop(kwarg, None)

        for arg, arg_type in zip(args, arguments_with_types.values()):
            if not isinstance(arg, arg_type):
                raise TypeError

        return function(*args, **kwargs)

    return wrapper
