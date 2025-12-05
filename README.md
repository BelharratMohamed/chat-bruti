# Chat'Bruti - Nuit de l'Info 2025

Bienvenue sur le dépôt de **Chat'Bruti**, une application de chat développée dans le cadre de la **Nuit de l'Info 2025**.

## 🌙 Contexte : La Nuit de l'Info 2025

La Nuit de l'Info est une compétition nationale qui réunit étudiants, enseignants et entreprises pour un défi de programmation intense. Du coucher du soleil au lever du soleil, les équipes doivent développer une application web complète en relevant divers défis techniques et créatifs.

**Édition 2025** : Cette année, les participants s'affrontent sur un thème national NIRD tout en intégrant des fonctionnalités innovantes et décalées.

## 🤖 À propos de Chat'Bruti

Chat'Bruti n'est pas un chatbot ordinaire. Il a été conçu pour avoir une personnalité... particulière. Il est intelligent, mais il aime jouer les "abrutis". Il peut répondre à vos questions, mais attendez-vous à des réponses sarcastiques, décalées, ou faussement naïves.

### Fonctionnalités
-   **Interface Moderne** : Une UI épurée et responsive, inspirée des standards actuels (mode sombre/clair).
-   **Historique des Conversations** : Sauvegarde automatique de vos échanges pour ne jamais perdre une "perle" du bot.
-   **Personnalité Unique** : Un moteur de réponse hybride (règles + IA) pour des interactions imprévisibles.
-   **Gestion de Contexte** : Le bot se souvient (parfois) de ce que vous lui avez dit.

## 🚀 Installation et Lancement

Pour tester Chat'Bruti localement, suivez ces étapes :

### Prérequis
-   Python 3.8+
-   pip

### Étapes
1.  **Cloner le dépôt** :
    ```bash
    git clone <votre-url-repo>
    cd nuitdelinfo
    ```

2.  **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurer l'environnement** :
    Assurez-vous d'avoir une clé API OpenAI si vous utilisez les fonctionnalités avancées du cerveau (fichier `.env` ou variable d'environnement).

4.  **Lancer l'application** :
    ```bash
    python3 run.py
    ```

5.  **Accéder à l'application** :
    Ouvrez votre navigateur et allez sur `http://localhost:5001`.

## 🛠 Technologies Utilisées
-   **Backend** : Python, Flask
-   **Frontend** : HTML5, CSS3, JavaScript (Vanilla)
-   **IA** : OpenAI API (pour la génération de texte avancée)

## 🧠 Fonctionnement Technique

Chat'Bruti utilise une architecture sophistiquée pour garantir à la fois la pertinence et l'humour :

### 1. L'API Hugging Face
Nous utilisons l'API d'inférence de Hugging Face (compatible OpenAI) pour accéder à des modèles de langage performants comme `Qwen/Qwen2.5-72B-Instruct`. Cela nous permet d'avoir une intelligence de haut niveau sans gérer l'infrastructure lourde.

### 2. La Stratégie du "Double Prompting"
Pour obtenir ce ton unique "brut de décoffrage", chaque réponse est générée en deux temps :

1.  **Phase 1 : La Vérité (Factualité)**
    *   Nous demandons d'abord au modèle d'être un "assistant utile et précis".
    *   *Objectif* : Obtenir une réponse correcte et fiable à la question de l'utilisateur.

2.  **Phase 2 : La Bêtise (Personnalité)**
    *   Nous réinjectons la réponse factuelle dans un second prompt avec une instruction de style : *"Tu es Chat'Bruti... reformule la réponse... sois direct mais absurde."*
    *   *Objectif* : Transformer l'information brute en une réponse drôle, sarcastique ou décalée, tout en gardant le fond.

## 📄 Licence

Ce projet est sous licence **MIT**. Vous êtes libre de le modifier et de le distribuer.

### Crédits et Licences Tierces
-   **Flask** : BSD-3-Clause
-   **OpenAI Python Client** : Apache 2.0
-   **Paramiko** : LGPL 2.1

## 👥 L'Équipe
Développé avec ❤️ (et beaucoup de café) par l'équipe 404 Not Found !.
