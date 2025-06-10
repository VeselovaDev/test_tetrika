from typing import Callable


def strict(
    function: Callable[..., bool | int | float | str],
) -> Callable[..., bool | int | float | str]:
    """Throws TypeError if wrapped function arguments are not as annotated"""

    def wrapper(*args, **kwargs):
        # fetch arguments and their types
        arguments_with_types: dict = function.__annotations__
        arguments_with_types.pop("return", None)

        # it seems that this decorator is designed to demand strict typing;
        # that is why it will raise TypeError if any of arguments is not annotated
        if len(arguments_with_types) < (len(args) + len(kwargs)):
            raise TypeError

        # function may have a mix of args and kwargs; process all kwargs first
        for kwarg in kwargs:
            if not isinstance(kwargs[kwarg], arguments_with_types[kwarg]):
                raise TypeError
            arguments_with_types.pop(kwarg, None)

        # now only args are left in the arguments_with_types;
        # order in *args and in arguments_with_types is the same as since python 3.7 dicts are ordered

        for arg, arg_type in zip(args, arguments_with_types.values()):
            if not isinstance(arg, arg_type):
                raise TypeError

        return function(*args, **kwargs)

    return wrapper
