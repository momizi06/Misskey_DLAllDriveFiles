# Misskey_DLAllDriveFiles

## Requirement
- Python 3.8+ (Recommend: 3.12)
- [Requests](https://pypi.org/project/requests/)
- Internet Connection

## Install
### 1. Install Requests package
`pip install requests`

### 2. Get your Misskey server API key
You can get API key (a.k.a. Access Token) from `<Your Misskey server URL>/settings/api`.  
e.g. `https://misskey.io/settings/api`

Your API key needs "Access your Drive files and folders" permission.

### 3. Run getAllFiles.py
getAllFiles.py generates json file that include your Drive files informations.

To run it, `python getAllFiles.py <server_url> <token> <save_dir>`.
e.g. `python getAllFiles.py 'https://misskey.io' 'qaW1seD2fRgtuhu566hijo' path/to/save`

### 4. Run dlAllFiles.py
dlAllFiles.py downloads Drive files describe by json file. It would be take a long time to download.

json files can generate from previous section.

To run it, `python dlAllFiles.py <info_dir> <save_dir>`.
e.g. `python dlAllFiles.py path/to/info path/to/savefiles`

You have to same path to save_dir that sets previous section.
