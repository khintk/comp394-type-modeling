# -*- coding: utf-8 -*-

from .types import Type, NoSuchMethod


class Expression(object):
    """
    AST for simple Java expressions. Note that this package deal only with compile-time types;
    this class does not actually _evaluate_ expressions.
    """

    def static_type(self):
        """
        Returns the compile-time type of this expression, i.e. the most specific type that describes
        all the possible values it could take on at runtime. Subclasses must implement this method.
        """
        raise NotImplementedError(type(self).__name__ + " must implement static_type()")

    def check_types(self):
        """
        Validates the structure of this expression, checking for any logical inconsistencies in the
        child nodes and the operation this expression applies to them.
        """
        raise NotImplementedError(type(self).__name__ + " must implement check_types()")


class Variable(Expression):
    """ An expression that reads the value of a variable, e.g. `x` in the expression `x + 5`.
    """
    def __init__(self, name, declared_type):
        self.name = name                    #: The name of the variable
        self.declared_type = declared_type  #: The declared type of the variable (Type)

    def static_type(self):
        return self.declared_type

    def check_types(self):
        pass


class Literal(Expression):
    """ A literal value entered in the code, e.g. `5` in the expression `x + 5`.
    """
    def __init__(self, value, type):
        self.value = value  #: The literal value, as a string
        self.type = type    #: The type of the literal (Type)

    def static_type(self):
        return self.type

    def check_types(self):
        pass



class NullLiteral(Literal):
    def __init__(self):
        super().__init__("null", Type.null)

    def static_type(self):
        return Type.null

    def check_types(self):
        pass


class MethodCall(Expression):
    """
    A Java method invocation, i.e. `foo.bar(0, 1, 2)`.
    """
    def __init__(self, receiver, method_name, *args):
        self.receiver = receiver        #: The object whose method we are calling (Expression)
        self.method_name = method_name  #: The name of the method to call (String)
        self.args = args                #: The method arguments (list of Expressions)

    def static_type(self):
        return self.receiver.static_type().method_named(self.method_name).return_type

    def check_types(self):
        print("afasd")
        # print(self.receiver.static_type().method_named(self.method_name).argument_types)
        # print(self.args)
        listOfArguments = self.receiver.static_type().method_named(self.method_name).argument_types
        numOfMethodsParameters = len(self.receiver.static_type().method_named(self.method_name).argument_types)
        # print(listOfArguments[1] != (self.args[1].static_type()))
        listOfTypesOfParameterArguments = []
        listOfTypesOfArguments = []

        for i in range(len(self.args)):
            listOfTypesOfParameterArguments.append(listOfArguments[i].name)
            listOfTypesOfArguments.append(self.args[i].static_type().name)

        if(self.method_name not in self.receiver.static_type().methods):
            if (len(self.args) != numOfMethodsParameters):
                raise JavaTypeError(
                    "Wrong number of arguments for {0}: expected {1}, got {2}".format(
                        str(self.receiver.static_type().name) + "." + str(self.method_name) + "()",
                        numOfMethodsParameters,
                        len(self.args)))
            return self.receiver.static_type().method_named(self.method_name)

        else:
            for i in range(len(self.args)):
                # if ((listOfArguments[i].name != (self.args[i].static_type().name))):
                if("a" != "b"):
                    raise JavaTypeError(
                        "{0} expects arguments of type {1}, but got {2}".format(
                            str(self.receiver.static_type().name) + "." + str(self.method_name) + "()",
                            tuple(listOfTypesOfParameterArguments),
                            tuple(listOfTypesOfArguments)))


class ConstructorCall(Expression):
    """
    A Java object instantiation, i.e. `new Foo(0, 1, 2)`.
    """
    def __init__(self, instantiated_type, *args):
        self.instantiated_type = instantiated_type  #: The type to instantiate (Type)
        self.args = args                            #: Constructor arguments (list of Expressions)

    def static_type(self):
        return self.instantiated_type

    def check_types(self):
        pass

class JavaTypeError(Exception):
    """ Indicates a compile-time type error in an expression.
    """
    pass


def names(named_things):
    """ Helper for formatting pretty error messages
    """
    return "(" + ", ".join([e.name for e in named_things]) + ")"
