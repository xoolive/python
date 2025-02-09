---
permalink: /altair/
title: Chapitre 10
back: /python/contents
---

## 10. La visualisation interactive avec Altair et ipyleaflet

La place croissante que prend Jupyter dans l'écosystème Python et des
technologies du web fait la part belle à des outils de visualisation
interactive. Nous présentons ici deux de ces bibliothèques:

- la grammaire de visualisation (_grammar of graphics_)
  **Altair** complète la bibliothèque Matplotlib, avec une
  syntaxe plus naturelle, qui traite séparément les données de la
  spécification de la visualisation. Elle est basée sur les
  bibliothèques Javascript d3js et Vega, couramment utilisées par les
  journalistes qui produisent des infographies;

- la bibliothèque **ipyleaflet** propose quant à elle d'enrichir
  des fenêtres interactives de visualisation de cartes, sur le modèle
  de Google Maps ou OpenStreetMap, avec des données géographiques.

À l'instar de Pandas, une présentation complète d'Altair en quelques
pages relève de la gageure. Elle ne remplace pas la riche documentation
de la bibliothèque accessible sur le site <https://altair-viz.org>. Ce
chapitre propose une simple introduction des possibilités de cette
bibliothèque, basée sur un jeu de données[^1] rendu célèbre par le
chercheur suédois Hans Rosling[^2]. Ce fichier comprend, par année et
par pays, des données de population, d'espérance de vie et de PIB par
habitant (rapportées en équivalent en dollars de 2011).

Altair est une grammaire graphique, c'est-à-dire un langage qui décrit
une visualisation de données avant de l'appliquer à un jeu de données
particulier. Elle est construite autour de la bibliothèque Pandas, prend
en paramètre des `pd.DataFrame` et produit, à l'aide des bibliothèques
Javascript Vega Lite et D3.js, une visualisation de données sur le web.
Elle peut également prendre en paramètre des URL vers des données
ordonnées au format JSON, accessibles sur le Net.

Le point de départ de la bibliothèque sera alors un jeu de données
caractérisé par le mot-clé anglais _tidy_ (rangé): cela signifie que les
données brutes ont déjà été prétraitées, filtrées, ordonnées pour
produire des points qui s'approchent au plus près de la définition de la
visualisation. On manipulera alors:

- un `pd.DataFrame` qui sera intégré automatiquement à la
  visualisation, et où les types de données seront inférés;
- le chemin (URL) vers un fichier CSV ou JSON lu directement par la
  bibliothèque Javascript responsable du rendu.

Il convient de garder en mémoire les limitations classiques actuelles
des moteurs de rendus Javascript: à l'heure actuelle (2021), il faudra
certainement se limiter à des visualisations qui manipulent un ordre de
grandeur de 100 000 points.

Le fichier fourni sur la page web précédente comprend quelques
incohérences, des valeurs manquantes (on reconstruit notamment la
colonne `continent`), et on ne s'intéressera qu'aux points situés entre
1950 et 2015, avec des valeurs présentes de population: le code Pandas
qui construit les données utilisées pour les visualisations de cette
page est fourni ci-dessous:

```python
data = pd.read_csv(
    "life-expectancy-vs-gdp-per-capita.csv",
    header=1,
    names=[
        "country", "country_code", "year", "population", "continent",
        "life_expectancy", "GDP_per_capita"
    ],
    parse_dates=["year"],
)
continents = data.query("continent == continent").groupby("country").agg({"continent": "max"})
data = (
    data.drop(columns="continent")
    .merge(continents.reset_index(), on="country")
    .query("'1950' <= year <= '2015' and population == population")
)

data.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }

</style>
<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>country</th>
      <th>country_code</th>
      <th>year</th>
      <th>population</th>
      <th>life_expectancy</th>
      <th>GDP_per_capita</th>
      <th>continent</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>150</th>
      <td>Afghanistan</td>
      <td>AFG</td>
      <td>1950</td>
      <td>7752000.0</td>
      <td>27.638</td>
      <td>2392.0</td>
      <td>Asia</td>
    </tr>
    <tr>
      <th>151</th>
      <td>Afghanistan</td>
      <td>AFG</td>
      <td>1951</td>
      <td>7840000.0</td>
      <td>27.878</td>
      <td>2422.0</td>
      <td>Asia</td>
    </tr>
    <tr>
      <th>152</th>
      <td>Afghanistan</td>
      <td>AFG</td>
      <td>1952</td>
      <td>7936000.0</td>
      <td>28.361</td>
      <td>2462.0</td>
      <td>Asia</td>
    </tr>
    <tr>
      <th>153</th>
      <td>Afghanistan</td>
      <td>AFG</td>
      <td>1953</td>
      <td>8040000.0</td>
      <td>28.852</td>
      <td>2568.0</td>
      <td>Asia</td>
    </tr>
    <tr>
      <th>154</th>
      <td>Afghanistan</td>
      <td>AFG</td>
      <td>1954</td>
      <td>8151000.0</td>
      <td>29.350</td>
      <td>2576.0</td>
      <td>Asia</td>
    </tr>
  </tbody>
</table>
</div>

L'usage est d'importer la bibliothèque Altair sous l'alias `alt`:

```python
>>> import altair as alt
```

### 11.0 Encodages et marques

Les visualisations Altair sont basées sur trois types de données:

- les `alt.Chart` contiennent la donnée (sous forme de `pd.DataFrame`
  ou de chemin vers un fichier);
- la marque (les mots-clés suivant le modèle `.mark_()`) décrit le
  type de visualisation voulu (nuage de points, courbe, etc.);
- le canal d'encodage, ou encodage, (mot-clé `.encode()`) est associé
  à une _feature_ pour distribuer les points sur une caractéristique
  (l'encodage) de la visualisation.

Dans l'exemple suivant, un nuage de points `.mark_point()` sur les
données réduites à l'année 2015, on associe l'abscisse `x`, l'ordonnée
`y` et la couleur `color` chacune à une caractéristique (le PIB par
habitant, l'espérance de vie et le continent). C'est la bibliothèque qui
se charge d'interpréter la description pour fournir une visualisation
conforme.

```python
data_2015 = data.query('year == "2015"')

