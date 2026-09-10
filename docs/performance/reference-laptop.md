# D2 — Reference Laptop + Browser Matrix

Date: 2026-09-10. Every benchmark claim (60 FPS / slice ≤750 ms / cold ≤10 s / 30 FPS + 5000 markers) is unmeasurable without a locked device. This doc locks it.

## 1. Upstream constraints

From `docs/research/d4-lib-pins.md` §3/§4/§7:
- Pin `cesium@1.142.0` exact. WebGL2 default context since 1.101/1.102.
- Billboards + labels require WebGL2 (or WebGL1 + `ANGLE_instanced_arrays` + `MAX_VERTEX_TEXTURE_IMAGE_UNITS > 0`) since 1.140 → our 5000 Argo/Glider markers need it. `scene.pickAsync` (marker click) requires WebGL2.
- **WebGL2 effectively mandatory, not optional, on 1.142.**
- **WebGPU irrelevant**: CesiumJS has no WebGPU impl or concrete roadmap (open issue CesiumGS/cesium#4989; staff replies 2023–2025 "not yet"). Appears only as P6/mermaid path (MDPI Babylon.js volume paper). Cesium lock = WebGL2. Do not gate device choice on WebGPU.
- ion needs: Sentinel-2 assetId 3954, World Bathymetry 2426648, `Authorization: Bearer`, Community quotas.
- Cesium has no official spec sheet; community guidance (staff, `community.cesium.com/t/.../45667`, 2026-03-26): basic = dual-core 2.0 GHz / 4 GB / WebGL2 iGPU; 3D Tiles min = quad-core 3.0 GHz / 8 GB / dGPU 2 GB VRAM / 10 Mbps; **mid-range = 6-core 3.5 GHz / 16 GB / dGPU 4–6 GB VRAM**. "GPU is the primary bottleneck." Our workload (zarr slices + 10k wind particles + 5000 billboards) = mid-range.

## 2. Concrete India configs 2026

| # | Machine | CPU | GPU | RAM | Price (INR) | Source | Status |
|---|---|---|---|---|---|---|---|
| A (iGPU/Iris Xe) | Lenovo IdeaPad Slim 5i 16IRL8 (82XF0077IN) | i5-13500H 12C/16T 4.7 GHz | Intel Iris Xe | 16 GB LPDDR5-5200 dual | store promo | `https://www.lenovo.com/in/en/p/laptops/ideapad/ideapad-s-series/ideapad-slim-5i-gen-8-(16-inch-intel)/82xf0077in` ; PSREF `https://psref.lenovo.com/syspool/Sys/PDF/IdeaPad/IdeaPad_Slim_5_16IRL8/IdeaPad_Slim_5_16IRL8_Spec.pdf` | VERIFIED |
| B (iGPU/Radeon) | ASUS Vivobook 16 M1605 | Ryzen 5 150 6C/12T / Ryzen 7 170 8C/16T | Integrated Radeon | 16 GB DDR4 | ~₹55–65k | `https://www.asus.com/in/laptops/for-home/vivobook/asus-vivobook-16-m1605/techspec/` | line VERIFIED; exact 7530U/16 GB SKU marketplace-only (UNVERIFIED on asus.com) |
| C (entry dGPU, reference) | Acer Aspire 7 A715-79G | Core 5 210H / Core 7 240H 2.5–5.2 GHz | NVIDIA RTX 3050 6 GB GDDR6 | 16 GB DDR4 SODIMM 2 slots up to 32 | MRP ₹1,04,999; street ~₹76,990 | `https://store.acer.com/en-in/acer-aspire-7-intel-core-7-240h-processor-16-gb-ram-512-gb-ssd-fhd-15-6-39-62-cm-144hz-windows-11-home-obsidian-black-1-99-kg-a715-79g-backlit-keyboard` | VERIFIED |
| D (weak-iGPU floor) | Lenovo IdeaPad Slim 3 Gen 8 15 (82XQ008VIN) | Ryzen 5 7520U 2.8–4.3 GHz | Integrated Radeon 610M (2 CU) | 16 GB LPDDR5-5500 | ₹40,500 | `https://store.lenovo.com/in/en/ideapad-slim-3-gen-8-39-62cms-amd-r5-arctic-grey-82xq008vin-2191.html` | VERIFIED |

Config D = honest floor: Radeon 610M (2 CU) will very likely miss 30 FPS + 5000 markers + 10k particles. Use as "minimum that must at least load", not target.

## 3. Tiers

| Tier | CPU | GPU | RAM | Honest expectation |
|---|---|---|---|---|
| Minimum acceptable (load, may not hit 60) | 6C/12T U-class | WebGL2 iGPU Iris Xe 96EU or Radeon Vega 7; `MAX_VERTEX_TEXTURE_IMAGE_UNITS > 0` | 16 GB **dual-channel** (single halves iGPU bandwidth) | Slice/cold OK; 30 FPS @5000 = real gate; 60 FPS UNLIKELY |
| Recommended target | 6C+ H-class | entry dGPU RTX 3050 6 GB (or RTX 2050 4 GB min) | 16 GB dual, 512 GB NVMe | 60 FPS plausible 1080p; 30 FPS + 5000 with margin |
| Locked reference | see §4 | | | |

## 4. Locked reference machine

**Acer Aspire 7 A715-79G** — Intel Core 7 240H + RTX 3050 6 GB GDDR6 + 16 GB dual-channel + 512 GB NVMe + 144 Hz FHD panel.

Rationale: (1) dGPU removes iGPU-shared-memory variability making FPS irreproducible; (2) 6 GB VRAM clears community 4–6 GB mid-range bar; (3) **144 Hz panel required** — a 60 Hz panel hard-caps any FPS measurement at 60 and makes "60 FPS" unfalsifiable; (4) available/supportable in India, one SKU, every team measures same silicon. Keep Config A/B iGPU as compatibility floor row in every result table.

## 5. GPU capability check (run once per machine)

```js
// paste in DevTools console on app origin
const gl = document.createElement('canvas').getContext('webgl2');
if (!gl) { console.error('NO WebGL2 — Cesium 1.142 markers/billboards unsupported'); }
const dbg = gl && gl.getExtension('WEBGL_debug_renderer_info');
const out = {
  webgl2: !!gl,
  renderer: dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : 'blocked',
  vendor:   dbg ? gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL)   : 'blocked',
  maxTextureSize: gl && gl.getParameter(gl.MAX_TEXTURE_SIZE),
  maxVertexTextureUnits: gl && gl.getParameter(gl.MAX_VERTEX_TEXTURE_IMAGE_UNITS), // must be > 0
  maxRenderbufferSize: gl && gl.getParameter(gl.MAX_RENDERBUFFER_SIZE),
  colorBufferFloat: !!(gl && gl.getExtension('EXT_color_buffer_float')),
  anisotropy: !!(gl && gl.getExtension('EXT_texture_filter_anisotropic')),
  instancedArraysWebGL1: !!document.createElement('canvas').getContext('webgl')?.getExtension('ANGLE_instanced_arrays'),
  hardwareAccelLikely: !/swiftshader|software|llvmpipe/i.test((dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : '') || ''),
};
console.table(out); console.log(JSON.stringify(out));
```

Plus `chrome://gpu` (Chrome/Edge) or `about:support → Graphics` (Firefox): confirm **Hardware accelerated = Yes**, record driver version. `maxTextureSize` matters — wind-layer failure is `Width must be less than or equal to the maximum texture size (0)` (d4 §4). A WebGL1 or `MAX_VERTEX_TEXTURE_IMAGE_UNITS == 0` machine cannot render 5000 markers on 1.142 → exclude/note.

## 6. Recording fields (every benchmark table)

1. `machine_model` + `serial/service_tag`
2. `cpu_model` exact / `cores_threads`
3. `gpu_model` (UNMASKED_RENDERER_WEBGL) + `vram_gb`
4. `gpu_driver_version`
5. `ram_gb` + `ram_channels` (single/dual) + `ram_speed_mts`
6. `storage_model` + free space
7. `os_build`
8. `browser` + `browser_full_version`
9. `viewport_css_px` W×H + `devicePixelRatio`
10. `panel_refresh_hz` (60/144)
11. `power_mode` (plugged/battery/best-performance) + `thermal_state`
12. `hardware_accel` Yes/No + `webgl_version`
13. `cache_state` (cold/warm/disk-cache) + `network_throttle`
14. `ion_assets_loaded` (Sentinel-2 3954 / CWB 2426648 / none)
15. `zarr_endpoint` (R2/local) + `chunking`
16. `metrics`: `time_to_first_slice_ms`, `slice_ms_p50/p95` (n≥30), `cold_start_ms`, `fps_p50/p95/min`, `marker_count`, `particle_count`, `console_error_count`, `gpu_mem_mb`
17. `date`, `operator`, `app_git_sha`

## 7. Browser matrix (pin exact versions, 2026-09-10)

| Browser | Version | Source | Why |
|---|---|---|---|
| Chrome stable | 153.0.8010.36/.37 (Win/Mac), .36 (Linux); prior 152.0.7977.75 | `https://chromereleases.googleblog.com/2026/09/stable-channel-update-for-desktop_0808145027.html` (2026-09-08) | Primary; Blink WebGL2/ANGLE |
| Edge stable | 152.0.4191.62 (2026-09-02); major 151.0.4129.59 (2026-07-31) | `https://learn.microsoft.com/en-us/deployedge/microsoft-edge-relnote-stable-channel` | Same Blink, MS ANGLE/driver path — judges may use it |
| Firefox release | 155 (2026-09-01); 156 lands 2026-09-15 | `https://whattrainisitnow.com/calendar/` | Gecko native GL — different WebGL2 path; min 115/ESR |
| Firefox ESR | 140.15 (matches 155) | same | Fallback if release misbehaves |

Test each at 1080p, hardware accel on, viewport 1920×1080 dpr 1. Record Firefox separately — Gecko WebGL2 perf diverges and can flip the 60 FPS verdict.

## 8. Verdict

- Lock **Acer Aspire 7 A715-79G** (RTX 3050 6 GB, 144 Hz) as reference. Report every claim against it.
- Keep **Config A/B iGPU row** as compatibility floor; do not average into reference numbers.
- **WebGL2 hard requirement.** WebGPU = P6 research note only.
- All four claims stay UNVERIFIED until locked-machine + browser-matrix run logged.

UNVERIFIED: exact street prices at run time; ASUS M1605 7530U SKU on asus.com; Radeon 610M actual FPS (extrapolated from 2-CU spec, not measured); Firefox 155 latest patch build number.
