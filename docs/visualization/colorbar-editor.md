# Colorbar Editor — Customizable Colormaps

The customizable colorbar editor required by the PS — palette, min/max, log/linear
scale, opacity, and vertical exaggeration controls.

---

## PS Requirement

> "Customizable Colorbar & Variable Controls: Dynamic colorbar editor (color palette,
> min/max range, log/linear scale), variable selector, layer opacity controls, and
> vertical exaggeration slider for intuitive depth perception."

---

## Colorbar Editor UI

### Controls

| Control | Type | Range | Default |
|---|---|---|---|
| Palette | Dropdown | turbo, plasma, viridis, RdBu, coolwarm, Spectral, cubehelix | turbo |
| Min value | Slider/Input | variable-dependent | auto (data min) |
| Max value | Slider/Input | variable-dependent | auto (data max) |
| Scale | Toggle | linear / log | linear |
| Opacity | Slider | 0.0 – 1.0 | 0.7 |
| Vertical exaggeration | Slider | 1× – 200× | 50× |
| Invert palette | Toggle | on/off | off |
| Custom stops | Color picker | user-defined | — |

### Visual Colorbar

A vertical or horizontal colorbar showing the palette with labeled tick marks:

```
32°C ┤████████████████████████████████████┤ red
     │██████████████████████████████████ │
20°C │████████████████████████████████   │
     │██████████████████████████████     │
10°C │████████████████████████████       │
     │██████████████████████████         │
 0°C │████████████████████████           │
     │██████████████████████             │
-2°C ┤████████████████████████████████████┤ blue
```

---

## Implementation

### Colormap as GPU LUT

The colormap is a **1D texture** (lookup table) uploaded to the GPU. The fragment
shader samples it by the scalar value:

```glsl
// Fragment shader (simplified)
float value = texture2D(uDataTexture, vUv).r;
float normalizedValue = (value - uMin) / (uMax - uMin);
if (uLogScale) {
  normalizedValue = log(value - uMin + 1.0) / log(uMax - uMin + 1.0);
}
normalizedValue = clamp(normalizedValue, 0.0, 1.0);
vec3 color = texture2D(uColormapLUT, vec2(normalizedValue, 0.5)).rgb;
gl_FragColor = vec4(color, uOpacity);
```

### Why Changes Are Instant

| Change | Cost |
|---|---|
| Palette change | Update LUT texture (1 upload) — instant, no data re-fetch |
| Min/max change | Update shader uniforms — instant |
| Log/linear toggle | Update shader uniform — instant |
| Opacity change | Update shader uniform — instant |
| Vertical exaggeration | Update shader uniform — instant |

**The data texture never changes** when adjusting the colorbar — only the color
mapping does. This is why all colorbar edits are instant.

---

## Colormap Library

Using `d3-scale-chromatic` and `cesium-color-maps`:

```js
import { interpolateTurbo, interpolatePlasma, interpolateRdBu } from 'd3-scale-chromatic';

// Build LUT texture from colormap function
function buildColormapLUT(gl, colormapFn, size = 256) {
  const colors = new Uint8Array(size * 4);
  for (let i = 0; i < size; i++) {
    const t = i / (size - 1);
    const rgb = d3.rgb(colormapFn(t));
    colors[i * 4] = rgb.r;
    colors[i * 4 + 1] = rgb.g;
    colors[i * 4 + 2] = rgb.b;
    colors[i * 4 + 3] = 255;
  }
  const texture = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, size, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, colors);
  return texture;
}

const turboLUT = buildColormapLUT(gl, interpolateTurbo);
```

### Available Colormaps

| Colormap | Type | Use case |
|---|---|---|
| `turbo` | Sequential | General temperature (rainbow, perceptually improved) |
| `plasma` | Sequential | Temperature, salinity (perceptually uniform) |
| `viridis` | Sequential | Temperature, salinity (perceptually uniform, print-safe) |
| `inferno` | Sequential | High-contrast temperature |
| `RdBu` | Diverging | Temperature/sea level anomaly (blue-white-red) |
| `coolwarm` | Diverging | Temperature anomaly |
| `Spectral` | Diverging | Multi-category ocean variables |
| `cubehelix` | Sequential | nullschool-style (perceptually uniform) |
| `Kindlmann` | Sequential | nullschool-style (perceptually uniform) |

---

## Variable-Specific Defaults

Each ocean variable has sensible colormap defaults:

| Variable | Default colormap | Default range | Scale |
|---|---|---|---|
| Temperature (thetao) | turbo | -2 to 32 °C | linear |
| Salinity (so) | viridis | 30 to 40 PSU | linear |
| Sea level anomaly (zos) | RdBu | -0.5 to 0.5 m | linear |
| Current speed | plasma | 0 to 1 m/s | linear |
| Chlorophyll | viridis | 0 to 10 mg/m³ | log |
| Dissolved oxygen | coolwarm | 0 to 400 µmol/kg | linear |

---

## Custom Color Stops

For advanced users, allow custom color stops:

```js
const customColormap = {
  stops: [
    { value: -2, color: '#08306b' },
    { value: 5,  color: '#2171b5' },
    { value: 15, color: '#6baed6' },
    { value: 25, color: '#fee391' },
    { value: 32, color: '#fe9929' }
  ],
  interpolate: 'linear'  // or 'log'
};
```

The LUT is rebuilt from the stops — still instant.

---

## Colorbar Display Component

```jsx
function ColorbarEditor({ variable, onChange }) {
  const [palette, setPalette] = useState('turbo');
  const [min, setMin] = useState(-2);
  const [max, setMax] = useState(32);
  const [logScale, setLogScale] = useState(false);
  const [opacity, setOpacity] = useState(0.7);

  return (
    <div className="colorbar-editor">
      <select value={palette} onChange={e => setPalette(e.target.value)}>
        <option value="turbo">Turbo</option>
        <option value="plasma">Plasma</option>
        <option value="viridis">Viridis</option>
        <option value="RdBu">RdBu (anomaly)</option>
      </select>

      <RangeSlider label="Min" value={min} onChange={setMin} />
      <RangeSlider label="Max" value={max} onChange={setMax} />
      <Toggle label="Log scale" checked={logScale} onChange={setLogScale} />
      <RangeSlider label="Opacity" min={0} max={1} step={0.05} value={opacity} onChange={setOpacity} />

      <ColorbarDisplay palette={palette} min={min} max={max} logScale={logScale} />
    </div>
  );
}
```

All changes propagate to the shader uniforms instantly — no data re-fetch.
