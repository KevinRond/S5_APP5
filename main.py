import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.special
import statistics as stat
from scipy.optimize import root_scalar
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

    labels = ["Moyenne", "Médiane", "Mode", "Écart-type", "Variance", "Minimum", "Maximum"]
    values = [
        stats['mean'],
        stats['med'],
        stats['mode'],
        stats['std'],
        stats['var'],
        stats['min'],
        stats['max']
    ]

    # Create a table with the custom labels and values
    table_data = [[label, f"{value:.2f}"] for label, value in zip(labels, values)]
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
            f"{bin['lower_limit_z']:.3f}",
            f"{bin['upper_limit_z']:.3f}",
            f"{bin['pi']:.3f}",
            bin['oi'],
            f"{bin['ei']:.3f}",
            f"{bin['wtf']:.3f}",
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
    interval_len = ((max_value - min_value) / bin_number) + 0.1

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
    n = 100
    adjustement_data = []

    for bin in bins:
        lower_limit_z = (bin['lower_limit'] - mean) / std
        upper_limit_z = (bin['upper_limit'] - mean) / std
        pi = stats.norm.cdf(upper_limit_z) - stats.norm.cdf(lower_limit_z)
        oi = bin['freq']
        ei = pi * n
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

    khi_deux = 0
    for bin in adjustement_data:
        khi_deux += bin['wtf']

    khi_critique = 14.07
    print(f"khi deux calculé: {khi_deux}")
    if khi_deux > khi_critique:
        print(f"Les données ne proviennent pas d'une distribution normale")
    else:
        print(f"Les données proviennent d'une distribution normale")

    return adjustement_data



def mandat_2():
    values = get_values("./TempsDeJeu.txt")
    data_stats = get_desc_stats(values)
    display_stats_table(data_stats)
    bins, interval_len = get_histogram_data(values)
    display_histogram(interval_len, values)
    display_histogram_table(bins)
    adjustement_data = get_adjustment_data(bins, data_stats['mean'], data_stats['std'])
    display_adjustment_table(adjustement_data)
    print(f"Valeurs de l'intervalle de confiance: {calculate_confidence_interval(values)}")

def F(x):
    if x >= 0:
        return 0.5 * (1 + np.sqrt(1 - np.exp(-1*x**2 * np.sqrt(np.pi/8))))
    else:
        return 1 - F(abs(x))


def inverse_F(u):
    # Fonction racine pour root_scalar
    def func(x):
        return F(x) - u

    # Résolution numérique de la fonction racine
    if u < 0.5:
        sol = root_scalar(func, bracket=[-10, 0], method='bisect')
    else:
        sol = root_scalar(func, bracket=[0, 10], method='bisect')

    return sol.root

def mandat_3():
    lambda_values = [10, 50, 100]
    values = get_values("./TempsDeJeu.txt")
    mean = stat.mean(values)
    std = stat.stdev(values)
    P = np.random.exponential(10, 10_000)
    Q = std * np.random.randn(10_000) + mean

    # Transformation inverse pour P (distribution exponentielle)
    U = np.random.uniform(0, 1, 10_000)

    # Transformation pour Q (distribution normale)
    Q_inv = np.array([inverse_F(u) for u in U]) * std + mean

    plt.hist(Q_inv, bins=100, alpha=0.7, edgecolor='black')
    plt.title('Distribution des valeurs de Q')
    plt.xlabel('Temps total joué par un joueur (min)')
    plt.ylabel('Fréquence')
    plt.savefig("courbe_normale", bbox_inches='tight', dpi=300)
    plt.show()

    for lam in lambda_values:

        P_inv = -np.log(1 - U) / lam

        plt.figure(figsize=(12, 12))
        plt.subplot(2, 1, 1)
        plt.hist(P_inv, bins=100, alpha=0.7, edgecolor='black')
        plt.title(f'Distribution des valeurs de P (λ = {lam})')
        plt.xlabel('Temps entre chaque arrivé (min)')
        plt.ylabel('Fréquence')

        # Calculate cumulative arrival times
        arrival_times = np.cumsum(P_inv)  # Each element is a cumulative arrival time

        # Calculate departure times
        departure_times = arrival_times + Q_inv  # Each element is the time when a player stops playing

        # Create a time array from 0 to 1000 (or however long you want to observe)
        t = np.arange(0, np.max(departure_times))

        # Count active players at each time t
        active_player_counts = []
        for current_time in t:
            # Count players who have joined but not yet left by current_time
            active_players = np.sum((arrival_times <= current_time) & (departure_times > current_time))
            active_player_counts.append(active_players)

        print(f"Nombre de joueurs actifs en moyenne: {stat.mean(active_player_counts)}")

        # Plot the number of active players over time
        plt.subplot(2, 1, 2)
        plt.plot(t, active_player_counts, color='blue')
        plt.title(f'Nombre de joueurs actifs (λ = {lam})')
        plt.xlabel('Temps (min)')
        plt.ylabel('Nombre de joueurs actifs')
        plt.savefig(f"lambda_{lam}", bbox_inches='tight', dpi=300)
        plt.show()





if __name__ == '__main__':
    # mandat_2()
    mandat_3()
