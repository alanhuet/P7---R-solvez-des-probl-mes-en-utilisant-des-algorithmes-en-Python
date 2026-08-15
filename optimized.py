import csv
import time

DATASET_1 = "data/dataset1_Python+P7.csv"
DATASET_2 = "data/dataset2_Python+P7.csv"

budget_max_euros = 500


def charger_actions(fichier_actions):
    """ Chargement du fichier csv en nettoyant les données incohérentes
    (co^ts <= 0 ou profits <= 0)"""

    actions = []

    with open(fichier_actions, mode='r', encoding='utf-8') as fichier:
        lecteur_csv = csv.DictReader(fichier)

        for ligne in lecteur_csv:
            nom = ligne['name']

            cout = float(ligne['price'])

            pourcentage_str = ligne['profit']
            pourcentage = float(pourcentage_str)

            # nettoyage des actions ayant une valeur à 0 ou un rendement à 0
            if cout > 0 and pourcentage > 0:
                profit_euros = round(cout * (pourcentage / 100), 2)

                actions.append({
                    'nom': nom,
                    'cout': cout,
                    'profit_euros': profit_euros
                })

    return actions


def programmation_dynamique(actions, budget_max_euros):

    budget_centimes = int(budget_max_euros * 100)
    n = len(actions)

    # Initialisation de laa matrice (n + 1) x ( budget_centimes + 1)
    matrice = [[0.0] * (budget_centimes + 1) for _ in range(n+1)]

    # 1. Remplissage du tablzeau
    for i in range(1, n + 1):
        action = actions[i - 1]
        cout_centimes = int(round(action['cout'] * 100))
        profit = action['profit_euros']

        for w in range(budget_centimes + 1):
            if cout_centimes <= w:
                matrice[i][w] = max(
                    matrice[i - 1][w],
                    round(profit + matrice[i - 1][w - cout_centimes], 2),
                )
            else:
                matrice[i][w] = matrice[i - 1][w]

    # 2. Backtracking pour retrouver les actions sélectionnées
    w = budget_centimes
    actions_selectionnees = []

    for i in range(n, 0, -1):
        if matrice[i][w] != matrice[i - 1][w]:
            action_achetee = actions[i - 1]
            actions_selectionnees.append(action_achetee)
            w -= int(round(action_achetee['cout'] * 100))

    profit_total = matrice[n][budget_centimes]
    return profit_total, actions_selectionnees


def executer_analyse(chemin_fichier):
    print(f"\nAnalyse du fichier : {chemin_fichier}")

    actions = charger_actions(chemin_fichier)

    temps_debut = time.time()
    profit_total, combinaison = programmation_dynamique(
        actions, budget_max_euros
        )
    temps_fin = time.time()

    duree = temps_fin - temps_debut
    cout_total = sum(action['cout'] for action in combinaison)

    print("\n--- RÉSULTATS PROGRAMME OPTIMISÉ ---")
    print(f"Nombre d'actions achetées : {len(combinaison)}")
    print(f"Coût total investissement : {cout_total:.2f} € / "
          f"{budget_max_euros} €"
          )
    print(f"Profit sur 2 ans : {profit_total:.2f} €")
    print(f"Temps de calcul : {duree:.4f} secondes")


if __name__ == "__main__":
    executer_analyse(DATASET_1)
    executer_analyse(DATASET_2)
