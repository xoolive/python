import requests
from tqdm.autonotebook import tqdm
from io import BytesIO


url = "https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh"
response = requests.get(url, stream=True)
total_size = int(response.headers.get("Content-Length", 0))
block_size = 4096
b = BytesIO()

with tqdm(
    total=total_size, unit="B", unit_scale=True, unit_divisor=1024
) as pbar:
    for data in response.iter_content(block_size):
        pbar.update(len(data))
        b.write(data)
