import json
import requests

def load_channels_from_url(json_url):
    response = requests.get(json_url)
    response.raise_for_status()
    data = response.json()
    data.pop("GLOBAL_OPTIONS", None)
    return data

def generate_m3u(channels, output_file, epg_url=None):
    # Always write the EPG url-tvg to the header, even if epg_url is None (can be empty string)
    if epg_url is None:
        epg_url = "https://example.com/your-epg.xml"  # <-- Replace with your actual EPG XMLTV url
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f'#EXTM3U url-tvg="{epg_url}"\n')
        for name, info in channels.items():
            tvg_id = info.get('tvg_id', '')
            tvg_logo = info.get('tvg_logo', '')
            group = info.get('group_title', '')
            stream_url = info.get('stream_url', '')
            if not stream_url:
                continue
            f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}" tvg-logo="{tvg_logo}" group-title="{group}",{name}\n')
            f.write(f"{stream_url}\n")

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/nightah/daddylive/refs/heads/main/daddylive-channels-data.json"
    channels = load_channels_from_url(url)
    epg_url = "https://example.com/your-epg.xml"  # <-- Replace with your actual EPG XMLTV url
    generate_m3u(channels, "daddylive-channels.m3u", epg_url)
