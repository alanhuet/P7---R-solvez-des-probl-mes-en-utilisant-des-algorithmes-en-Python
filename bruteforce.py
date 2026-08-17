import csv

fichier_actions = "data/Liste+d'actions+-+P7+Python+-+Feuille+1.csv"
budget_max = 500


def charger_actions(fichier_actions):
    actions = []

    with open(fichier_actions, mode='r', encoding='utf-8') as fichier:
        lecteur_csv = csv.DictReader(fichier)

        for ligne in lecteur_csv:
            nom = ligne['Actions #']

            cout = float(ligne['Coût par action (en euros)'])

            pourcentage_str = ligne['Bénéfice (après 2 ans)'].replace('%', '')
            pourcentage = float(pourcentage_str)

            profit_euros = round(cout * (pourcentage / 100), 2)

            actions.append({
                'nom': nom,
                'cout': cout,
                'profit_euros': profit_euros
            })

    return actions


def bruteforce_recursif(actions, budget_max, index=0):

    # Condition d'arrêt : plus d'action à analyser ou budget épuisé
    if index >= len(actions) or budget_max <= 0:
        return 0, []

    action_courante = actions[index]

    # option 1 : On n'achète pas l'action
    profit_sans, combo_sans = bruteforce_recursif(
        actions, budget_max, index + 1
        )

    # option 2 : On achète l'action
    if action_courante["cout"] <= budget_max:
        profit_avec_reste, combo_avec = bruteforce_recursif(
            actions, budget_max - action_courante["cout"], index + 1
        )
        profit_avec = action_courante["profit_euros"] + profit_avec_reste

        if profit_avec > profit_sans:
            return profit_avec, [action_courante] + combo_avec

    return profit_sans, combo_sans


if __name__ == "__main__":
    actions = charger_actions(fichier_actions)

    profit_total, combinaison = bruteforce_recursif(actions, budget_max)

    cout_total = sum(act["cout"] for act in combinaison)

    print("\n--- MEILLEUR INVESTISSEMENT TROUVÉ ---")
    print(f"Nombre d'actions achetées : {len(combinaison)}")
    print(f"Coût total : {cout_total:.2f} € / {budget_max} €")
    print(f"Profit total après 2 ans : {profit_total:.2f} €")

    print("Actions sélectionnées :")
    for action in combinaison:
        print(
            f"- {action['nom']} | Coût: {action['cout']} € | "
            f"Profit: {action['profit_euros']} €"
            )
