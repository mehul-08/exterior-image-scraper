import os
import json
import csv
from google_maps_scraper import (
    fetch_google_maps_html,
    extract_google_maps_identifiers,
    get_place_photos,
    clean_google_photo_rpc,
    fetch_photo_metadata
)

def main():
    url = input("📍 Enter Google Maps URL: ").strip()
    if not url:
        print("❌ No URL provided.")
        return

    try:
        if "cid=" in url:
            cid = url.split("cid=")[-1].split("&")[0]
            place_id, place_id_2, g_id, session_id, info = extract_google_maps_identifiers(cid)
        else:
            place_id, place_id_2, g_id, session_id, info = fetch_google_maps_html(url)

        if not all([place_id, place_id_2, g_id, session_id]):
            print("❌ Missing required identifiers.")
            return

        print("🔍 Fetching photo list...")
        raw_json = get_place_photos(place_id, place_id_2, g_id, session_id)
        photos = clean_google_photo_rpc(raw_json)
        info["exterior_images"] = photos

        # Add contributor data
        for photo in info["exterior_images"]:
            contributor = fetch_photo_metadata(photo["image_id"])
            if contributor:
                photo["contributor_name"] = contributor["name"]
                photo["contributor_profile"] = contributor["profile_url"]

        # Save to files
        base_name = info["name"].replace(" ", "_")
        json_path = f"{base_name}.json"
        csv_path = f"{base_name}.csv"

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON saved to {json_path}")

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "image_id", "image_url", "date", "reporting_url",
                "contributor_name", "contributor_profile"
            ])
            for p in info["exterior_images"]:
                writer.writerow([
                    p.get("image_id", ""),
                    p.get("image_url", ""),
                    p.get("date", ""),
                    p.get("reporting_url", ""),
                    p.get("contributor_name", ""),
                    p.get("contributor_profile", "")
                ])
        print(f"✅ CSV saved to {csv_path}")

    except Exception as e:
        print("❌ Error:", str(e))


if __name__ == "__main__":
    main()
