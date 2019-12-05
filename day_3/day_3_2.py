import functools 
MIN_X, MAX_X = 0, 0
MIN_Y, MAX_Y = 0, 0

class Segment:

    def __init__(self, p1, p2, steps):
        self.a = p1
        self.b = p2
        self.alignment = 'y' if self.a[0] == self.b[0] else 'x'
        self.steps = steps
        
    def crossing(self, other, selfSteps=False):
        if self.alignment == other.alignment:
            return None
        if min(other.a[1], other.b[1]) <= self.a[1] <= max(other.a[1], other.b[1]) and \
           min(self.a[0], self.b[0]) <= other.a[0] <= max(self.a[0], self.b[0]):

            cross = None
            if self.alignment == 'x':
                cross = (other.a[0], self.a[1])
            elif self.alignment == 'y':
                cross = (self.a[0], other.a[1])
            if selfSteps:
                return (cross[0], cross[1], other.steps)
            else:
                return (cross[0], cross[1], self.cross_step(cross) + other.cross_step(cross))
        return None

    def cross_step(self, crossing):
        offset = self.b[0] - crossing[0] if self.alignment == 'x' else self.b[1] - crossing[1]
        return self.steps - abs(offset) 
    
    def char_at(self, x, y):
        char = '.'
        if self.alignment == 'x' and  y == self.a[1] and min(self.a[0], self.b[0]) <= x <= max(self.b[0], self.a[0]):
            char = '-'
        elif self.alignment == 'y' and x == self.a[0] and min(self.a[1], self.b[1]) <= y <= max(self.b[1], self.a[1]) :
            char = '|'
        return char

    def blit(self, char_map, lower_bounds):
                        
        x_offset = -lower_bounds[0]
        y_offset = -lower_bounds[1]

        if self.alignment == 'x':
            y = self.a[1]
            for x in range(min(self.a[0], self.b[0]), max(self.a[0], self.b[0])):
                char_map[x + x_offset][y + y_offset] = '|'
        elif self.alignment == 'y':
            x = self.a[0]
            for y in range(min(self.a[1], self.b[1]), max(self.a[1], self.b[1])):
                char_map[x + x_offset][y + y_offset] = '-'
        char_map[self.a[0] + x_offset][self.a[1] + y_offset] = '+'
        char_map[self.b[0] + x_offset][self.b[1] + y_offset] = '+'


    def __str__(self):
        return str(self.a) + "->" + str(self.b)

def build_wire(data):
    global MAX_X, MAX_Y, MIN_X, MIN_Y

    last_pos = (0, 0)
    seg_list = []
    steps = 0
    while len(data) > 0:
        #parse data

        new_x, new_y = last_pos
        move = data.pop(0)
        dir = move[0]
        offset = int(move[1:])
        #apply change

        if dir == 'U':
            new_y = new_y + offset
        elif dir == 'D':
            new_y = new_y - offset
        elif dir == 'L':
            new_x = new_x - offset
        elif dir == 'R':
            new_x = new_x + offset
        else:
            print("UNRECOGNIZED DIRECTION")
        steps = steps + offset

        seg_list.append(Segment((last_pos[0], last_pos[1]), (new_x, new_y), steps))
        last_pos = (new_x, new_y)
        MIN_X = min(MIN_X, new_x)
        MAX_X = max(MAX_X, new_x)
        MIN_Y = min(MIN_Y, new_y)
        MAX_Y = max(MAX_Y, new_y)

    return seg_list

def taxi_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
def dist_origin(x):
    return taxi_dist((0, 0), x)

def map_wires(w0, w1):
    size_x = abs(MAX_X - MIN_X) + 2
    size_y = abs(MAX_Y - MIN_Y) + 2
    char_map = [['.' for i in range(size_x)] for i in range(size_y)]
    for seg in w0 + w1:
        seg.blit(char_map, (MIN_X, MIN_Y))
    return char_map



