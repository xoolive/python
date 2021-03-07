---
permalink: /protocols/tour_de_france
title: Le Tour de France 2020
back: /python/protocols/
layout: code
partie: 03-pythonic
chapitre: 16-protocols
code: tour_de_france.py
---

## Couverture du Tour de France 2020 par les avions de relais télévisés

![Tour de France 2020](/python/_static/tour_de_france.png){: style="max-width: 50%;"}

Les événements sportifs comme le Tour de France font appel à des hélicoptères pour filmer la course au fur et à mesure que les cyclistes parcourent les routes de France. Ces hélicoptères volent à basse altitude, et d'autres avions évoluent alors à plus haute altitude pour relayer les signaux TV des images prises par les hélicoptères et les partager en direct avec les chaînes de télévision. Le DataFrame Pandas suivant contient toutes les trajectoires d'un avion qui a été recruté pour couvrir l'édition 2020 du Tour de France. Ces données sont issues du réseau OpenSky Network [https://opensky-network.org](https://opensky-network.org).

Les altitudes sont exprimées en pieds, la vitesse sol `groundspeed` est exprimée en nœuds, la vitesse verticale `vertical_rate` en pieds par minute et l'angle `track`, en degrés, représente le cap (l'angle de route) suivi par l'avion. La colonne `icao24` est un identifiant unique par avion, qui peut être assimilé à son immatriculation et la colonne `callsign` représente une mission ou un numéro de vol.

Dans le tableau fourni, un seul avion est représenté mais on trouve plusieurs trajectoires dans le jeu de données. On imagine alors ici une classe `Collection` qui implémente le protocole `Iterable` et une classe `Trajectoire` qui ont toutes les deux un attribut `"data: pd.DataFrame"`. Dans l'exemple ci-dessous, les classes sont utilisées pour reconstruire une carte de France avec le parcours du Tour de France 2020 (limité aux journées qui ont été couvertes par l'avion en question).

|              Début |                Fin |     Durée |
|-------------------:|-------------------:|----------:|
|      29 août 07:27 |      29 août 10:37 |  03:09:55 |
|      30 août 10:27 |      30 août 16:42 |  06:15:00 |
|      31 août 09:37 |      31 août 15:42 |  06:05:00 |
| 01 septembre 10:52 | 01 septembre 15:57 |  05:04:50 |
| 02 septembre 10:27 | 02 septembre 15:22 |  04:55:00 |
| 03 septembre 10:07 | 03 septembre 15:02 |  04:55:00 |
| 04 septembre 10:52 | 04 septembre 15:12 |  04:19:55 |
| 05 septembre 10:47 | 05 septembre 15:47 |  04:59:55 |
| 06 septembre 09:37 | 06 septembre 14:47 |  05:09:55 |
| 08 septembre 10:52 | 08 septembre 15:27 |  04:34:50 |
| 09 septembre 10:47 | 09 septembre 15:52 |  05:05:00 |
| 10 septembre 09:42 | 10 septembre 15:17 |  05:34:50 |
| 11 septembre 09:27 | 11 septembre 15:17 |  05:49:55 |
| 12 septembre 10:27 | 12 septembre 15:47 |  05:19:55 |
| 13 septembre 10:02 | 13 septembre 15:22 |  05:19:55 |
| 15 septembre 10:32 | 15 septembre 15:57 |  05:24:50 |
| 16 septembre 09:47 | 16 septembre 15:22 |  05:35:00 |
| 17 septembre 09:47 | 17 septembre 15:22 |  05:35:00 |
| 18 septembre 10:52 | 18 septembre 15:27 |  04:34:50 |