import json
import requests
import re

def parse_option(opt):
    """Extracts header key and value from #EXTVLCOPT line."""
    m = re.match(r'#EXTVLCOPT:http-([^=]+)=(.*)', opt)
    if m:
        key = m.group(1).replace('-', '').title()
        value = m.group(2)
        return (key, value)
    return (None, None)

def load_channels_from_url(json_url):
    response = requests.get(json_url)
    response.raise_for_status()
    data = response.json()
    global_options = data.pop("GLOBAL_OPTIONS", [])
    return data, global_options

def get_headers(global_opts, channel_opts):
    """Returns the merged header string for a channel."""
    opts = channel_opts if channel_opts else global_opts
    headers = []
    for opt in opts:
        key, value = parse_option(opt)
        if key and value:
            headers.append(f"{key}={value}")
    return "|" + "|".join(headers) if headers else ""

def generate_m3u(channels, global_options, output_file, epg_url):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f'#EXTM3U url-tvg="{epg_url}"\n')
        for name, info in channels.items():
            group = info.get('group_title', '')
            tvg_id = info.get('tvg_id', '')
            tvg_logo = info.get('tvg_logo', '')
            stream_url = info.get('stream_url', '')
            options = info.get('options', None)
            if not stream_url:
                continue
            # Compose the EXTINF line
            extinf = (f'#EXTINF:-1 group-title="{group}" tvg-id="{tvg_id}" '
                      f'tvg-logo="{tvg_logo}",{name}\n')
            # Compose the stream URL line with headers
            headers = get_headers(global_options, options)
            stream = f"{stream_url}{headers}\n"
            f.write(extinf)
            f.write(stream)

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/nightah/daddylive/refs/heads/main/daddylive-channels-data.json"
    epg_url = "https://raw.githubusercontent.com/nightah/daddylive/refs/heads/main/epgs/daddylive-channels-epg.xml"  # Replace with your EPG XMLTV url
    channels, global_options = load_channels_from_url(url)
    generate_m3u(channels, global_options, "daddylive-channels.m3u", epg_url)
            if not stream_url:
                continue
            f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}" tvg-logo="{tvg_logo}" group-title="{group}",{name}\n')
            f.write(f"{stream_url}\n")

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/nightah/daddylive/refs/heads/main/daddylive-channels-data.json"
    channels = load_channels_from_url(url)
    epg_url = "https://raw.githubusercontent.com/nightah/daddylive/refs/heads/main/epgs/daddylive-channels-epg.xml"  # <-- Replace with your actual EPG XMLTV url
    generate_m3u(channels, "daddylive-channels.m3u", epg_url)