alt.Chart(data_2015).encode(
    x="GDP_per_capita",
    y="life_expectancy",
    color="continent"
).mark_point()
```

<div id="scatter2015"></div>
<script type="text/javascript">
    var spec = "../_static/altair/2015_scatter.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#scatter2015", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

Les marques les plus fréquentes ont toutes un nom explicite, qui
n'appelle pas nécessairement d'explication approfondie:

|                 |
| :-------------- |
| `mark_point()`  |
| `mark_circle()` |
| `mark_square()` |
| `mark_line()`   |
| `mark_area()`   |
| `mark_bar()`    |
| `mark_tick()`   |

Les canaux d'encodage les plus fréquents sont:

|           |                                   |
| :-------- | :-------------------------------- |
| `x`       | abscisse                          |
| `y`       | ordonnée                          |
| `couleur` | couleur de la marque              |
| `opacity` | transparence/opacité de la marque |
| `shape`   | forme de la marque                |
| `size`    | taille de la marque               |
| `facet`   | répétition du canal               |

Il est possible d'utiliser des arguments nommés pour les canaux sur le modèle
`x="x_data"`, ou d'utiliser les constructeurs Altair associés
`alt.X("x_data")` en paramètres nommés ou non, qui permettent également de
passer des arguments supplémentaires:

- ① un titre `title` différent pour annoter l'axe des ordonnées;
- ② une échelle `scale` qui ne comprend pas la valeur 0;
- ③ un formatage particulier `format` pour compter les populations en
  millions. Le formatage est défini par la bibliothèque web d3js:
  <https://github.com/d3/d3-format>

Altair utilise le type de chacune des _features_ à partir des `dtype`
Pandas. Il est possible de les spécifier néanmoins, et cette étape est
nécessaire si les données sont passées par fichier:

- `Q` pour _quantitative_: des données numériques continues, comme une
  altitude, une température;
- `N` pour _nominal_: des données textuelles, comme un nom de pays;
- `O` pour _ordinal_: des données numériques entières pour des
  classements;
- `T` pour _temporal_: des données temporelles.

```python
data_france = data.query('country == "France"')

alt.Chart(data_france).encode(
    alt.X("year:T", title="année"),  # ①
    alt.Y(
        "population:Q",
        scale=alt.Scale(zero=False),  # ②
        axis=alt.Axis(format="~s")  # ③
    ),
).mark_line()
```

<div id="population_france"></div>
<script type="text/javascript">
    var spec = "../_static/altair/population_france.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#population_france", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

Un nuage de points sans encodage affiche un simple point. Bien que cette
entrée ne renvoie pas d'erreur, elle n'est pas pertinente en soi.

```python
alt.Chart(data).mark_point()
```

<div id="mark_point"></div>
<script type="text/javascript">
    var spec = "../_static/altair/mark_point.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#mark_point", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

Pour un encodage de données nominales, une coordonnée est attribuée à
chaque élément unique de la _feature_. Les plages de couleurs sont
également choisies en fonction, pour distinguer clairement une catégorie
d'une autre.

```python
alt.Chart(data).encode(
    alt.Y("continent:N"),
    alt.Color("continent:N")
).mark_square()
```

<div id="mark_continent"></div>
<script type="text/javascript">
    var spec = "../_static/altair/mark_continent.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#mark_continent", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

### 11.1 Agrégation et composition

L'agrégation de données correspond à l'opération `groupby()` en Pandas.
Altair permet de définir ce type d'opération à calculer sur les données
préparées passées en paramètre. Le calcul est alors effectué par la
bibliothèque Javascript de visualisation au lieu de l'être par Pandas.
L'avantage principal est que le volume des données produites pour créer
toutes les visualisations est réduit.

Dans l'exemple ci-dessous, la préparation de données équivalente avant
visualisation serait, pour un calcul de valeur médiane:

```python
data_2015.groupby("continent").agg({"GDP_per_capita": "median"})
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: left;
    }

