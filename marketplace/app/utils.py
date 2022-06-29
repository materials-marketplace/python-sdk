"""This moduke contains utilities.

.. currentmodule:: marketplace.app.utils
.. moduleauthor:: Pablo de Andres, Pranjali Singh (Fraunhofer IWM)
"""

import re
import functools


def check_capability_availability(capability=None):
    """Decorator for checking that a certain app supports a given capability.

    Args:
        capability (str): capability that should be in capabilities
    """
    def decorator_check(func):
        @functools.wraps(func)
        def wrapper(instance, *args, **kwargs):
            if not capability:
                capability = func.__name__
                
            if capability not in instance.capabilities:
                raise NotImplementedError("The app does not support this capability.")
            return func(instance, *args, **kwargs)

        return wrapper
    return decorator_check


def camel_to_snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
