import cmath
from math import sqrt

def c(n, m=0):
    return complex(round(n, 7), round(m, 7))

class ComplexCalculator:
    @staticmethod
    def assert_equation(c1, c2):
        if not ComplexCalculator.is_types_valid(c1) or not ComplexCalculator.is_types_valid(c2):
            raise TypeError("This class can be used for complex numbers only.\nFor int or float use c(n, 0)")
        
        c1 = ComplexCalculator.round_all(c1)
        c2 = ComplexCalculator.round_all(c2)
        return c1.real == c2.real and c1.imag == c2.imag

    @staticmethod
    def check_answers(n, w, answers_list):
        if type(n) != int or type(w) != complex or type(answers_list) not in (list, tuple):
            raise TypeError("Just learn how to use this method idiot") 

        ans_dict = {}
        for ans in answers_list:
            ans_dict[ans] = ComplexCalculator.assert_equation(w, ans**n)
        
        return ans_dict

    @staticmethod 
    def is_types_valid(n):
        return type(n) in ComplexCalculator.get_allowed_types()

    @staticmethod 
    def get_allowed_types():
        return (complex,)

    @staticmethod
    def round_all(complex_n, r=3):
        if not ComplexCalculator.is_types_valid(complex_n):
            raise TypeError("This class can be used for complex numbers only.\nFor int or float use c(n, 0)")
        
        real = round(complex_n.real,r)
        imag = round(complex_n.imag, r)
        return c(real, imag)

def main():
    equation = (3, c(27))
    answers = ( 
                c(3, 0),
                c(-3/2, (3 * sqrt(3))/2),
                c(-3/2, -(3 * sqrt(3))/2)
    )
    print("z**3 == 27")
    print(ComplexCalculator.check_answers(*equation, answers))
    equation = (4, c(-81))
    answers = ( 
                c(3/sqrt(2), 3/sqrt(2)),
                c(-3/sqrt(2), 3/sqrt(2)),
                c(-3/sqrt(2), -3/sqrt(2)),
                c(3/sqrt(2), -3/sqrt(2))
    )
    print("z**4 == -81")
    print(ComplexCalculator.check_answers(*equation, answers))
    

if __name__ == "__main__":
    main()