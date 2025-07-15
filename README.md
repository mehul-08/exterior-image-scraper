# 🛰️ Google Maps Exterior Image Scraper

This Python tool extracts **exterior images and metadata** (image IDs, URLs, dates, contributors, etc.) from a **Google Maps Place URL** and outputs both `.json` and `.csv` formats.

---

## 🚀 Features

- Extracts:
  - Place name, address, phone number, website
  - Image ID, URL, date
  - Reporting link
  - Contributor name and profile (if available)
- Supports both **CID-based** and **place-based** Google Maps URLs
- Outputs:
  - `place_name.json`
  - `place_name.csv`

---

## 📦 Installation

```bash
pip install -r requirements.txt
