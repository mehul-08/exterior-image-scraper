
import requests
import re
import html
import json
# import json
from datetime import date
import pprint
import requests
from bs4 import BeautifulSoup
import re
import html
import urllib3
import csv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_google_maps_html(url):
    cookies = {
        'AEC': 'AVh_V2hSxEizJ5HrF5flOvxglpwCys-jzje8OKGzHGQZgovcsvkWrC-9w7M',
        'NID': '525=XO8ZKAvNeNVGxFWoX5C5ojKOafrAklL2jMBqFfA1Em1zR_5-xM5aPCnyN4r9DxwNHtcxPngHmGecweM_-uJYA0Jejekwjuq0p_ocKHLsp9ublqdDTV-tI6lwjgD2CjQbYUkPq2tC0C-8pQN9YYwXQAB6a-hAyudRr4mXWiSqs6zkUMEfK1Qa5AcQ1cqonBafRN04tr-xvVu7ecRtMFy_e80meA9YaJJdSijNxVWkDxLpH2uvoK4b35VkhM0taSEjRg-u7G_Rp9aTDPC25g',
    }

    headers = {
        'Host': 'www.google.com',
        'Sec-Ch-Ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Service-Worker-Navigation-Preload': 'true',
        'X-Client-Data': 'CI31ygE=',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Priority': 'u=0, i',
    }

    params = {
        'entry': 'ttu',
        'g_ep': 'EgoyMDI1MDYyNi4wIKXMDSoASAFQAw==',
    }

    response = requests.get(url, params=params, cookies=cookies, headers=headers, verify=False)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    decoded = html.unescape(html_content)

    
        
        # Step 2: Get X-Event-Id
    event_id = response.headers.get("X-Event-Id")

    # Step 3: Save HTML
    html_content = response.text

        # Step 4: Decode and extract identifiers
    decoded = html.unescape(html_content)

        # Place ID: "!1s0x...:0x..."
    place_match = re.search(r"!1s(0x[0-9a-f]+):0x([0-9a-f]+)", decoded)
    place_id = place_id_2 = None
    if place_match:
            place_id = place_match.group(1)
            place_id_2 = "0x" + place_match.group(2)

        # gID from /g/ path
    g_match = re.search(r'"/g/([a-zA-Z0-9_]+)"', decoded)
    g_id = g_match.group(1) if g_match else None

    
    info = {"source_url": url}
    title_tag = soup.find("meta", property="og:title")
    if title_tag:
        parts = title_tag.get("content", "").split("\u00b7")
        info["name"] = parts[0].strip()
        if len(parts) > 1:
            info["location_address"] = parts[1].strip()

    tel_match = re.search(r'tel:(\+?\d{6,})', html_content)
    if tel_match:
        info["contact_number"] = tel_match.group(1)

    url_match = re.search(r'https://near-me\.hdfcbank\.com[^\s"\'<>\\]+', html_content)
    if url_match:
        decoded_url = html.unescape(url_match.group(0).replace("\\u003d", "=").replace("\\u0026", "&"))
        info["website_url"] = decoded_url


    return place_id, place_id_2, g_id, event_id,info

