import argparse
import requests
import json


def search_npm(query):
    DEFAULT_SEARCH_SIZE = 250

    packages = []
    results_offset = 0
    has_more_pages = True

    try:
        while has_more_pages:
            search_url = f"https://registry.npmjs.org/-/v1/search?text={query}&from={results_offset}&size={DEFAULT_SEARCH_SIZE}"

            resp = requests.get(url=search_url).json()
            packages.extend(resp["objects"])

            # Check if there are any more pages.
            results_offset = results_offset + DEFAULT_SEARCH_SIZE
            has_more_pages = results_offset < resp["total"]

    except Exception as e:
        print(f'Something went wrong: {e}')

    return packages


def get_npm_package_repo_url(package_name):
    npm_api_url = f"https://registry.npmjs.org/{package_name}"

    resp = requests.get(url=npm_api_url).json()
    if "repository" in resp and "url" in resp["repository"]:
        return resp["repository"]["url"]

    return ""


def npm_get_package_heuristics_result(package):
    """
    Reduce noise with some heuristics.
    :param package:
    :return:
    """
    repo_url = get_npm_package_repo_url(package["package"]["name"])
    if is_github_repo_private(repo_url):
        return True

    return False


def get_npm_package_names(packages, is_heuristics_enabled):
    names = []
    for package in packages:

        if not is_heuristics_enabled or (is_heuristics_enabled and npm_get_package_heuristics_result(package)):
            names.append(package["package"]["name"])

    return names


def is_github_repo_private(repo_url):
    repo_url_clean = repo_url.lstrip("git+")
    if not repo_url_clean.startswith("https://github.com"):
        return False

    resp = requests.get(url=repo_url_clean)
    return resp.status_code != 200


def main(**kwargs):
    npm_packages = search_npm(kwargs["query"])
    npm_package_names = get_npm_package_names(npm_packages, kwargs["heuristics"])
    if not kwargs["silent"]:
        print("Found " + str(len(npm_packages)) + " results")

        if kwargs["heuristics"]:
            print("Found " + str(len(npm_package_names)) + " results after heuristics engine.")

    for name in npm_package_names:
        print(name)


def interactive():
    parser = argparse.ArgumentParser(description="Search for public NPM packages that might have been leaked.")

    # Add the arguments.
    parser.add_argument('-s', '--silent', help='Print only the results', dest='silent', action='store_true')
    parser.add_argument('-q', '--query', help='Search query', dest='query', required=True)
    parser.add_argument('-he', '--heuristics-enabled', help='Heuristics mode enabled for noise reduction',
                        dest='heuristics',
                        action='store_true')
    args = parser.parse_args()

    main(query=args.query, silent=args.silent, heuristics=args.heuristics)


if __name__ == '__main__':
    interactive()