</style>
<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>continent</th>
      <th>GDP_per_capita</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Africa</th>
      <td>2954.0</td>
    </tr>
    <tr>
      <th>Asia</th>
      <td>11738.0</td>
    </tr>
    <tr>
      <th>Europe</th>
      <td>26240.0</td>
    </tr>
    <tr>
      <th>North America</th>
      <td>10358.5</td>
    </tr>
    <tr>
      <th>Oceania</th>
      <td>38890.5</td>
    </tr>
    <tr>
      <th>South America</th>
      <td>14117.5</td>
    </tr>
  </tbody>
</table>
</div>

```python
alt.Chart(data_2015).encode(
    alt.X(
        "median(GDP_per_capita):Q",
        title="PIB par habitant médian en 2015", axis=alt.Axis(format="~s"),
    ),
    alt.Y("continent:N"),
    alt.Color("continent:N"),
).mark_bar(size=10)
```

<div id="pib_continent"></div>
<script type="text/javascript">
    var spec = "../_static/altair/pib_continent.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#pib_continent", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

D'autres opérateurs d'agrégation sont disponibles, notamment pour la
somme `sum`, le produit `product`, la moyenne `mean`, le minimum `min`,
le maximum `max`, le nombre d'éléments vides `missing`, ou le nombre
d'éléments distincts `distinct`.

L'exemple suivant affiche le nombre de pays par continent. Chaque pays
est représenté de nombreuses fois dans le fichier (une fois par année)
mais l'opérateur `distinct` comprend cette nuance.

```python
alt.Chart(data).encode(
    alt.X("distinct(country):N", title="Nombre de pays"),
    alt.Y("continent:N"),
    alt.Color("continent:N"),
).mark_bar(size=10)
```

<div id="nb_continent"></div>
<script type="text/javascript">
    var spec = "../_static/altair/nb_continent.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#nb_continent", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

Il est possible de produire des agrégations quel que soit le canal
d'encodage. Dans la visualisation suivante, l'écart-type est encodé dans
la couleur des barres. Comme le PIB par habitant est annoté comme type
de données _quantitatif_, Altair choisit une table de couleur adaptée
qui fait varier la **saturation** de la couleur, par opposition au type
de données _nominatif_ qui fournit une table de couleur faisant varier
la **teinte**.

Cet exemple est aussi l'occasion de préciser deux autres options:

- L'attribut `sort` ① permet ici de trier les catégories de l'axe `Y`
  suivant un critère qui peut être arbitraire, croissant ou
  décroissant (par rapport à l'ordre alphabétique pour les variables
  nominatives), ou suivant l'ordre associé à un autre canal
  d'encodage. Le signe `-` dans l'exemple ci-dessous indique un ordre
  décroissant. Cette option permet d'ordonner visuellement les barres
  par longueur décroissante plutôt que par ordre alphabétique sur le
  nom des continents.

- L'attribut `scale` ② fonctionne également pour le canal d'encodage de
  couleur: il permet ici de calibrer les bornes inférieures et
  supérieures de la table de couleurs. Par défaut, ces bornes sont
  assignées aux valeurs minimales et maximales trouvées dans les
  données.

```python
alt.Chart(data_2015).encode(
    alt.X(
        "mean(GDP_per_capita):Q",
        axis=alt.Axis(format="~s"), title="Moyenne du PIB par habitant",
    ),
    alt.Y("continent:N", sort="-x"),  # ①
    alt.Color(
        "stdev(GDP_per_capita):Q", title="Écart-type",
        scale=alt.Scale(domain=(0, 30e3))  # ②
    ),
).mark_bar(size=10)
```

<div id="pib_continent_std"></div>
<script type="text/javascript">
    var spec = "../_static/altair/pib_continent_std.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#pib_continent_std", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

L'Asie semble être le continent avec le plus d'inégalités de richesse.
Un diagramme en boîte permet de visualiser différemment les données: les
éléments atypiques sortent des boîtes à moustache et le canal d'encodage
`tooltip` permet d'afficher le nom du pays quand on passe la souris sur
le point. Le Qatar en Asie et la Norvège en Europe par exemple sont des
pays au PIB par habitant très supérieur à celui des voisins.

```python
alt.Chart(data_2015).encode(
    alt.X("GDP_per_capita:Q", axis=alt.Axis(format="~s"), title="PIB par habitant",),
    alt.Y("continent:N"),
    alt.Tooltip("country:N"),
).mark_boxplot(size=10)
```

<div id="pib_continent_boxplot"></div>
<script type="text/javascript">
    var spec = "../_static/altair/pib_continent_boxplot.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#pib_continent_boxplot", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

