from __future__ import absolute_import, unicode_literals
from builtins import object

from six import iteritems, with_metaclass


class EnumerationError(Exception):
    pass


class Enumeration(object):
    """
    So we can have something like enums
    """

    _names = None

    @classmethod
    def names(cls):
        """
        Returns:
            list: str[] Names of each enumerated value on class
        """
        if not cls._names:
            cls._names = [
                attr for attr in dir(cls())
                if attr.upper() == attr
                and not callable(attr)
                and not attr.startswith("_")
            ]

        return cls._names

    @classmethod
    def members(cls):
        """
        Returns:
            dict[str, object]: {name: value} of each enumerated name
        """
        return {m: getattr(cls, m) for m in cls.names()}

    @classmethod
    def values(cls):
        """
        Returns:
            list: The values of each enumerated member name
        """
        return [getattr(cls, m) for m in cls.names()]

    @classmethod
    def from_name(cls, name):
        """
        Args:
            name(str):
        Returns:
            object: The value for cls.:name
        """
        if hasattr(cls, name):
            return getattr(cls, name)

        raise EnumerationError(
            "%s has no enumerated value named %s" % (cls.__name__, name)
        )

    @classmethod
    def choices(cls):
        """
        Returns:
            list: A list of Django's quaint choices tuples
        """
        return [
            (name, value)
            for name, value in iteritems(cls.members())
        ]


def _is_name(name_str):
    """
    In the name of DRY, I factored this out in the only way I could.  Note that
    I would love to include the notion of not callable at this level, but any
    attempts to do this in a separate method that is not __getattribute__
    causes infinite recursion.

    The astute among you will notice that this function does not check
    callability like the code above in Enumeration.  That is because dir() is
    guaranteed to return strings, which are not callable, and this method
    operates on name strings, not class attributes themselves.  We could easily
    clean up the code above and remove this comment.

    Args:
        name_str (str): The name of the attribute to check
    Returns:
        bool: True if the name_str is a name, False otherwise
    """
    return (
        name_str.upper() == name_str.upper()  # case insensitive match
        and not name_str.startswith('_')  # not hidden
    )


class ModelEnumerationType(type):
    """
    Bear with me, this is pretty intense, and I'm not recommending that we
    normally do this.

    This metaclass is necessary because we need to control the class-level
    attribute access to ModelEnumeration.  So think of it like overriding the
    class' getattr, not those of each instance.

    We do this simply to uphold the idea that:

        Enum.name

    Will return back a string representation of the name, not the value that is
    assigned to it.
    """
    def __getattr__(cls, name_str):
        """
        This is the "normal" getattr, which we just delegate to the parent to
        do the normal thing.

        Args:
            name_str (str): String of name to get
        Returns:
            str: The value of the attribute with the given name
        """
        return super(ModelEnumerationType, cls).__getattribute__(name_str)

    def __getattribute__(cls, name_str):
        """
        This is the "crazy" getattr, which returns back the name_str as-is for
        name attributes only.  Otherwise it delegates off to the "normal"
        getattr by throwing an AttributeException.

        Args:
            name_str (str): String of name to get
        Returns:
            str: The value of the attribute with the given name

        """
        attr = super(ModelEnumerationType, cls).__getattribute__(name_str)

        if callable(attr):
            return attr

        if _is_name(name_str):
            return name_str
        else:
            raise AttributeError


class ModelEnumeration(with_metaclass(ModelEnumerationType, Enumeration)):
    """
    This is like an Enumeration, but it works for the Django ORM.  In
    particular, when you access:

        Enum.name

    You get back a string representation of the name, not the display value
    assigned to it.  To get that, just do:

        Enum.get_value(Enum.name)
    """
    _names = None

    @classmethod
    def names(cls):
        """
        Returns:
            list: str[] Names of each enumerated value on class
        """
        if not cls._names:
            cls._names = [
                attr for attr in dir(cls())
                if not callable(cls.__getattr__(attr)) and _is_name(attr)
            ]

        return cls._names

    @classmethod
    def get_value(cls, name_str):
        """
        Workaround for our metaclass hack to directly get the value of a name
        rather than the name itself.  Relies upon the __getattr__ implemented
        in the metaclass.

        Args:
            name_str (str): String of name to get
        Returns:
            str: The value of the attribute with the given name
        """
        return cls.__getattr__(name_str)

    @classmethod
    def members(cls):
        """
        Returns:
            dict[str, object]: {name: value} of each enumerated name
        """
        return {m: cls.get_value(m) for m in cls.names()}

    @classmethod
    def values(cls):
        """
        Returns:
            list: The values of each enumerated member name
        """
        return [cls.get_value(m) for m in cls.names()]

    @classmethod
    def from_name(cls, name):
        """
        Args:
            name(str):
        Returns:
            object: The value for cls.:name
        """
        if hasattr(cls, name):
            return cls.get_value(name)

        raise EnumerationError(
            "%s has no enumerated value named %s" % (cls.__name__, name)
        )
