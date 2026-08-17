import csv
import time

DATASET_1 = "data/dataset1_Python+P7.csv"
DATASET_2 = "data/dataset2_Python+P7.csv"

budget_max_euros = 500
facteur_echelle = 10


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


def programmation_dynamique_1d(actions, budget_max_euros, facteur_echelle):
    """Trouve la meilleure combinaison d'actions pour maximiser le profit.

    Convertit les prix au dixième d'euro pour exécuter le calcul en moins
    d'une seconde.
    """
    # Conversion du budget en unités entières
    budget_unites = int(budget_max_euros * facteur_echelle)
    n = len(actions)

    # Conversion des coûts en entiers et extraction des profits
    costs = [int(round(a["cout"] * facteur_echelle)) for a in actions]
    profits = [a["profit_euros"] for a in actions]

    # dp[w] : Meilleur profit possible pour un budget w
    dp = [0.0] * (budget_unites + 1)

    # keep[i][w] : Booléen indiquant si l'action i est retenue pour le budget w
    keep = [[False] * (budget_unites + 1) for _ in range(n)]

    # Remplissage du tableau de mémorisation
    for i in range(n):
        c = costs[i]
        p = profits[i]

        if c > budget_unites:
            continue

        # parcours inversé : élimine le risque de réutiliser la même action
        for w in range(budget_unites, c - 1, -1):
            nouveau_profit = dp[w - c] + p
            if nouveau_profit > dp[w]:
                dp[w] = nouveau_profit
                keep[i][w] = True

    # Reconstruction du portefeuille optimal (Backtracking)
    w = budget_unites
    actions_selectionees = []

    for i in range(n - 1, -1, -1):
        if keep[i][w]:
            actions_selectionees.append(actions[i])
            w -= costs[i]

    return round(dp[budget_unites], 2), actions_selectionees


def executer_analyse(chemin_fichier):
    print(f"\nAnalyse du fichier : {chemin_fichier}")

    actions = charger_actions(chemin_fichier)

    temps_debut = time.time()
    profit_total, combinaison = programmation_dynamique_1d(
        actions, budget_max_euros, facteur_echelle
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
    print("\nActions sélectionnées :")
    for action in combinaison:
        print(
            f"- {action['nom']} | Coût: {action['cout']:.2f} € | Profit:"
            f" {action['profit_euros']:.2f} €"
        )


if __name__ == "__main__":
    executer_analyse(DATASET_1)
    executer_analyse(DATASET_2)
