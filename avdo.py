import argparse
import time

from src.pipeline.stage import stage_0, stage_1, stage_2
from src.etc.dump import clear_damp
from src.etc.utils import GREEN, WHITE
from src.etc.output import output


if __name__ == "__main__":
    t0 = time.time()

    # Default values
    index_url_default = "https://data.oecd.org/searchresults/?hf=20&b=0&r=f%2Ftype%2Fdatasets%2Fapi+access&r=%2Bf%2Ftype%2Fdatasets%2Fapi+access&l=en&s=score"
    download_path = "../scrappersandcrowlers/oecd/downloads"
    max_pool_size_default = 10
    save_partial_results_default = False

    # Create argument parser
    parser = argparse.ArgumentParser(description="parallel crawler")

    # Define command-line arguments
    parser.add_argument("--index-url", default=index_url_default, type=str, help="Index URL")
    parser.add_argument("--download-path", default=download_path, type=str, help="Download path")
    parser.add_argument("--max-pool-size", type=int, default=max_pool_size_default, help="Maximum pool size. Default: 4")
    parser.add_argument("--save-partial-results", type=bool, default=save_partial_results_default, help="Save partial results. Default: false")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the argument values
    index_url = args.index_url
    max_pool_size = args.max_pool_size
    save_partial_results = args.save_partial_results
    download_path = args.download_path

    print(f"starting OECD crawler:\n\t- index url: {index_url}\n\t- parallel processes max pool size: {max_pool_size}\n\t- save partial results in yml files: {save_partial_results}")

    previews = stage_0(url=index_url, t0=t0)
    pages = stage_1(data=previews, t0=t0, max_pool=max_pool_size)
    out, fails = stage_2(data=pages, t0=t0, max_pool=max_pool_size, download_path=download_path)

    output(out, fails, 2)

    clear_damp()

    print(f"{GREEN}Done in {round(time.time() - t0, 2)}s {WHITE}")
