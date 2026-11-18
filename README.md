# The World in One Day — 18 November 2026

[![news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Ahmadmukafi/news-image-20261118-r2/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Ahmadmukafi/news-image-20261118-r2/reward.svg)](https://make.fun/bounty/news-image-20261118)

A magazine-cover front page summing up the world's news of Wednesday
18 November 2026, drawn from scratch with Python PIL. The cover leads
with a drawn night map of the Gulf — the day's dominant story — above
a three-column grid of the other big stories and a markets ticker.

## The day

- **The Gulf ignites.** American jets hit a missile site on Qeshm
  Island; Iran's drones struck U.S. radar sites in Bahrain and Kuwait
  — the third attack there in a week.
- **Crimea bridge falls.** Ukraine hits the Kerch bridge a second day;
  part of its road span falls into the strait. Russia hits two bridges
  in Kyiv, cutting water and heat.
- **Democrats take 56.** Peltola wins Alaska's Senate seat, giving
  Democrats 56 seats in the U.S. Senate.
- **Ebola doubles.** The DR Congo outbreak passes 11,000 cases and
  5,400 deaths — more than double in three months, the UN says.
- **Markets slide.** S&P 500 7,340.53 (−1.03%), Nasdaq 24,328.38
  (−0.74%), Nikkei 59,024.28 (+0.28%), Brent $91.55 (−1.71%),
  Gold $3,775 (−2.31%).

Also: Cyclone Xavier hits the Cook Islands, a Russian military plane
crash kills 19, and a 6.0 quake strikes Papua New Guinea.

## How it is made

`main.ts` runs `draw.py`, which draws the 1024×1024 front page with
PIL (DejaVu fonts) and writes `entry.png`. No network is used at
runtime, and running it twice produces identical bytes.

```
node main.ts
```
