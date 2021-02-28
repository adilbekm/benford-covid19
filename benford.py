import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# custom colors
my_red   = (0.87, 0.12, 0.15, 1.00)
my_green = (0.22, 0.62, 0.20, 0.80)
my_blue  = (0.15, 0.47, 0.69, 0.70)


# benford frequency = math.log((1 + 1/d), 10)
bs = [
    0.301029995,
    0.176091259,
    0.124938736,
    0.096910013,
    0.079181246,
    0.066946789,
    0.057991946,
    0.051152522,
    0.045757490]


def apply_benford(ns):
    '''Given a list of integers ns, calculates frequency
    of numbers 1, 2, .., 9 in the first digit, and returns
    a list of 9 floating point numbers, [f1, f2, .. f9],
    where f1 is the frequency of 1, f2 the frequency of 2, etc.
    
    If an integer is negative, the negative sign will be ignored;
    if an integer is zero, it will be ingored.
    '''
    ns = [str(abs(n)) for n in ns if n != 0]
    cs = [0 for n in range(9)]
    t = len(ns)
    for n in ns:
        f = int(n[0])
        i = f - 1
        cs[i] += 1
    fs = [float(c) / float(t) for c in cs]
    return fs


def benford_error(ns):
    '''Given a list of integers ns, passes it to apply_benford(),
    and returns total absolute error from true benford frequencies.
    Returned value will be a floating point number.
    '''
    fs = apply_benford(ns)
    ferr = np.array(fs) - np.array(bs)
    terr = sum(abs(ferr))
    return terr


def plot_benford(ns, title=None, fname=None, path=None):
    '''Given a list of integers ns, passes it to apply_benford(),
    and creates a plot of its output.

    The plot will have a title if one is specified, and will be
    saved as PNG file with the name and location as specified by
    parameters fname and path, or as "test.png" in the current
    directory if not specified.
    '''
    fs = apply_benford(ns)
    
    fig = plt.figure()
    ax = plt.subplot()
    if title:
        ax.set_title(title)
    
    labels = [str(n) for n in range(1, 10)]
    x = np.arange(len(labels))
    
    # error from benford
    ferr = np.array(fs) - np.array(bs)
    yerr = np.zeros((2, 9))
    terr = 0 # total error
    for j, e in enumerate(ferr):
        i = 1
        if e < 0:
            i = 0
            e = abs(e)
        yerr[i][j] = e
        terr += e

    label1 = 'Actual data'
    label2 = 'Benford\'s Law' 

    ax.bar(x, fs, width=0.6, color=my_blue, label=label1)
    ax.errorbar(x, bs, yerr=yerr, fmt='-o', elinewidth=2, ls='--',
            color=my_red, label=label2)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Frequency')
    ax.set_xlabel('First Digit')
    ax.legend(loc=1) # 1 = upper right

    # show total error below legend
    terr_text = 'Total Error: {:.2f}'.format(terr)
    ax.text(0.98, 0.78, terr_text, transform=ax.transAxes,
            ha='right', fontsize=12, color=my_red)
    
    if fname is None:
        fname = 'test.png'
    if path:
        if path[-1] != '/':
            path = path + '/'
        fname = path + fname
    
    fig.savefig(fname)
    plt.close()
    return


def plot_benford_world(df, loc_prov, path=None):
    '''Given dataframe df (see world.py for details about its structure),
    and a list of country-province tuples loc_prov, applies Benford's law
    and creates a plot with plot_benford() for each location-province.
    '''
    for lp in loc_prov:

        l = str(lp[0])
        p = str(lp[1])

        if p == 'nan': # no province
            df1 = df[(df.location == l) & (df.province.isna())]
        else:
            df1 = df[(df.location == l) & (df.province == p)]

        n = list(df1.cases_inc)
        n = [k for k in n if k > 0]
        n_len = len(n)

        if n_len == 0:
            continue

        min_date = df1.file_date.min()
        max_date = df1.file_date.max()

        if p == 'nan':
            lp_full = l
        else:
            lp_full = l + '_' + p
        lp_safe = lp_full.replace(' ', '_')
        title = 'Covid-19 Daily Cases: {}\n{} numbers from {} to {}'
        title = title.format(lp_safe, n_len, min_date, max_date)
        fname ='{}.png'.format(lp_safe.lower())
        
        if path is None:
            path = 'world_output'

        plot_benford(n, title, fname, path)


