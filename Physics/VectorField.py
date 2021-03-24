import sympy as sp
from Physics.Vector import Vector
class VectorField:
    def __init__(self, function_label, component_equation_texts):
        self.function_label = function_label
        self.components = []
        for component_equation_text in component_equation_texts:
            self.components.append(sp.parse_expr(component_equation_text))

    def solve(self, *args):
        new_components = self.components.copy()
        for substitution in args:
            var, value = substitution.split("=")
            for i in range(len(new_components)):
                try:
                    new_components[i] = new_components[i].subs(var, value)
                except:
                    raise Exception
        valid = True
        for component in new_components:
            if(not isinstance(component,sp.core.numbers.Integer) and not isinstance(component,sp.core.numbers.Float)):
                valid = False
        if(valid):
            for i in range(len(new_components)):
                if(isinstance(new_components[i], sp.core.numbers.Integer)):
                    new_components[i] = int(new_components[i])
                elif(isinstance(new_components[i], sp.core.numbers.Float)):
                    new_components[i] = float(new_components[i])
            return Vector(len(self.components),new_components)
        else:
            #CHANGE THIS FUNCTION LABEL TO FIT NEW VARIABLES
            new_text_components = []
            for component in new_components:
                new_text_components.append(str(component))
            return VectorField(self.function_label, new_text_components)

    def __str__(self):
        text = self.function_label + " = <"

        for component in self.components:
            text = text + str(component) + ","

        text = text[0 : len(text)-1]
        text = text + ">"

        return text
