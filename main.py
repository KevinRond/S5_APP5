import numpy as np
import matplotlib.pyplot as plt
import math
import statistics as stat
import scipy.special
import scipy.stats as stats

def get_values(file_path):
    with open(file_path, 'r') as file:
        return [float(line.strip()) for line in file]

def get_desc_stats(data):
    mean = stat.mean(data)
    median = stat.median(data)
    mode = stat.mode(data)
    std = stat.stdev(data)
    var = stat.variance(data)
    min = np.min(data)
    max = np.max(data)

    return {
        'mean': mean,
        'med': median,
        'mode': mode,
        'std': std,
        'var': var,
        'min': min,
        'max': max
    }


def display_stats_table(stats):
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create a table with the statistics data
    table_data = [[key, f"{value:.2f}"] for key, value in stats.items()]
    table = ax.table(cellText=table_data, colLabels=["Statistique descriptive", "Valeur"], cellLoc="center", loc="center")
    table.scale(1, 2)

    plt.savefig("table_stats", bbox_inches='tight', dpi=300)
    plt.show()


def display_histogram_table(bins):
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    table_data = [
        [
            bin['class'],
            f"[{bin['lower_limit']:.1f} - {bin['upper_limit']:.1f}[",
            f"{bin['centre']:.2f}",
            bin['freq'],
            f"{bin['rel_freq'] * 100:.2f}%",
            f"{bin['cumul_freq'] * 100:.2f}%"
        ]
        for bin in bins
    ]

    # Create a table with bin data
    table = ax.table(
        cellText=table_data,
        colLabels=["Classe", "Limites", "Centre", "Fréquence", "Fréquence relative", "Fréquence cumulative"],
        cellLoc="center", loc="center"
    )
    table.scale(1, 1.5)

    plt.savefig("table_histogramme", bbox_inches='tight', dpi=300)
    plt.show()

def display_adjustment_table(adjustment_data):
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    table_data = [
        [
            bin['class'],
            f"[{bin['lower_limit']:.1f} - {bin['upper_limit']:.1f}[",
            f"{bin['lower_limit_z']:.2f}",
            f"{bin['upper_limit_z']:.2f}",
            f"{bin['pi']:.2f}",
            bin['oi'],
            f"{bin['ei']:.2f}",
            f"{bin['wtf']:.2f}",
        ]
        for bin in adjustment_data
    ]

    # Create a table with bin data
    table = ax.table(
        cellText=table_data,
        colLabels=["Classe", "Limites", "Borne Gauche Z", "Borne Droite Z", "Pi", "Oi", "Ei", "(Oi-Ei)**2 / Ei"],
        cellLoc="center", loc="center"
    )
    table.scale(1, 1.5)

    plt.savefig("table_ajustement", bbox_inches='tight', dpi=300)
    plt.show()

def get_histogram_data(data):
    bin_number = int(np.sqrt(len(data)))
    min_value = np.min(data)
    max_value = np.max(data)
    interval_len = (max_value - min_value) / bin_number

    bins = []
    cumul_freq = 0

    for i in range(bin_number):
        lower_limit = min_value + interval_len*i
        upper_limit = min_value + interval_len*(i+1)
        centre = ((min_value + interval_len*i) + (min_value + interval_len*(i+1)))/2
        frequency = sum(lower_limit <= x < upper_limit for x in data)
        rel_freq = frequency / len(data)
        cumul_freq += rel_freq
        bins.append({
            'class': i+1,
            'lower_limit': lower_limit,
            'upper_limit': upper_limit,
            'centre': centre,
            'freq': frequency,
            'rel_freq': rel_freq,
            'cumul_freq': cumul_freq
        })

    return bins, interval_len



def display_histogram(binwidth, data):
    plt.hist(data, bins=np.arange(min(data), max(data) + binwidth, binwidth), edgecolor='black', alpha=0.7)
    plt.xlabel('Minutes de jeu par semaine')
    plt.ylabel('Fréquence')
    plt.title(f'Histogramme des minutes jouer par semaine')
    plt.savefig("histogramme", bbox_inches='tight', dpi=300)
    plt.show()

def calculate_confidence_interval(data):
    z = 1.96
    mean = stat.mean(data)
    std = stat.stdev(data)

    error = z * std / np.sqrt(len(data))
    lower_interval = mean - error
    upper_interval = mean + error

    return lower_interval, upper_interval

def get_adjustment_data(bins, mean, std):
    adjustement_data = []

    for bin in bins:
        lower_limit_z = (bin['lower_limit'] - mean) / std
        upper_limit_z = (bin['upper_limit'] - mean) / std
        pi = stats.norm.cdf(upper_limit_z) - stats.norm.cdf(lower_limit_z)
        oi = bin['freq']
        ei = oi * pi
        wtf_is_that = (oi - ei)**2 / ei
        adjustement_data.append({
            'class': bin['class'],
            'lower_limit': bin['lower_limit'],
            'upper_limit': bin['upper_limit'],
            'lower_limit_z': lower_limit_z,
            'upper_limit_z': upper_limit_z,
            'pi': pi,
            'oi': oi,
            'ei': ei,
            'wtf': wtf_is_that
        })

    x = 0
    for bin in adjustement_data:
        x += bin['wtf']

    other_x = 14.07

    if x > other_x:
        print(f"Les données ne proviennent pas d'une distribution normale")
    else:
        print(f"Les données proviennent d'une distribution normale")

    return adjustement_data


def mandat_2():
    values = get_values("./TempsDeJeu.txt")
    data_stats = get_desc_stats(values)
    # display_stats_table(data_stats)
    bins, interval_len = get_histogram_data(values)
    # display_histogram(interval_len, values)
    display_histogram_table(bins)
    adjustement_data = get_adjustment_data(bins, data_stats['mean'], data_stats['std'])
    display_adjustment_table(adjustement_data)
    # print(calculate_confidence_interval(values))

def mandat_3():
    N = 10_000
    arrival_rate = 5
    mean = 1/arrival_rate
    x = np.linspace(0, 5, 1000)
    P = (arrival_rate**x * np.exp(-arrival_rate * x))/scipy.special.factorial(x) # mauvaise formule

    print(math.factorial(5))

    plt.plot(x, P)
    plt.show()


if __name__ == '__main__':
    mandat_2()
    # mandat_3()
