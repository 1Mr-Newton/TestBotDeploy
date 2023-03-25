import argparse
import requests
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Download a file with progress')
parser.add_argument('--url', help='URL of the file to download', required=True)
parser.add_argument(
    '--filename', help='Name of the file to save as', required=True)
args = parser.parse_args()

url = args.url
filename = args.filename

response = requests.get(url, stream=True)

total_size = int(response.headers.get('content-length', 0))
block_size = 1024  # 1 Kibibyte

progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
with open(filename, 'wb') as file:
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        file.write(data)

progress_bar.close()

if total_size != 0 and progress_bar.n != total_size:
    print("ERROR, something went wrong while downloading!")
else:
    print("Downloaded successfully!")