Le tracé d'histogrammes est vu par Altair du point de vue d'une
agrégation particulière où les échantillons sont répartis en classes (le
mot-clé _bin_ en anglais, déjà vu avec Matplotlib, puis la méthode
d'agrégation sans argument `count()`): il faut donc préciser cette
agrégation pour visualiser des distributions.

Une autre fonctionnalité permise par Altair est la composition de
graphes:

- l'opérateur `+` associe plusieurs couches (_layers_) sur la même
  visualisation;
- les opérateurs `|` et `&` concatènent deux visualisations côte à côte
  (`hconcat` pour _horizontal_) ou l'une au-dessus l'autre (`vconcat` pour
  _vertical_).

Lors de composition de graphes, il est possible de **factoriser des
spécifications**. Dans l'exemple suivant, le même graphe est affiché
deux fois, la visualisation de droite ajoute un canal d'encodage de
couleur ①. On notera également l'utilisation de la fonction
`.properties` ② qui permet entre autres de spécifier la taille de la
fenêtre.

```python
base = (
    alt.Chart(data_2015)
    .encode(
        alt.X(
            "GDP_per_capita", bin=alt.Bin(maxbins=30),
            title="PIB par habitant", axis=alt.Axis(format="$~s"),
        ),
        alt.Y("count()", title="Nombre de pays"),
    )
    .mark_bar()
    .properties(width=280, height=200)  # ②
)

base | base.encode(alt.Color("continent"))  # ①
```

<div id="histogrammes"></div>
<script type="text/javascript">
    var spec = "../_static/altair/histogrammes.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#histogrammes", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

Il est également possible de changer de marque entre deux visualisations
factorisées, ou de surcharger des encodages ou personnalisations
précédemment spécifiées.

```python
# Définition de la partie commune aux visualisations
base = (
    alt.Chart(data_2015)
    .encode(
        alt.X(
            "sum(population):Q",
            title="Population totale en 2015", axis=alt.Axis(format="~s"),
        ),
        alt.Color("continent:N", legend=None),
    )
    .mark_bar(size=10)
    .properties(width=280)
)

(
    base.encode(alt.Y("continent:N", title=None))
    | base.encode(alt.X("population:Q"), alt.Y("continent:N")).mark_point()
) & base.properties(width=680)
```

<div id="factorisation"></div>
<script type="text/javascript">
    var spec = "../_static/altair/factorisation.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#factorisation", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

### 11.2 Transformation

Nous avons vu avec les méthodes d'agrégation que les visualisations
peuvent appeler des calculs intermédiaires sur les données d'origine.
Ces calculs peuvent être faits _via_ Pandas avant de programmer une
visualisation, ou au sein de la visualisation à l'aide de nombreuses
_fonctions de transformation_ Altair spécifiques.

Les fonctions de transformation (les mots-clés suivant le modèle
`.transform_`) changent la structure des données d'entrée pour y ajouter
de nouvelles colonnes, ou _features_, filtrer ou trier des lignes
suivant un critère, ou opérer des jointures sur d'autres tables.

Les principales fonctions de transformation sont:

|                             |                                                           |
| :-------------------------- | :-------------------------------------------------------- |
| `transform_aggregate()`     | agrégation d'une colonne avec écrasement                  |
| `transform_joinaggregate()` | agrégation d'une colonne dans une nouvelle colonne        |
| `transform_calculate()`     | calcul d'une nouvelle grandeur                            |
| `transform_density()`       | calcul d'une estimation de densité                        |
| `transform_window()`        | calcul d'un critère par fenêtre (sous-ensemble de lignes) |

Dans l'exemple suivant, on crée une nouvelle _feature_ avec la
population moyenne par pays dans l'intervalle d'années considéré, afin
d'ordonner les pays avec le plus peuplé en moyenne en bas de l'affichage
et le moins peuplé en haut. La transformation `joinaggregate` permet de
conserver la _feature_ `population` malgré le calcul de sa version
agrégée.

La deuxième transformation `filter` permet de ne sélectionner que les
pays d'Europe avec plus de 50 millions d'habitants en moyenne. Le
paramètre `datum` fait référence au jeu de données embarqués dans le
constructeur `alt.Chart`.

```python
(
    alt.Chart(data)
    .encode(
        alt.X("year:T", title="année"),
        alt.Y("population:Q", axis=alt.Axis(format="~s")),
        alt.Color("country:N", title="pays"),
        alt.Order("mean_pop:Q", sort="descending"),
    )
    .mark_area()
    .transform_joinaggregate(mean_pop="mean(population)", groupby=["country"])
    .transform_filter({"and": ["datum.continent == 'Europe'", "datum.mean_pop > 50e6"]})
    .properties(width=400, height=200)
)
```

<div id="transform_moyenne"></div>
<script type="text/javascript">
    var spec = "../_static/altair/transform_moyenne.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#transform_moyenne", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

L'exemple suivant met en application toutes les notions vues jusqu'ici.
On cherche à afficher les dix premiers pays suivant un critère donné sur
le même jeu de données. Ici aucun prétraitement Pandas n'a été réalisé.
Tout est spécifié dans Altair:

- une spécification est factorisée entre les deux visualisations ①. La
  différence réside dans la `feature` attribuée au canal d'encodage
  `x`;

- le critère est évalué sur la dernière donnée (en fonction de
  l'année) présente par pays: les deux colonnes `population` et
  `GDP_per_capita` sont remplacées par la valeur correspondant à
  l'année la plus récente. C'est l'agrégation `argmax` ② qui retrouve
  la dernière donnée associée à chaque pays, la transformation
  `calculate` ③ sélectionne les données de population en se basant sur
  les indices produits par `argmax`.\
  On notera l'utilisation du mot-clé `datum` qui rappelle le jeu de
  données manipulé;

- le tri des pays par ordre décroissant est spécifié dans l'encodage
  du canal `y`. En revanche la coupe après les 10 premiers pays
  nécessite l'application d'un critère basé sur le rang de chaque
  valeur en fonction des valeurs décroissantes de `population` et de
  `GDP_per_capita` ④. _In fine_, c'est un `transform_filter()` qui se
  charge de sélectionner les lignes en fonction du rang ⑤.

```python
base = (
    alt.Chart(data)
    .mark_bar(size=10)
    .encode(alt.Y("country:N", sort="-x", title="pays"), alt.Color("continent:N"),)  # ①
    .transform_aggregate(  # ②
        most_recent_year="argmax(year)", groupby=["country", "continent"]
    )
    .transform_calculate(  # ③
        population="datum.most_recent_year.population",
        GDP_per_capita="datum.most_recent_year.GDP_per_capita",
    )
    .transform_window(  # ④
        rank_pop="rank(population)",
        sort=[alt.SortField("population", order="descending")],
    )
    .transform_window(
        rank_gdp="rank(GDP_per_capita)",
        sort=[alt.SortField("GDP_per_capita", order="descending")],
    )
    .properties(width=300, height=200)
)

(
    base.encode(alt.X("population:Q", axis=alt.Axis(format="~s"))).transform_filter(
        alt.datum.rank_pop <= 10  # ⑤
    )
    | base.encode(
        alt.X("GDP_per_capita:Q", axis=alt.Axis(format="$~s"), title="PIB par habitant")
    ).transform_filter(
        alt.datum.rank_gdp <= 10  # ⑤
    )
)
```

<div id="transform_complete"></div>
<script type="text/javascript">
    var spec = "../_static/altair/transform_complete.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#transform_complete", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

### 11.3 Interactivité

L'interactivité la plus simple est celle qui est induite par l'encodage
de canal `tooltip`: au passage de la souris sur un point donné, un
pop-up apparaît avec les informations spécifiées. La documentation
montre de nombreux exemples d'interactivité, basés sur les mouvements de
la souris, la sélection d'intervalles, ou d'autres.

L'exemple ci-dessous reprend le type de visualisation avec lequel Hans
Rosling s'est illustré lors de plusieurs conférences TED: un point
correspond à un pays, sa taille à sa population. Ici, on place en $x$ le
PIB par habitant et en $y$ l'espérance de vie dans le pays.

On souhaite animer la visualisation par année pour pouvoir suivre la
trajectoire de chacun de ces pays dans cette espace. Cette sélection se
fait au moyen d'un widget où la poignée sélectionne l'année ①. La
méthode `selection_single` réagit en attribuant au champ `year` la
valeur positionnée sur le widget: la visualisation est alors mise à jour
quand la valeur du champ change.

L'encodage est basique ②; le nom du pays s'affiche quand on passe la
souris sur un point; le canal `text` servira à annoter certains points
de manière permanente, directement sur la visualisation; l'axe des
abscisses est choisi logarithmique. Au lieu de choisir la dernière année
qui contient des données, on choisit les données de l'année sélectionnée
par le widget. ③

La visualisation est alors constituée de deux couches: les cercles de
couleur (par continent) à la taille proportionnelle à la population du
pays (en échelle logarithmique); et une annotation textuelle pour
certains pays dont la trajectoire reflète le cours de l'histoire (chute
de l'URSS, Khmers rouges au Cambodge, fin de l'Apartheid en Afrique du
Sud, essor économique spectaculaire de la Corée du Sud).

```python
annotate_countries = [
    "South Africa", "United States", "France", "China", "Russia", "Nigeria",
    "Brazil", "South Korea", "Japan", "India", "Cambodia",
]

year_slider = alt.binding_range(min=1950, max=2015, step=1, name="year:")  # ①
year_selector = alt.selection_single(
    name="year_selection", fields=["year"], bind=year_slider, init={"year": 2000}
)

base = (
    alt.Chart(data)
    .encode(  # ②
        alt.X(
            "GDP_per_capita:Q", axis=alt.Axis(format="k"),
            scale=alt.Scale(type="log", domain=(100, 1e5)), title="PIB par habitant",
        ),
        alt.Y(
            "life_expectancy:Q",
            scale=alt.Scale(domain=(20, 90)), title="Espérance de vie",
        ),
        alt.Text("country:N"),
        alt.Tooltip("country:N"),
    )
    .transform_filter("datum.year == year_selection.year")  #  ③
    .properties(width=600, height=400)
)
(
    base.mark_circle()
    .encode(
        alt.Color("continent:N"),
        alt.Size("population:Q", scale=alt.Scale(domain=(5e6, 1e9), type="log")),
    )
    .add_selection(year_selector)
    + base.transform_filter(
        {"field": "country", "oneOf": annotate_countries}
    ).mark_text(size=14, align="right", xOffset=-10, font="Ubuntu")
)
```

<div id="interactive"></div>
<script type="text/javascript">
    var spec = "../_static/altair/interactive.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#interactive", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

### 11.4 Configuration

Il est possible de personnaliser l'affichage d'une visualisation Altair
à trois niveaux:

- celui de l'encodage: on associe une valeur de couleur, de forme, à
  une _feature_;
- celui de la marque: on spécifie localement la configuration;
- celui de l'affichage complet, à l'aide des fonctions
  `.configure_()`.

La dernière méthode est souvent la manière privilégiée de procéder à des
microajustements, par exemple sur la taille des polices, le
positionnement des étiquettes.

```python
base = (
    alt.Chart(data_france)
    .encode(
        alt.X("year:T", title="année"),
        alt.Y("population:Q", scale=alt.Scale(zero=False), axis=alt.Axis(format="~s")),
    )
    .mark_line()
)
(
    base.properties(title="Population française", height=200, width=300)
    .configure_axis(labelFontSize=12, titleFontSize=0, labelAngle=-30)
    .configure_line(size=3, color="#008f6b")
    .configure_title(anchor="start", fontSize=16, font="Fira Sans", color="#008f6b")
    .configure_view(stroke=None)
)
```

<div id="configure"></div>
<script type="text/javascript">
    var spec = "../_static/altair/configure.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#configure", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

### 11.5 Coordonnées géographiques

Le support pour les structures de données géographiques dans Altair est
encore jeune à l'heure où ces lignes sont écrites. Il est néanmoins
possible de produire des cartes à partir de fichiers au format
standardisé pour décrire des informations géographiques, les formats les
plus courants étant GeoJSON et TopoJSON.

Altair fournit alors:

- un marqueur spécialisé `.mark_geoshape()`;
- deux canaux d'encodage pour la latitude et la longitude;
- un type d'encodage pour les formes géométriques `geojson` (`G`);
- une opération de projection parmi une liste de projections
  simples: p. ex. `mercator`, `orthographic`, `conicConformal`, etc.

La difficulté consiste alors ici à avoir accès à des fonds de carte pour
créer des visualisations de qualité. La bibliothèque fournit parmi les
jeux de données officiels `vega_datasets` une carte du monde de haut
niveau et une carte des États-Unis à bonne résolution.

Pour un public francophone, on trouvera à l'heure de l'écriture de ces
lignes:

- des données sur la France:
  <https://github.com/gregoiredavid/france-geojson>
- des données sur la Belgique:
  <https://github.com/arneh61/Belgium-Map>
- des données sur la Suisse:
  <https://github.com/interactivethings/swiss-maps>

L'utilisation de la bibliothèque geopandas[^3] (qui ne sera pas
détaillée dans cet ouvrage) facilite la manipulation des fichiers
GeoJSON et TopoJSON sous forme de tableau Pandas dont les colonnes sont
les métadonnées, et une colonne particulière, généralement nommée
`geometry`, contient une structure qui représente la forme de l'objet en
question.

