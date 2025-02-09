---
permalink: /pyscript/fractals
back: /python/pyscript/
layout: pyscript
---

## Dessiner des fractales dans le navigateur

Sélectionner une courbe pour démarrer le dessin:
<select id="fractale" py-mouseup="tracer">
  <option value="koch">Courbe de Koch</option>
  <option value="sierpinsky">Fractale de Sierpinsky</option>
  <option value="hilbert">Courbe de Hilbert</option>
  <option value="crystal">Cristal</option>
  <option value="snow_flake">Flocon de neige</option>
</select>
<input
  id="ordre"
  class="number-input"
  type="number"
  min="3"
  max="5"
  value="4"
/>

<div id="dessin"></div>

<script type="py" src="/python/assets/fractals/main.py" config="/python/assets/fractals/pyscript.toml"></script>
