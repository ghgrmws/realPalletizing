import csv
import os.path
import random


Type = {
    "1": [0, 1/2, 2/3, 1, 2/3, 1],
    "2": [2/3, 1, 0, 1/2, 2/3, 1],
    "3": [2/3, 1, 2/3, 1, 0, 1/2],
    "4": [1/2, 1, 1/2, 1, 1/2, 1],
    "5": [0, 1/2, 0, 1/2, 0, 1/2],
    "6": [0, 1, 0, 1, 0, 1],
    "7": [0, 7/8, 0, 7/8, 0, 7/8],
    "8": [0, 1, 0, 1, 0, 1],
}


class Instance_Generator:
    def __init__(self, W, H, D, N, k):
        self.Width = W
        self.Height = H
        self.Depth = D
        self.Number = N
        self.k = k

    def save_in_file(self, file_name):
        with open(file_name, "w") as f:
            f.write(str(self.Number) + "," + str(self.Width) + "," + str(self.Height) + "," + str(self.Depth) + "\n")
            for i in range(self.Number):
                f.write(self.make_a_box())

    def make_a_box(self):
        if self.k > 0:
            if random.random() < 0.5:
                tk = self.k
            else:
                tk = random.randint(1, 5)
        else:
            tk = self.k
        t = Type[str(tk)]
        w = int(random.uniform(max(1, t[0] * self.Width), t[1] * self.Width))
        h = int(random.uniform(max(1, t[2] * self.Height), t[3] * self.Height))
        d = int(random.uniform(max(1, t[4] * self.Depth), t[5] * self.Depth))
        return str(w) + "," + str(h) + "," + str(d) + "\n"


def generate_data(dirs):
    """
    This method is from http://hjemmesider.diku.dk/~pisinger/codes.html
    Here has total 8 classes with 40 instances, which 10 instances for each value of {50, 100, 150, 200}, for each
    Bin size for classes 1-5 is W=H=D=100, and size of boxes follows a uniform distribution in this table.

                Width           Height          Depth
    Type 1      [1, 1/2W]       [2/3H, H]       [2/3D, D]
    Type 2      [2/3W, W]       [1, 1/2H]       [2/3D, D]
    Type 3      [2/3W, W]       [2/3H, H]       [1, 1/2D]
    Type 4      [1/2W, W]       [1/2H, H]       [1/2D, D]
    Type 5      [1, 1/2W]       [1, 1/2H]       [1, 1/2D]

    For Class k in [1, 5], each item of type k is chosen with probability 60%, and other four types with probability 10%

    Classes 6–8 are as follows:
    Class 6:    W=H=D=10    w,h,d [1, 10]
    Class 7:    W=H=D=40    w,h,d [1, 35]
    Class 8:    W=H=D=100   w,h,d [1, 100]
    """
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    N = [50, 100, 150, 200]
    case = 0
    for i in range(1, 6):
        for n in N:
            for cur in range(10):
                inst = Instance_Generator(100, 100, 100, n, i)
                inst.save_in_file(dirs + "/" + str(case) + ".csv")
                case += 1
    """
    Class 6
    """
    for n in N:
        for cur in range(10):
            inst = Instance_Generator(10, 10, 10, n, 6)
            inst.save_in_file(dirs + "/" + str(case) + ".csv")
            case += 1
    """
    Class 7
    """
    for n in N:
        for cur in range(10):
            inst = Instance_Generator(40, 40, 40, n, 7)
            inst.save_in_file(dirs + "/" + str(case) + ".csv")
            case += 1
    """
    Class 8
    """
    for n in N:
        for cur in range(10):
            inst = Instance_Generator(100, 100, 100, n, 8)
            inst.save_in_file(dirs + "/" + str(case) + ".csv")
            case += 1


def get_data(file_path):
    with open(file_path) as f:
        reader = csv.reader(f)
        headers = next(reader)
        N = int(headers[0])
        W = int(headers[1])
        H = int(headers[2])
        D = int(headers[3])
        boxes = list()
        for r in reader:
            boxes.append(list(map(int, r)))
    return N, W, H, D, boxes