```python
import geopandas as gpd

github_url = "https://raw.githubusercontent.com/{user}/{repo}/master/{path}"

regions_fr = gpd.GeoDataFrame.from_file(
    github_url.format(
        user="gregoiredavid", repo="france-geojson",
        path="regions-version-simplifiee.geojson",
    )
)
departements_fr = gpd.GeoDataFrame.from_file(
    github_url.format(
        user="gregoiredavid", repo="france-geojson",
        path="departements-version-simplifiee.geojson",
    )
)

belgique = gpd.GeoDataFrame.from_file(
    github_url.format(user="arneh61", repo="Belgium-Map", path="Provincies.json",)
).assign(
    centroid_lon=lambda df: df.geometry.centroid.x,
    centroid_lat=lambda df: df.geometry.centroid.y,
)
```

La structure geopandas peut être passée en argument de `alt.Chart` et il
est alors possible d'utiliser la marque géographique. Ici, on choisit le
nom de la région en encodage de la couleur. Dans l'exemple de la carte
de la Belgique, on ajoute le nom de chaque province au centroïde de la
forme géométrique. Le nom de Bruxelles est enlevé (`transform_filter`)
pour ne pas se chevaucher avec celui du Brabant Flamand. Enfin, la
coordonnée en latitude du texte est volontairement bruitée pour éviter
les chevauchements (`transform_calculate`); des méthodes de placement
d'étiquettes textuelles sans chevauchement plus complexes existent mais
sortent du cadre de cet ouvrage.