if __name__ == '__main__':
    # run a quick test
    ns = [4128, 4568, 3833, 2786, 3084, 4674, 4172, 5547, 5495, 12079, 2926, 
    3776, 4899, 6168, 6959, 6490, 5587, 3978, 4633, 6096, 7181, 7436, 7187,
    6415, 9860, 6811, 7986, 8914, 9853, 5098, 6851, 5936, 8833, 11581, 10028,
    10398, 6952, 5285, 5187, 6487, 18892, 6715, 8551, 3563, 3888, 2898, 19419, 
    5609, 5255, 4479, 6900, 6164, 8444, 5786, 5273, 5236, 4770, 6819, 6153, 
    7540, 5556, 6495, 4670, 4372, 6438, 6018, 5303, 5637, 4199, 2883, 2734, 
    3820, 3444, 8008, 4212, 3100, 2419, 4514, 3415, 3688, 4296, 3367, 3288, 
    1972, 3117, 3885, 1779, 2893, 3119, 2582, 1521, 2094, 2676, 2908, 2859, 
    2425, 2349, 1336, 2057, 2805, 2809, 2885, 2253, 2141, 1643, 1807, 2584, 
    2716, 2400, 1842, 1578, 1144, 2303, 2102, 2684, 2532, 1926, 1734, 1276, 
    1719, 2321, 2034, 2428, 1711, 1504, 2258, 610, 2202, 1775, 2277, 1495, 889, 
    868, 1290, 1759, 6142, 1688, 952, 1168, 800, 1333, 1229, 1443, 1552, 1137, 
    1106, 845, 1196, 1454, 1532, 1222, 897, 716, 1018, 1086, 1561, 2045, 1656, 
    1129, 2111, 1186, 1051, 2585, 1415, 2091, 1244, 1345, 1283, 1472, 1729, 2008, 
    1972, 1153, 1263, 564, 1246, 1536, 1346, 1763, 1166, 1051, 626, 1452, 1954, 
    1545, 1979, 1127, 1629, 1313, 1341, 1730, 1954, 2344, 1763, 1749, 1625, 1621, 
    2097, 2102, 1892, 2140, 1815, 1268, 1820, 2481, 2051, 2160, 1782, 1956, 1827, 
    1908, 2462, 1982, 2039, 1435, 1346, 1546, 1329, 1413, 2099, 1629, 1843, 1186, 
    1342, 1605, 1719, 1635, 1009, 1721, 848, 804, 1412, 1549, 1652, 1333, 1002, 
    751, 983, 1443, 1427, 1768, 1310, 1011, 676, 938, 921, 1370, 1289, 1189, 888, 
    626, 674, 916, 1185, 1076, 784, 488, 176, 742, 497, 1107, 758, 738, 422, 677, 
    511, 530, 853, 622, 691, 470, 301, 281, 404, 492, 471, 639, 502, 408, 184, 
    155, 586, 414, 561, 380, 426, 312, 207, 571, 444, 388, 269, 187, 271, 353, 
    281, 394, 342, 99, 208, 296, 208, 404, 257, 225, 205, 351, 285, 183, 309, 236, 
    273, 86, 191, 267, 105, 172, 127, 132, 106, 101, 42, 71, 47, 40, 34, 23, 7, 
    1, 9, 8, 3, 5, 5, 1]
    plot_benford(ns, title='Test Plot')
    print('Test plot created: test.png')


