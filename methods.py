import collections
import csv
import os.path
import random
from queue import PriorityQueue


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


def cutting_generator(W, H, D, extra_rate, lower_bound):
    # 10 - 60 cm
    box = collections.namedtuple('box', ['v', 'w', 'h', 'd'])
    q = PriorityQueue()
    q.put(box(v=-W*H*D, w=W, h=H, d=D))
    bs = list()
    while not q.empty():
        print(q.qsize())

        ws = list()
        hs = list()
        ds = list()

        space = q.get()
        if space.w >= lower_bound * 2:
            mid_w = random.randint(lower_bound, space.w)
            ws.append(mid_w)
            ws.append(space.w - mid_w)
        else:
            ws.append(space.w)

        if space.h >= lower_bound * 2:
            mid_h = random.randint(lower_bound, space.h)
            hs.append(mid_h)
            hs.append(space.h - mid_h)
        else:
            hs.append(space.h)

        if space.d >= lower_bound * 2:
            mid_d = random.randint(lower_bound, space.d)
            ds.append(mid_d)
            ds.append(space.d - mid_d)
        else:
            ds.append(space.d)

        if len(ws) == 1 and len(hs) == 1 and len(ds) == 1:
            bs.append((ws[0], hs[0], ds[0]))
        else:
            for i in ws:
                for j in hs:
                    for k in ds:
                        q.put(box(v=-i * j * k, w=i, h=j, d=k))

    count = len(bs)
    for i in range(int(count * extra_rate)):
        w = random.randint(lower_bound, W)
        h = random.randint(lower_bound, H)
        d = random.randint(lower_bound, D)
        bs.insert(0, (w, h, d))
    return bs


def generate_cutting_data(file_path, W, H, D, extra_rate, lower_bound):
    boxes = cutting_generator(W, H, D, extra_rate, lower_bound)
    with open(file_path, 'a') as f:
        N = len(boxes)
        f.write('%i,%i,%i,%i\n' % (N, W, H, D))
        for b in boxes:
            f.write('%i,%i,%i\n' % (b[0], b[1], b[2]))
    return
