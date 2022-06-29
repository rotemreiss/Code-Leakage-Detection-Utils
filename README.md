# Code-Leakage-Detection-Utils
Utils (mostly drafts) developed for code leakage detection.

---

<div align="center">
  
[npmsearch](#npmsearchpy) | [npm-secrets](#npm-secrets) | [dockerhub-secrets](#dockerhub-secrets)

</div>

---

## Tools Description
### npmsearch.py
Searches for public NPM pacakges that might have been leaked by mistake using built-in heuristics.

#### Prerequisites
- Python3

### npm-secrets
- Utilizes npmsearch.py to find public npm packages by a given keyword.
- Fetch the packages.
- Search for secrets.

#### Prerequisites
- Python3
- [Shhgit][1]

### dockerhub-secrets
- Search DockerHub for public images by a given keyword.
- Fetch the metadata and layers of the first and last tags of the found images.
- Analyzes the Docker image and searches for sensitive stuff that might have leaked (secrets, code and etc.)

#### Prerequisites
- Python3
- [Shhgit][1]


[1]: <https://github.com/eth0izzle/shhgit>
