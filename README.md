# matchSIRET

Ce dépôt propose un code pour créer et alimenter un index Elasticsearch avec les données [base SIRENE de l'INSEE, après géolocalisation par Etalab](https://files.data.gouv.fr/geo-sirene/), ainsi que pour faire des recherches d'établissements sur cet index Elasticsearch. Le dépôt comprend aussi une liste de quelques sources de données en open data comprenant des libellés d'entreprise

Le code source a été conçu pour être compatible avec l'outil [Onyxia](https://github.com/InseeFrLab/onyxia-web) développé par l'INSEE avec le soutien d'Etalab, mais fonctionne également sans Onyxia.

## Pré-requis

Le service utilise un service Elasticsearch ([à partir de cette image](https://git.lab.sspcloud.fr/hby7ih/matchsiretimage)), Python3.10 et les bibliothèques Python indiquées dans [requirements.txt](requirements.txt). L'utilisation de JupyterLab en plus de Python est facultatif.
Les données proviennent de SIRENE et sont géolocalisées par ETALAB (https://files.data.gouv.fr/geo-sirene/last/). Elles sont [en libre accès et rafraichies chaque mois par Etalab](https://files.data.gouv.fr/geo-sirene/last/)

## Déployer matchSIRET ***avec*** Onyxia

1) Créer un service Elasticsearch [en indiquant le chemin de cette image](https://git.lab.sspcloud.fr/hby7ih/matchsiretimage) (tag:latest)
2) Créer un service JupyterLab [en indiquant le chemin du fichier d'initialisation](https://raw.githubusercontent.com/etalab/matchSIRET/main/init.sh). Des modifications du fichier d'intialisation, et notamment des chemins, peuvent être utiles selon votre version d'Onyxia.
3) Dans JupyterLab, ouvrir le fichier `indexation/indexation.ipynb`, indiquer l'url de votre service Elasticsearch (qui figure dans le "README" de votre service Elastic dans votre compte sur Onyxia) dans la cellule correspondante, et exécuter l'ensemble des cellules (ce processus prend plusieurs heures)

## Déployer matchSIRET ***sans*** Onyxia

1) Créer un service Elasticsearch [en indiquant le chemin de cette image](https://git.lab.sspcloud.fr/hby7ih/matchsiretimage) (tag:latest) avec des volumes permanents. Pour télécharger Elasticsearch et déployer une instance locale, vous pouvez suivre [la procédure de la documentation Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html)
2) Clôner ce dépôt matchSIRET, et installer les dépendances Python3.10 dans un environnement virtuel
3) Ouvrir le fichier `indexation/indexation.ipynb`, indiquer l'url de votre service Elasticsearch dans la cellule correspondante, et exécuter l'ensemble des cellules (ce processus prend plusieurs heures)

## Envoyer des requêtes à cette instance Elasticsearch

L'index Elasticsearch créé et rempli précédemment s'appuie sur un stockage permanent (qui ne disparaît pas avec la fermeture du service Elastic). On peut y effectuer des recherches avec les fonctions utilitaires du fichier `queries.py` qui s'appuient sur les structure de données `WorkSiteName` et `GeoWorkSiteName` de `worksites.py`

## Coment contribuer

Voir le [guide de contribution](CONTRIBUTING.md)

## Méthodologie 

Le but est de retrouver un établissement d'entreprise à partir d'un libellé potentiellement approximatif (qui peut correspondre au nom du groupe, au nom de l'enseigne, au nom commercial de l'établissmeent, etc.) et  d'une information géographique possiblement approximative (une adresse ou un nom de ville). D'autres champs peuvent venir fiabiliser la recherche, comme le secteur d'activité, etc. Elasticsearch permet une recherche floue ("fuzzy matching") sur les libellés, secteurs et autres champs textuels, et permet de représenter l'information géographique par un couple de coordonnées (latitude, longitude). 

_i) Construction d'un index_

L'ensemble des entrées de la base SIRENE sont géolocalisées par Etalab, puis versées dans l'index par le processus `indexation.ipynb` décrit plus haut (qui doit encore être automatisé pour un rafraichissement mensuel des données, ce qui n'est pas le cas aujourd'hui).

_ii ) Construction d'une recherche_

L'entité recherché se caractérise par un libellé (approximatif) et une adresse plus ou moins précise. Les établissements recherchés doivent être mis sous la forme `WorkSiteName` du fichier `worksites.py` , puis géocodées avec la fonction `geocode_worksites` (ce code écrit un fichier temporaire à l'emplacement d'où il est lancé ; il faut juste s'assurer qu'il a les droits d'écritures adaptés). L'établissement géolocalisé `WorkSiteName` peut ensuite être recherché avec la fonction `request_elastic` de `queries.py`
 
 _iii) Evaluation de la pertinence des résultats_
 
Pour évaluer la pertinence du moteur de recherche, vous avez besoin de données de validation pour lesquels vous disposez déjà d'une association du SIRET, du libellé et de l'adresse. Lors de la conception de ce projet, nous nous sommes appuyés sur des [données en open data](data_sources.txt), notamment une base de restaurants (non exhasutive) utilisée et publiée par la Direction Générale de l'Alimentation (DGAL).

Remarque : il peut arriver que plusoieurs établissements d'entreprise répondent aux critères de recherche (par exemple, si vous avez spécifié une ville et un nom de groupe, et que plusieurs établissements de ce groupe se trouvent dans cette ville). Il faut alors renvoyer l'ensemble de ces résultats exacts (ce cas se pose assez peu dans notre base de données des restaurants).

Si vous êtes un réutilisateur de ce code pour une mission spécifique, il peut être pertinent pour vous d'utiliser vos propres données de validation et de les utiliser pour finetuner vos poids (dans la mesure où l'efficacité opérationnelle dépend de l'équilibrage des poids de recherche)

  _iv) Finetuner le modèle__
 
 En utiliser vos propres données de finetuning comprenant déjà des SIRET, des adresses, des libellés et tous champs très présent pour votre cas d'usage, vous pouvez finetuner les poids de recherche Elasticsearch. Pour celà, il vous suffit de modifier le fichier de poids.

(Pour l'historie du projet : la méthodologie d'avant-projet est décrite sur le [wiki du programme 10%](https://github.com/etalab-ia/programme10pourcent/wiki/Ateliers-SIRETisation))

## Projets open source liés à ce dépôt

[SocialGouv](https://github.com/SocialGouv/recherche-entreprises) : recherche d'établissements d'entreprises, notamment pour des travaux sur les conventions collectives
[L'Annuaire des entreprises](https://github.com/etalab/annuaire-entreprises-search-infra) : recherche d'entreprises (à l'échelle du SIREN et non du SIRET)

## Contact

La maintenance est effectuée par Etalab, au sein de la Direction interministérielle du numérique (DINUM) française.

[lab-ia@data.gouv.fr](mailto:lab-ia@data.gouv.fr)