```python
base = alt.Chart(belgique)
(
    base.mark_geoshape(stroke="white").encode(alt.Color("NAME_1", title="Région"))
    + (
        base.encode(
            alt.Longitude("centroid_lon"),
            alt.Latitude("centroid_lat"),
            alt.Text("NAME_2"),
        )
        .mark_text(color="black", font="Ubuntu", fontSize=12)
        .transform_filter("datum.NAME_2 != 'Bruxelles'")
        .transform_calculate(centroid_lat="datum.centroid_lat + .1 * (random() - .5)")
    )
)
```

<div id="belgique"></div>
<script type="text/javascript">
    var spec = "../_static/altair/belgique.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#belgique", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

Contrairement à Matplotlib, la projection par défaut choisie pour les
cartes est la projection de Mercator. L'utilisation de la projection
plate carrée qui associe la latitude à la coordonnée `y` et la longitude
à la coordonnée `x` est moins directe. La figure suivante compare à ce
titre les trois projections plate carrée, inadaptée pour la plupart des
usages, Mercator, qui fonctionne par défaut dans la plupart des régions
du monde, et Lambert 93, définie ici manuellement, qui est la projection
standard en France. Un graticule (une grille de lignes isolatitudes et
isolongitudes) est ajouté ① pour donner une meilleure perception des
opérations de projection.

