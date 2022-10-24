# Génération de questions à partir d'un texte

Ce système extrait les phrases d'un texte et génère des questions avec les réponses associées. Le texte est analysé avec l'analyseur [Stanza](https://stanfordnlp.github.io/stanza/ "Overview - Stanza") qui le découpe en phrases et produit une analyse en dépendances pour chacune (c'est un système écrit en Python). 

Ces dépendances sont ensuite transformées en structures de constituants par un programme JavaScript (exécutable via [node](https://nodejs.org/en/ "Node.js")) ce qui permet de recréer *assez fidèlement* la phrase originale à l'aide de jsRealB. Comme **jsRealB** permet de générer des questions à partir d'une structure de phrase, un programme JavaScript en `node` produit des variations de la structure de constituants originale pour créer des questions.

## Questions extraites

Une question n'est possible que si le constituant racine est un `S` ou `VP` et si on identifie une sous-structure qui correspond au patron recherché. Les questions possibles sont les suivantes, identifiées en sortie par le code entre parenthèses. Dans le cas d'un `CP`, on tente d'appliquer le processus sur les `S` ou `VP` enfants (mais il arrive assez souvent qu'ils sont incomplets car le sujet n'est pas répété)

* *what is* sujet (`WAS`) :  le premier `NP`, `N`, `Pro` ou `SP` 
* *what is* objet direct (`WAD`) : le premier `NP`, `N`, `Pro` ou `SP` dans le premier `VP` 
* *what is* objet indirect  : le premier `PP` dans le premier `VP` selon la préposition (en utilisant une *heuristique* raisonnable)
   * *when* (`WHN`)  : si la préposition correspond à une préposition de temps (e.g. *after*, *during*, ...)
   * *where* (`WHE`) : si la préposition correspond à une préposition de lieu (e.g. *above*, *in*,...)
   * *prep* *what* (`WAI`) : dans les autres cas, où *prep* est la préposition rencontrée dans le texte

## Données
Les fichiers de données et de résultats sont dans le répertoire `data` avec les extensions suivantes:

* `txt` : les textes à traiter (certains ont été révisées à la main pour enlever les erreurs évidentes: mots collés ou inversion de lettres)
* `conllu` : les analyses de dépendances produites par Stanza en format *conllu*, utilisé dans les [Universal Dependencies](http://universaldependencies.org/ "Universal Dependencies")
* `out` : les résultats du programme `questionsFromText.js` qui produit des lignes identifiées par les indicateurs suivants:
    * `id`   : identification de la phrase dans la structure de dépendances
    * `text` : phrase originale
    * `TEXT` : phrase recréée à partir des structures de dépendances
    *  type de question (voir indicateur ci-dessus) : question => réponse (plusieurs questions peuvent être produites pour une seule phrase)
    * `ERR`  : la phrase ne peut être traitée
* `tsv` : fichier de données original manipulé pour créer un `txt`

Le répertoire `old` conserve les premières données reçues, mais qui n'étaient pas très appropriées pour la technique utilisée pour générer des questions.

## Lancement du programme
    node questionsFromText fichier.txt

* vérifie que *fichier.conllu* correspondant existe et qu'il est plus récent que *fichier.txt*, sinon il lance le programme `text2ud.py ` pour le (re)créer.
* transforme la structure de dépendances en une structure de constituants
* crée les questions

## Programmes

### Création de la structure de dépendances
* `text2ud.py` : transforme le texte en structure de dépendances, en prenant pour acquis que **Stanza** a déjà été installé; les instructions d'installation sont indiquées dans les commentaires au début du programme.

### Création des questions
* `questionsFromText.js` : programme initial qui accepte deux paramètres:
    * *fichier.txt* : phrases à traiter
    * *lang* : `en` ou `fr`, toutefois `fr` n'a pas encore été bien testé


### Création de la structure de constituants
* `JSR.js`  : structure des constituants
* `UD.js`   : structure des dépendances
* `UD2jsr.js` : tables de transformation des features UD en jsRealB
* `UDnode-en.js` : traiter l'info d'un noeud de dépendance (spécifique à l'anglais)
* `UDnode-fr.js` : traiter l'info d'un noeud de dépendance (spécifique au français)
* `UDnode.js`    : traiter l'info d'un noeud de dépendance (commun aux deux langues)
* `UDregenerator-en.js` : transformation de UD en constituants (spécifique à l'anglais)
* `UDregenerator-fr.js` :  transformation de UD en constituants (spécifique au français)
* `UDregenerator.js`    : transformation de UD en constituants (commun aux deux langues)
* `utils.js` : fonctions utilitaires

### Réalisation des phrases
* `jsRealB-node.js` : source de **jsRealB**
* `lexicon-dme.json` : lexique étendu utilisé par **jsRealB**

### Autres
* `obqa.py` : programme spécifique pour traiter le fichier `ex_questions_obqa.tsv`
    * essayer en prenant toujours la réponse la plus longue : on obtient 43% !!!
    * concaténer le début du texte et la réponse, j'ai ensuite corrigé les phrases à la main
* `README.md`: ce fichier