if __name__ == "__main__":
    data0 = "R997,D99,R514,D639,L438,D381,L251,U78,L442,D860,R271,U440,L428,U482,R526,U495,R361,D103,R610,D64,L978,U587,L426,D614,R497,D116,R252,U235,R275,D882,L480,D859,L598,D751,R588,D281,R118,U173,L619,D747,R994,U720,L182,U952,L49,D969,R34,D190,L974,U153,L821,U593,L571,U111,L134,U111,R128,D924,R189,U811,R100,D482,L708,D717,L844,U695,R277,D81,L107,U831,L77,U609,L629,D953,R491,D17,R160,U468,R519,D41,R625,D501,R106,D500,R473,D244,R471,U252,R440,U326,R710,D645,L190,D670,L624,D37,L46,D242,L513,D179,R192,D100,R637,U622,R322,U548,L192,D85,L319,D717,L254,D742,L756,D624,L291,D663,R994,U875,R237,U304,R40,D399,R407,D124,R157,D415,L405,U560,R607,U391,R409,U233,R305,U346,L233,U661,R213,D56,L558,U386,R830,D23,L75,D947,L511,D41,R927,U856,L229,D20,L717,D830,R584,U485,R536,U531,R946,U942,R207,D237,L762,U333,L979,U29,R635,D386,R267,D260,R484,U887,R568,D451,R149,U92,L379,D170,R135,U799,L617,D380,L872,U868,R48,U279,R817,U572,L728,D792,R833,U788,L940,D306,R230,D570,L137,U419,L429,D525,L730,U333,L76,D435,R885,U811,L937,D320,R152,U906,L461,U227,L118,U951,R912,D765,L638,U856,L193,D615,L347,U303,R317,U23,L139,U6,L525,U308,L624,U998,R753,D901,R556,U428,L224,U953,R804,D632,L764,U808,L487,U110,L593,D747,L659,D966,R988,U217,L657,U615,L425,D626,L194,D802,L440,U209,L28,U110,L564,D47,R698,D938,R13,U39,R703,D866,L422,D855,R535,D964,L813,D405,R116,U762,R974,U568,R934,U574,R462,D968,R331,U298,R994,U895,L204,D329,R982,D83,L301,D197,L36,U329,R144,U497,R300,D551,L74,U737,R591,U374,R815,U771,L681"
    data1 = "L997,D154,R652,U379,L739,U698,R596,D862,L125,D181,R786,U114,R536,U936,L144,U936,R52,U899,R88,D263,R122,D987,L488,U303,R142,D556,L691,D769,L717,D445,R802,U294,L468,D13,R301,D651,L242,D767,R465,D360,L144,D236,R59,U815,R598,U375,R645,U905,L714,U440,R932,D160,L420,U361,L433,D485,L276,U458,R760,D895,R999,U263,R530,U691,L918,D790,L150,U574,R800,U163,R478,U112,L353,U30,L763,U239,L353,U619,R669,D822,R688,U484,L678,D88,R946,D371,L209,D175,R771,D85,R430,U16,R610,D326,R836,U638,L387,D996,L758,U237,L476,U572,L456,U579,L457,D277,L825,U204,R277,U267,L477,D573,L659,D163,L516,D783,R762,U146,L387,U700,R911,U335,L115,D887,R677,U312,R707,U463,L743,U358,L715,D603,R966,U21,L857,D680,R182,D977,L279,U196,R355,D624,L434,U410,R385,U47,L999,D542,L453,D735,R781,U115,R814,U110,R344,D139,R899,D650,L118,D774,L227,D140,L198,D478,R115,D863,R776,D935,R473,U722,R555,U528,L912,U268,R776,D223,L302,D878,R90,U52,L595,U898,L210,U886,R161,D794,L846,U404,R323,U616,R559,U510,R116,D740,L554,U231,R54,D328,L56,U750,R347,U376,L148,U454,L577,U61,L772,D862,R293,U82,L676,D508,L53,D860,L974,U733,R266,D323,L75,U218,L390,U757,L32,D455,R34,D363,L336,D67,R222,D977,L809,D909,L501,U483,L541,U923,R97,D437,L296,D941,L652,D144,L183,U369,L629,U535,L825,D26,R916,U131,R753,U383,L653,U631,R280,U500,L516,U959,R858,D830,R357,D87,R885,D389,L838,U550,R262,D529,R34,U20,L25,D553,L884,U806,L800,D988,R499,D360,R435,U381,R920,D691,R373,U714,L797,D677,L490,D976,L734,D585,L384,D352,R54,D23,R339,D439,L939,U104,L651,D927,L152"
    # data0 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    # data1 = "U62,R66,U55,R34,D71,R55,D58,R83"
    # data0 = "R8,U5,L5,D3"
    # data1 = "U7,R6,D4,L4"
    wire0 = build_wire(data0.split(","))
    wire1 = build_wire(data1.split(","))

    crossings = []
    for seg0 in wire0:
        for seg1 in wire1:
            cross = seg0.crossing(seg1)
            if cross is not None and not (cross[0] == 0 and cross[1] == 0):
                crossings.append(cross)
    for seg0 in wire1:
        for seg1 in wire0:
            cross = seg0.crossing(seg1)
            if cross is not None and not (cross[0] == 0 and cross[1] == 0) :
                crossings.append(cross)
    while crossings[0][0] == 0 and crossings[0][1] == 0:
        del crossings[0]
    crossings.sort(key=lambda x: x[2])
    print(crossings[0][2])
    #print(crossings)
    # m = map_wires(wire0, wire1)
    # for c in crossings:
    #     m[c[0] - MIN_X][c[1] - MIN_Y] = 'x'
    # for line in m:
    #     print(functools.reduce(lambda a,b: a+b, line))
        




        