```python
base = (
    alt.Chart(
        alt.graticule(step=[2, 2], extentMajor=([-5, 41], [11, 52]))  # ①
    ).mark_geoshape(fill="None", stroke="#008f6b")
    + alt.Chart(regions_fr).mark_geoshape(
        stroke="white", fill="#008f6b", strokeWidth=1.2
    )
).properties(width=250, height=250)

(
    base.project("identity", reflectY=True).properties(title="Plate Carrée")
    | base.project("mercator").properties(title="Mercator (par défaut)")
    | (
        base.project("conicConformal", rotate=[-3, -46.5], parallels=[49, 44])
        .properties(title="Lambert 93")
    )
).configure_title(font="Ubuntu", fontSize=15, anchor="start")
```

<div id="france"></div>
<script type="text/javascript">
    var spec = "../_static/altair/france.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#france", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

L'affichage de fonds de carte est rarement une fin en soi. L'intérêt est
de pouvoir afficher des informations supplémentaires. On peut ajouter
une couche (_layer_) à notre fond de carte, et utiliser les canaux
d'encodage `latitude` et `longitude`. Nous illustrons ici cette
utilisation avec l'exemple des toponymes au suffixe -acum : une colonne
est ajoutée pour catégoriser les villes par suffixe, l'encodage `color`
se charge ensuite de la visualisation.

```python
(
    (
        alt.Chart(regions_fr)
        .mark_geoshape(stroke="grey", fill="white")
        .project("conicConformal", rotate=[-3, -46.5], parallels=[49, 44])  # Lambert 93
        + alt.Chart(
            pd.concat(
                [
                    villes.query(
                        f"nom.str.contains('.{fin}$')", engine="python"
                    ).assign(suffixe=f"-{fin}")
                    for fin in ["ac", "ach", "acq", "ay", "az", "ecques"]
                ]
            )
        )
        .mark_circle(opacity=0.5)
        .encode(
            alt.Latitude("latitude"),
            alt.Longitude("longitude"),
            alt.Color("suffixe"),
            alt.Tooltip("nom"),
        )
    )
    .properties(title="Le suffixe -acum dans les toponymes en France")
    .configure_legend(
        labelFont="Ubuntu", titleFont="Ubuntu", labelFontSize=13, titleFontSize=14
    )
    .configure_title(font="Ubuntu", fontSize=16, anchor="start")
    .configure_view(stroke=None)
)
```

<div id="villes_acum"></div>
<script type="text/javascript">
    var spec = "../_static/altair/villes_acum.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#villes_acum", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

L'interaction entre les données et les fonds de carte peut être plus
marquée, comme dans les cartes choroplèthes qui associent une couleur à
une région géographique. On peut ici reprendre les statistiques de
population par département français  pour associer chaque mesure à un
polygone affiché sur la carte.

Cette association se fait ici sur la base du numéro du département (dans
la colonne `departement`) qui est présent dans le `pd.DataFrame` et dans
le fichier GeoJSON des départements (dans la propriété `code`) à l'aide
de la fonction `.transform_lookup`.

