# Pricing Analysis — Vercel + Render

Cost breakdown for deploying the SIH-OCEAN platform on Vercel (frontend) + Render (backend).

---

## Cost Summary

### Testing / Development (Free Tier)

| Service | Plan | Cost | Limitations |
|---|---|---|---|
| Vercel (frontend) | Hobby | **$0** | 100 GB bandwidth, unlimited static sites |
| Render (backend) | Free | **$0** | 512 MB RAM, 0.1 CPU, spins down after 15 min idle |
| Render (disk) | — | **$0** | No persistent disk on Free tier |
| Cesium ion | Free | **$0** | Free tier includes terrain + imagery |
| **Total** | | **$0/month** | For testing only — no persistent data |

### Production / Demo (Recommended)

| Service | Plan | Cost | What you get |
|---|---|---|---|
| Vercel (frontend) | Hobby | **$0** | 100 GB bandwidth, CDN, preview deploys |
| Render (backend) | Starter | **$7/mo** | 512 MB RAM, 0.5 CPU, no spin-down |
| Render (disk) | 10 GB SSD | **$2.50/mo** | Persistent Zarr + SQLite + cache |
| Cesium ion | Free | **$0** | Terrain + imagery (free tier) |
| **Total** | | **$9.50/month** | Production-ready demo deployment |

### Scale (if needed for many users)

| Service | Plan | Cost | What you get |
|---|---|---|---|
| Vercel (frontend) | Pro | **$20/mo** | 1 TB bandwidth, team features |
| Render (backend) | Standard | **$25/mo** | 2 GB RAM, 1 CPU |
| Render (disk) | 50 GB SSD | **$12.50/mo** | More data storage |
| Cesium ion | Free | **$0** | (upgrade if exceeding tile quota) |
| **Total** | | **$57.50/month** | Handles hundreds of concurrent users |

---

## Vercel Pricing Detail

### Hobby (Free)
- **Bandwidth:** 100 GB/month
- **Build minutes:** 6000 min/month
- **Static sites:** Unlimited
- **Deploy frequency:** 100/day
- **Custom domains:** 1 per project
- **Preview deployments:** Yes (every PR)
- **Team members:** 1 (personal)

### Pro ($20/month)
- **Bandwidth:** 1 TB/month
- **Build minutes:** 24,000 min/month
- **Custom domains:** 10 per project
- **Team members:** Up to 40
- **Analytics:** Web analytics included
- **Edge functions:** Included

**For SIH-OCEAN:** Hobby (free) is sufficient. The frontend is a static SPA — no
server-side rendering needed. 100 GB bandwidth covers thousands of users loading the
Cesium app + assets.

---

## Render Pricing Detail

### Free ($0/month)
- **RAM:** 512 MB
- **CPU:** 0.1
- **Spins down:** After 15 min inactivity (30s cold start)
- **Instance hours:** 750/month (~31 days 24/7)
- **Persistent disk:** No
- **Custom domains:** No

### Starter ($7/month)
- **RAM:** 512 MB
- **CPU:** 0.5
- **Spins down:** No (always on)
- **Instance hours:** Unlimited
- **Persistent disk:** Yes ($0.25/GB/month)
- **Custom domains:** Yes

### Standard ($25/month)
- **RAM:** 2 GB
- **CPU:** 1
- **Spins down:** No
- **Persistent disk:** Yes
- **Custom domains:** Yes
- **Zero-downtime deploys:** Yes

### Pro ($85/month)
- **RAM:** 4 GB
- **CPU:** 2
- **Persistent disk:** Yes

### Persistent Disks
- **Cost:** $0.25/GB/month
- **Min size:** 1 GB
- **Max size:** Varies by plan
- **Snapshots:** Daily, included
- **Note:** Can only increase size, not decrease. Pick smallest that works.

**For SIH-OCEAN:**
- Starter ($7) + 10 GB disk ($2.50) = **$9.50/month** for the demo
- Upgrade to Standard ($25) if isosurface compute is slow on 0.5 CPU
- 10 GB disk holds: ~5 GLORYS variables × Indian Ocean subset × 1 month ≈ 2 GB Zarr,
  plus SQLite (~500 MB), plus cache (~2 GB) = ~5 GB used

---

## Cesium ion Pricing

### Free Tier
- **Terrain:** Cesium World Terrain (global, streamed)
- **Imagery:** Bing Maps Aerial (Cesium ion asset)
- **Asset storage:** 5 GB
- **Monthly tile requests:** Generous free tier (not publicly specified, but
  sufficient for a demo with hundreds of users)
- **Cost:** $0

### Paid Tiers
- **Developer:** $99/month (higher quotas, commercial use)
- **Premium:** Custom pricing

**For SIH-OCEAN:** Free tier is sufficient for the SIH demo. The app uses Cesium ion
for terrain + imagery only — the ocean data comes from our own Zarr store on Render.

---

## Hidden Costs to Watch

| Cost | When | Mitigation |
|---|---|---|
| Render bandwidth overage | If backend serves lots of Zarr chunks | Cache chunks at CDN level; use compressed Zarr |
| Vercel bandwidth overage | If >100 GB/month (many users) | Upgrade to Pro ($20/mo) for 1 TB |
| Cesium ion quota | If many users hit terrain/imagery tiles | Self-host terrain tiles (GEBCO) to reduce ion calls |
| Render disk expansion | As data grows | Start small (10 GB), expand as needed |
| Copernicus data | Free for research; may need license for production | Check Copernicus Marine license |

---

## Recommendation

**For the SIH demo/presentation:**
```
Vercel Hobby (free) + Render Starter ($7) + 10 GB disk ($2.50) = $9.50/month
```

This gives you:
- A fast, CDN-served frontend on Vercel (free)
- An always-on backend on Render with persistent data ($9.50/mo)
- Cesium ion terrain + imagery (free)
- Custom domain support (Render Starter includes it)

**For scaling to many users:**
```
Vercel Pro ($20) + Render Standard ($25) + 50 GB disk ($12.50) = $57.50/month
```

**For testing only:**
```
Vercel Hobby (free) + Render Free ($0) = $0/month
```
(No persistent data — re-upload on each deploy. Backend spins down after 15 min.)