def extract_google_maps_identifiers(cid):
    """
    Extracts Google Maps identifiers (place ID parts, gID, X-Event-Id) from a CID-based request.
    Returns: place_id, place_id_2, g_id, event_id
    """
    params = {'cid': cid}

    cookies = {
        'AEC': 'AVh_V2g1k56iZlEuE3qFswn4DStEllPsxXNRaqStgqTlHRCk0ngfxbGxpt0',
        'NID': '525=neX51IQoH1DrOdNWsFsfNF5gt3INzbpxsQxk8381vgfgfEZ7jaoRIQq5GRIb2kNbxhlhVavpLTinN94fZNutpqy-m8hcxPPL5MYARkjKmeL-BEdhCMfKJI1JkFxRapfB4K0ZI3lMUUiGpiB90ZdbiruK5bMKwFpsoZzQk9XK03vTrxdNSIvyjNMXvUKWhdQZoT540Ok-n1YtX0rryV70VW8427UcRPpSW21jUfdh_RVRXvz0OQgAliKr52TsMQPk1yg',
    }

    headers = {
        'Host': 'www.google.com',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Ch-Ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Service-Worker-Navigation-Preload': 'true',
        'X-Client-Data': 'CI31ygE=',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=0, i',
        # 'Cookie': 'AEC=AVh_V2g1k56iZlEuE3qFswn4DStEllPsxXNRaqStgqTlHRCk0ngfxbGxpt0; NID=525=neX51IQoH1DrOdNWsFsfNF5gt3INzbpxsQxk8381vgfgfEZ7jaoRIQq5GRIb2kNbxhlhVavpLTinN94fZNutpqy-m8hcxPPL5MYARkjKmeL-BEdhCMfKJI1JkFxRapfB4K0ZI3lMUUiGpiB90ZdbiruK5bMKwFpsoZzQk9XK03vTrxdNSIvyjNMXvUKWhdQZoT540Ok-n1YtX0rryV70VW8427UcRPpSW21jUfdh_RVRXvz0OQgAliKr52TsMQPk1yg',
    }

    # Step 1: Request
    response = requests.get(
        "https://www.google.com/maps",
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False
    )
    # html_content = response.text
    decoded = html.unescape(html_content)

    # Step 2: Get X-Event-Id
    event_id = response.headers.get("X-Event-Id")

    # Step 3: Save HTML
    html_content = response.text

    # Step 4: Decode and extract identifiers
    decoded = html.unescape(html_content)

    # Place ID: "!1s0x...:0x..."
    place_match = re.search(r"!1s(0x[0-9a-f]+):0x([0-9a-f]+)", decoded)
    place_id = place_id_2 = None
    if place_match:
        place_id = place_match.group(1)
        place_id_2 = "0x" + place_match.group(2)

    # gID from /g/ path
    g_match = re.search(r'"/g/([a-zA-Z0-9_]+)"', decoded)
    g_id = g_match.group(1) if g_match else None

    soup = BeautifulSoup(html_content, "html.parser")
    info = {}
    title_tag = soup.find("meta", property="og:title")
    if title_tag:
        parts = title_tag.get("content", "").split("\u00b7")
        info["name"] = parts[0].strip()
        if len(parts) > 1:
            info["location_address"] = parts[1].strip()

    tel_match = re.search(r'tel:(\+?\d{6,})', html_content)
    if tel_match:
        info["contact_number"] = tel_match.group(1)

    url_match = re.search(r'https://near-me\.hdfcbank\.com[^\s"\'<>\\]+', html_content)
    if url_match:
        decoded_url = html.unescape(url_match.group(0).replace("\\u003d", "=").replace("\\u0026", "&"))
        info["website_url"] = decoded_url

    info["source_url"] = f"https://www.google.com/maps?cid={cid}"
    return place_id, place_id_2, g_id, event_id,info