```python
feature_list = ["altitude_max", "population"]

chart = (
    alt.Chart(departements_fr)
    .mark_geoshape(stroke="white")
    .encode(alt.Tooltip(["code", "nom"]))
    .transform_lookup(lookup="code", from_=alt.LookupData(stats, "departement", feature_list))
    .project("conicConformal", rotate=[-3, -46.5], parallels=[49, 44])
    .properties(width=220, height=200)
)
(
    chart.encode(alt.Color("altitude_max:Q")) | chart.encode(alt.Color("population:Q"))
).configure_view(stroke=None).resolve_scale(color="independent")
```

<div id="france_choroplethes"></div>
<script type="text/javascript">
    var spec = "../_static/altair/france_choroplethes.json";
    var opt = {"renderer": "canvas", "actions": true};
    vegaEmbed("#france_choroplethes", spec, opt).then(function(result) {
    }).catch(console.error);
</script>

### 11.6 ipyleaflet

ipyleaflet[^4] est une bibliothèque Python spécifiquement conçue pour
l'environnement Jupyter. Elle permet un portage de l'application
Javascript Leaflet qui propose d'enrichir des widgets de cartes
interactives sur le modèle de Google Maps ou OpenStreetMap. La
bibliothèque met à disposition un widget particulier `Map`, à l'image
des autres structures `ipywidgets` qu'il est possible d'enrichir et
d'équiper de fonctions _callbacks_ (des fonctions déclenchées
automatiquement lors d'événements prédéfinis) pour l'interaction.

Une carte est alors initialisée sur des coordonnées géographiques avec
un niveau de zoom. Dans l'exemple ci-dessous, on affiche les vingt
communes les plus peuplées au bout d'un `Marker`. Ces éléments sont par
défaut interactifs : un clic dessus ouvre une fenêtre où l'on peut
insérer un nouveau widget au choix, ici un simple contenu enrichi avec
le nom de la ville et sa population.

Dans cet exemple, on ajoute également un menu déroulant `Dropdown` avec
la liste des villes affichées: la fonction de rappel récupère ici les
coordonnées de la ville sélectionnée pour centrer la carte dessus.
Enfin, il est également possible d'enrichir une carte avec des
informations issues de fichiers au format GeoJSON, à l'image de ceux
utilisés pour Altair. Le paramètre `hover_style` permet ici de
configurer un comportement interactif simple où le style est mis à jour
quand la souris passe au-dessus d'un élément.

```python
from ipyleaflet import Map, Marker, GeoData
from ipywidgets import HTML, Layout, Dropdown

top_20 = villes.sort_values("population", ascending=False).head(20)

map_ = Map(center=(46.5, 3), zoom=5, layout=Layout(max_width="400px"))  # ①

for _, data in top_20.iterrows():
    marker = Marker(location=(data.latitude, data.longitude), draggable=False)  # ②
    marker.popup = HTML(f"<b>{data.nom}</b>: {data.population:_} habitants")  # ③
    map_.add_layer(marker)

def on_click(info):
    ville = top_20.set_index("nom").loc[info["new"]]
    map_.center = (ville.latitude, ville.longitude)
    map_.zoom = 8

dropdown = Dropdown(description="Ville:", options=sorted(top_20.nom))
dropdown.observe(on_click, names="value")

geodata = GeoData(
    geo_dataframe=departements_fr,
    style={"color": "#008f6b", "opacity": 1, "fillOpacity": 0.1, "weight": 1},
    hover_style={"color": "white", "fillOpacity": 0.4, "weight": 3, "zorder": 2},
)
map_.add_layer(geodata)

display(dropdown, map_)
```

### En quelques mots...

- L'environnement Jupyter intégré aux navigateurs web permet
  d'importer les facilités d'interactivité développées dans les
  bibliothèques Javascript modernes pour produire des visualisations
  et environnements d'exploration des données tout en restant dans
  l'ecosystème Python.

- Matplotlib  et Altair abordent la visualisation de données de deux
  points de vue différents. Matplotlib propose un langage bas niveau
  et des structures de données qui permettent de configurer tous les
  éléments d'une présentation graphique. Altair expose une _grammar of
  graphics_ (grammaire de visualisation) qui permet de spécifier une
  visualisation pour la décliner ensuite sur les données. C'est
  probablement l'équivalent le plus proche des bibliothèques de
  visualisation avancées d'autres langages, comme `ggplot2` en R.

**Pour aller plus loin**

- _The Grammar of Graphics_, Leland Wilkinson, 2012\
  Springer, ISBN 978-1-4419-2033-1

- _Fundamentals of Data Visualization_, Claus O. Wilke, 2018\
   O'Reilly, ISBN 978-1-4920-3108-6\
   <https://clauswilke.com/dataviz/>

[^1]: <https://ourworldindata.org/grapher/life-expectancy-vs-gdp-per-capita>
[^2]: <https://www.ted.com/talks/hans_rosling_let_my_dataset_change_your_mindset>
[^3]: <https://geopandas.readthedocs.io/>
[^4]: https://ipyleaflet.readthedocs.io/
