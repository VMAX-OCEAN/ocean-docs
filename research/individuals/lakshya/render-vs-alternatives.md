# Render vs Alternatives — Backend Hosting Comparison

Why Render is the best choice for the SIH-OCEAN backend, compared to alternatives.

---

## Comparison Matrix

| Platform | Persistent Disk | Python/Docker | Long-running | Cost (entry) | CORS | Custom Domain | Auto-deploy |
|---|---|---|---|---|---|---|---|
| **Render** | Yes (SSD, $0.25/GB) | Python + Docker | Yes (always-on on paid) | $7/mo | Manual config | Yes (paid) | Yes (Git) |
| Railway | Yes (volumes) | Docker | Yes | $5/mo (usage-based) | Manual config | Yes | Yes (Git) |
| Fly.io | Yes (volumes) | Docker | Yes | $0 (free tier) | Manual config | Yes | Yes (CLI/Git) |
| Heroku | Yes (dynos) | Python + Docker | Yes | $5/mo (eco) | Manual config | Yes (paid) | Yes (Git) |
| Vercel (serverless) | No | Python (serverless) | No (10-60s timeout) | $0 | Manual config | Yes | Yes (Git) |
| AWS EC2 | Yes (EBS) | Anything | Yes | $3-10/mo | Manual config | Yes | Manual |
| DigitalOcean | Yes (volumes) | Docker | Yes | $4/mo (droplet) | Manual config | Yes | Yes (apps) |

---

## Render (Recommended)

### Pros
- **Persistent disk** — SSD, $0.25/GB, survives deploys. Perfect for Zarr + SQLite.
- **Native Python runtime** — no Docker needed for basic FastAPI
- **Docker support** — if PyVista/VTK needs system deps
- **`render.yaml` Blueprint** — Infrastructure as Code, one-click deploy
- **Always-on** on Starter plan ($7/mo) — no spin-down
- **Health checks** — built-in, auto-restart on failure
- **Git-based** — push to GitHub → auto-deploy
- **Simple** — much simpler than AWS/GCP for a small project

### Cons
- **No autoscaling** with persistent disk (single instance only)
- **No zero-downtime deploy** with persistent disk
- **Starter plan** has only 512 MB RAM (may be tight for xarray + PyVista)
- **No built-in CDN** for Zarr chunks (would need Cloudflare in front)

### Verdict
**Best for SIH-OCEAN.** The persistent disk is the killer feature — Zarr data and
SQLite survive deploys without external storage. The `render.yaml` Blueprint makes
deployment reproducible. Starter plan ($7/mo) is affordable for a demo.

---

## Railway

### Pros
- **Usage-based pricing** — pay only for what you use (good for low-traffic)
- **Volumes** — persistent storage (similar to Render disks)
- **Docker** — full control
- **Simple** — comparable to Render in UX
- **Free trial** — $5 credit to start

### Cons
- **No native Python runtime** — Docker only
- **Usage-based can be unpredictable** — costs scale with traffic
- **Smaller community** than Render
- **No Blueprint** — no Infrastructure as Code equivalent

### Verdict
Good alternative if you want usage-based pricing. But Render's `render.yaml` Blueprint
and native Python runtime are better for our case.

---

## Fly.io

### Pros
- **Free tier** — 3 shared-cpu VMs, 3 GB storage
- **Global regions** — deploy close to users
- **Volumes** — persistent storage
- **Docker** — full control
- **CLI-first** — good developer experience

### Cons
- **Docker only** — no native Python runtime
- **More complex** than Render (need to write Dockerfile, fly.toml)
- **Free tier limited** — shared CPU, may not handle xarray well
- **No Blueprint** — manual configuration

### Verdict
Good if you want free tier + global regions. But Docker-only and more complex setup.
Render is simpler.

---

## Heroku

### Pros
- **Mature** — oldest PaaS, well-documented
- **Native Python** — buildpacks handle everything
- **Add-ons** — Postgres, Redis, etc.

### Cons
- **Expensive** — Eco ($5/mo) gives limited dyno hours; Basic ($7/mo) per dyno
- **No free tier** anymore (ended 2022)
- **Ephemeral filesystem** — need S3 for persistent data (no disk)
- **Limited** compared to Render for the same price

### Verdict
Heroku killed its free tier and is more expensive than Render for the same features.
Render is the better choice in 2025.

---

## Vercel Serverless (for backend)

### Pros
- **Same platform as frontend** — single dashboard
- **Free tier** — 100 GB bandwidth
- **Edge functions** — fast cold regions

### Cons
- **10-60s timeout** — too short for marching cubes isosurface compute
- **No persistent disk** — SQLite/Zarr data lost between invocations
- **Cold starts** — every serverless function invocation may cold-start
- **Not designed for long-running Python** — xarray lazy loading doesn't work well
- **Memory limit** — 1024 MB on free tier (may be tight)

### Verdict
**Not suitable for our backend.** The serverless model doesn't work for a long-running
Python process with persistent data. This is why we split: Vercel for frontend, Render
for backend.

---

## AWS / GCP / Azure

### Pros
- **Full control** — any configuration possible
- **Cheapest at scale** — EC2 spot instances, S3 storage
- **CDN** — CloudFront/Cloudflare in front

### Cons
- **Complex** — VPC, security groups, IAM, load balancers, etc.
- **Time-consuming** — setup takes hours vs minutes on Render
- **No Blueprint** — Terraform/CloudFormation needed
- **Overkill** for a SIH demo

### Verdict
Overkill for the SIH demo. If the platform needs to scale to thousands of users
post-SIH, migrate to AWS with S3 for Zarr + EC2 for backend + CloudFront for CDN.

---

## Final Recommendation

```
Frontend: Vercel (free, CDN, preview deployments)
Backend:  Render Starter ($7/mo + $2.50/mo disk)
Data:     Render persistent disk (Zarr + SQLite)
```

**Total: $9.50/month** for a production-ready, persistent-data, auto-deploying
deployment with custom domain support.

**Why not all-Render?** Vercel's edge CDN is faster for the Cesium static assets
(Workers, Assets, Widgets — ~8 MB cached for 1 year). Vercel's preview deployments
(every PR gets a URL) are better for iterative development.

**Why not all-Vercel?** Vercel serverless can't run a persistent Python backend with
disk storage. Render's web service + persistent disk is the right tool for that job.