def get_place_photos(cid_hex, cid_id, gid, session_id):
    cookies = {
        'AEC': 'AVh_V2g1k56iZlEuE3qFswn4DStEllPsxXNRaqStgqTlHRCk0ngfxbGxpt0',
        'NID': '525=neX51IQoH1DrOdNWsFsfNF5gt3INzbpxsQxk8381vgfgfEZ7jaoRIQq5GRIb2kNbxhlhVavpLTinN94fZNutpqy-m8hcxPPL5MYARkjKmeL-BEdhCMfKJI1JkFxRapfB4K0ZI3lMUUiGpiB90ZdbiruK5bMKwFpsoZzQk9XK03vTrxdNSIvyjNMXvUKWhdQZoT540Ok-n1YtX0rryV70VW8427UcRPpSW21jUfdh_RVRXvz0OQgAliKr52TsMQPk1yg',
    }

    headers = {
        'Host': 'www.google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
        'Accept': '*/*',
        'Referer': 'https://www.google.com/',
        'X-Maps-Diversion-Context-Bin': 'CAE=',
        'X-Client-Data': 'CI31ygE=',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    # Format the dynamic parts
    pb_value = f"!1e2!3m5!1s{cid_hex}%3A{cid_id}!9e0!15m2!1m1!4s%2Fg%2F{gid}!5m50!2m2!1i203!2i100!3m2!2i20!5b1!7m33!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!1m3!1e9!2b1!3e2!2b1!9b0!15m8!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20!6m3!1s{session_id}!7e81!15i16698!16m4!1m1!1BCgIYEw!2b1!4e1"

    # Final URL
    url = f"https://www.google.com/maps/rpc/photo/listentityphotos?authuser=0&hl=en&gl=in&pb={pb_value}"

    # Send request
    response = requests.get(url, headers=headers, cookies=cookies, verify=False)

    if response.ok:
        print("✅ Response received")
        html_file=response.text
        # print(html_file)# Print part of the response
    else:
        print("❌ Request failed:", response.status_code)
    return html_file



# import json

# import json

def find_date_recursive(obj):
    """
    Recursively search for a list like [YYYY, MM, DD] or [YYYY, MM, DD, HH] in nested structure.
    """
    if isinstance(obj, list):
        if (
            len(obj) in [3, 4] and
            all(isinstance(i, int) for i in obj) and
            2000 <= obj[0] <= 2100 and
            1 <= obj[1] <= 12 and
            1 <= obj[2] <= 31
        ):
            return obj  # Found a valid date
        for item in obj:
            result = find_date_recursive(item)
            if result:
                return result
    elif isinstance(obj, dict):
        for value in obj.values():
            result = find_date_recursive(value)
            if result:
                return result
    return None

def clean_google_photo_rpc(json_text):
    if json_text.startswith(")]}'"):
        json_text = json_text[5:]

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        return []

    if not data or not isinstance(data[0], list):
        return []

    results = []

    for item in data[0]:
        try:
            image_id = item[0]
            raw_url = item[6][0]
            image_url = raw_url.split('=')[0]
        except Exception:
            continue

        # 🔍 Dynamically search for date pattern in the item
        date_info = None
        try:
            date_list = find_date_recursive(item)
            if date_list and len(date_list) >= 3:
                y, m, d = date_list[:3]
                date_info = f"{y}-{int(m):02d}-{int(d):02d}"
        except Exception:
            date_info = None
        reporting_url= f"https://www.google.com/local/imagery/report/?cb_client=maps_sv.tactile&image_key=!1e10!2s{image_id}&hl=en&gl=in"
        results.append({
            "image_id": image_id,
            "image_url": image_url,
            "date": date_info,
            "reporting_url":reporting_url
        })

    return results

def lambda_handler(event, context):
    url = event.get("url")
    if not url:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'url' in request"})
        }

    try:
        place_id, place_id_2, g_id, session_id, info = fetch_google_maps_html(url)
        if not all([place_id, place_id_2, g_id, session_id]):
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Failed to extract identifiers"})
            }
        raw_json = get_place_photos(place_id, place_id_2, g_id, session_id)
        if not raw_json:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Failed to get photos"})
            }
        photo_urls = clean_google_photo_rpc(raw_json)
        info["exterior_images"] = photo_urls
        return {
            "statusCode": 200,
            "body": json.dumps(info)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


def fetch_photo_metadata(image_id):
    cookies = {
        'AEC': 'AVh_V2hSxEizJ5HrF5flOvxglpwCys-jzje8OKGzHGQZgovcsvkWrC-9w7M',
        'OTZ': '8152211_34_34__34_',
        'NID': '525=KkYxc4NCyL74yPWNUV0OING2i9szoQe0Dgs_q52o6xnhCn2ueyrEI0csWYUVcIfKH3D81lv3cDjdKKqdvbJC4zxg1HGM-es95PRXTKc7hPRkg58yklOhvR-xD9e6YbOSI7qjQRWcAbayuQfhSOwZ61khSKgk2Zh2Kt5Ug1KErEe3ghAF7CvvJgD7WqEiy7td1f3H-h7GJii_tUMju5Zlaif6dMPoOk53G6kMdamsQQ6HVUoo0W7QfGdknr0DiXIZlEq-CDp8',
    }

    headers = {
        'Host': 'www.google.com',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Ch-Ua': '"Not)A;Brand";v="8", "Chromium";v="138"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Sec-Ch-Ua-Mobile': '?0',
        'Accept': '*/*',
        'X-Client-Data': 'CI31ygE=',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.google.com/',
        'Priority': 'u=1, i',
    }

    url = (
        "https://www.google.com/maps/photometa/v1"
        "?authuser=0&hl=en&gl=in&pb="
        f"!1m4!1smaps_sv.tactile!11m2!2m1!1b1!2m2!1sen!2sin"
        f"!3m5!1m2!1e10!2s{image_id}!2m1!5s"
        "!4m61!1e1!1e2!1e3!1e4!1e5!1e6!1e8!1e12!1e17"
        "!2m1!1e1!4m1!1i48!5m1!1e1!5m1!1e2!6m1!1e1!6m1!1e2"
        "!9m36!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b1!3e2"
        "!1m3!1e3!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e1!2b0!3e3"
        "!1m3!1e4!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e3"
        "!11m2!3m1!4b1"
    )

    response = requests.get(url, cookies=cookies, headers=headers, verify=False)
    if not response.ok:
        return None

    text = response.text
    if text.startswith(")]}'"):
        text = text[5:]
    try:
        data = json.loads(text)
        contributor_raw = data[1][0][4][1][0]
        name = contributor_raw[0]
        profile_url = "https:" + contributor_raw[1]
        return {"name": name, "profile_url": profile_url}
    except Exception:
        return None


def main_5():
    urls = [
        "https://www.google.com/maps/place/HDFC+Bank/data=!4m7!3m6!1s0x390ce503a42c1b21:0x1441691481284de1!8m2!3d28.5439028!4d77.3333091!16s%2Fg%2F11jm94xdx6!19sChIJIRsspAPlDDkR4U0ogRRpQRQ?authuser=0&hl=en&rclk=1",

    ]

    with open("exterior_images_with_contributors.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "name", "location_address", "contact_number", "website_url", "source_url",
            "total_exterior_images",  # <-- NEW COLUMN
            "image_id", "image_url", "date", "reporting_url",
            "contributor_name", "contributor_profile"
        ])

        for url in urls:
            print(f"Processing: {url}")
            try:
                if "cid=" in url:
                    cid = re.search(r"cid=(\d+)", url).group(1)
                    place_id, place_id_2, g_id, session_id, info = extract_google_maps_identifiers(cid)
                else:
                    place_id, place_id_2, g_id, session_id, info = fetch_google_maps_html(url)

                if not all([place_id, place_id_2, g_id, session_id]):
                    raise ValueError("Missing identifiers")

                raw_json = get_place_photos(place_id, place_id_2, g_id, session_id)
                if not raw_json:
                    raise ValueError("No RPC photo response")

                photos = clean_google_photo_rpc(raw_json)
                if not photos:
                    writer.writerow([
                        info.get("name", ""), info.get("location_address", ""),
                        info.get("contact_number", ""), info.get("website_url", ""),
                        info.get("source_url", ""), "", "no exterior image found", "", "",
                        "", ""
                    ])
                    continue
                total_ext_images = len(photos)  # Count once
                for photo in photos:
                    contributor = fetch_photo_metadata(photo.get("image_id", ""))
                    writer.writerow([
                        info.get("name", ""),
                        info.get("location_address", ""),
                        info.get("contact_number", ""),
                        info.get("website_url", ""),
                        info.get("source_url", ""),
                        total_ext_images, 
                        photo.get("image_id", ""),
                        photo.get("image_url", ""),
                        photo.get("date", ""),
                        photo.get("reporting_url", ""),
                        contributor.get("name") if contributor else "",
                        contributor.get("profile_url") if contributor else ""
                    ])

            except Exception as e:
                print(f"Error processing {url}: {e}")
                writer.writerow(["error"] * 11)

    print("✅ Saved output to: exterior_images_with_contributors.csv")
