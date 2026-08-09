from bruteforce import charger_actions, fichier_actions, bruteforce_recursif

budget_max = 500

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
