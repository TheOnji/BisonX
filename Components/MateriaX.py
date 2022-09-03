import json


def main():
    Mat = Materia()
    Mat([5, 5, 5, 5, 5, 5, 5])
    print(Mat)
    Mat([1, 2, 3, 4, 5, 6, 7])
    print(Mat)


class Materia():
    def __init__(self):
        self.Materia_value = 30
        self.null = {'Critical Hit': 0,
                    'Determination': 0,
                    'Direct Hit Rate': 0,
                    'Skill Speed': 0,
                    'Spell Speed': 0,
                    'Tenacity': 0,
                    'Piety': 0}
        self.__dict__.update(self.null)
        self.ID = 0000000

    def __call__(self, Materia_ID):
        self.ID = int("{}{}{}{}{}{}{}".format(*Materia_ID))
        for ID, stat in zip(Materia_ID, self.null.keys()):
            setattr(self, stat, ID * self.Materia_value)    

    def __repr__(self):
        print(f"Materia ID: {self.ID}")
        for key in self.null:
            print(f"{key}: {self.__dict__[key]}")
        return ''

if __name__ == '__main__':
    main()