def process_google_maps_url(url):
    """
    Takes a Google Maps URL and returns (info, exterior_photos) or None.
    """
    try:
        if "cid=" in url:
            cid_match = re.search(r"cid=(\d+)", url)
            if not cid_match:
                return None
            cid = cid_match.group(1)
            place_id, place_id_2, g_id, session_id, info = extract_google_maps_identifiers(cid)
        else:
            place_id, place_id_2, g_id, session_id, info = fetch_google_maps_html(url)

        if not all([place_id, place_id_2, g_id, session_id]):
            return None

        raw_json = get_place_photos(place_id, place_id_2, g_id, session_id)
        if not raw_json:
            return None

        photos = clean_google_photo_rpc(raw_json)
        if not photos:
            return info, []

        # Add contributor details to each photo
        for photo in photos:
            contributor = fetch_photo_metadata(photo.get("image_id", ""))
            if contributor:
                photo["contributor_name"] = contributor.get("name", "")
                photo["contributor_profile"] = contributor.get("profile_url", "")
            else:
                photo["contributor_name"] = ""
                photo["contributor_profile"] = ""

        return info, photos

    except Exception as e:
        print(f"Error: {e}")
        return None

def save_output(info: dict, photos: list, filename_base: str):
    """
    Save the output as JSON and CSV using the base filename (derived from place or CID).
    """
    json_path = f"{filename_base}.json"
    csv_path = f"{filename_base}.csv"

    # Save JSON
    full_data = info.copy()
    full_data["exterior_images"] = photos
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(full_data, jf, indent=2, ensure_ascii=False)

    # Save CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as cf:
        writer = csv.writer(cf)
        writer.writerow([
            "name", "location_address", "contact_number", "website_url", "source_url",
            "image_id", "image_url", "date", "reporting_url", "contributor_name", "contributor_profile"
        ])
        for photo in photos:
            writer.writerow([
                info.get("name", ""),
                info.get("location_address", ""),
                info.get("contact_number", ""),
                info.get("website_url", ""),
                info.get("source_url", ""),
                photo.get("image_id", ""),
                photo.get("image_url", ""),
                photo.get("date", ""),
                photo.get("reporting_url", ""),
                photo.get("contributor_name", ""),
                photo.get("contributor_profile", ""),
            ])
    print(f"✅ JSON saved: {json_path}")
    print(f"✅ CSV saved: {csv_path}")

if __name__ == "__main__":
    input_url = input("Enter Google Maps Place URL: ").strip()
    result = process_google_maps_url(input_url)
    if not result:
        print("❌ Failed to process the URL.")
    else:
        info, photos = result
        filename_base = info.get("name", "place").replace(" ", "_").replace("/", "_")
        save_output(info, photos, filename_base)



