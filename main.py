import numpy as np
import matplotlib.pyplot as plt
import math
import statistics as stat

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
        'Moyenne': mean,
        'Médiane': median,
        'Mode': mode,
        'Écart-type': std,
        'Variance': var,
        'Minimum': min,
        'Maximum': max
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
            bin['limits'],
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
        colLabels=["Classe", "Limite", "Centre", "Fréquence", "Fréquence relative", "Fréquence cumulative"],
        cellLoc="center", loc="center"
    )
    table.scale(1, 1.5)

    plt.savefig("table_histogramme", bbox_inches='tight', dpi=300)
    plt.show()

def get_histogram_data(data):
    bin_number = int(np.sqrt(len(data)))
    min_value = np.min(data)
    max_value = np.max(data)
    interval_len = (max_value - min_value) / bin_number
    interval_len = math.ceil(interval_len)

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
            'limits': f'{lower_limit} - {upper_limit}',
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


if __name__ == '__main__':
    values = get_values("./TempsDeJeu.txt")
    stats = get_desc_stats(values)
    display_stats_table(stats)
    bins, interval_len = get_histogram_data(values)
    display_histogram(interval_len, values)
    display_histogram_table(bins)
