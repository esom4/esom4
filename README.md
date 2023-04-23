# Esom4
Esom4 is a tool that scrapes public genetic databases to find genetic mutations from an input file. This project can be used for academic research or clinical applications.

DISCLAIMER: This tool is developed for non-profit purposes only. Our goal is to help researchers and students in providing efficient and fast analysis exploiting open-source web-based information.

## Prerequisites
Before using Esom4, you will need to do the following:
1. Clone the repository to your local machine.
2. Install Python 3.x and the following packages (the script will prompt to install the missing ones):
- requests
- beautifulsoup4
- pandas
- selenium
- openpyxl
- tqdm
3. Install the Chrome driver. You can download it from [here](https://sites.google.com/chromium.org/driver/).
4. To use Franklin genoox database create a config.properties file with the following properties
```
[FRANKLIN]
USERNAME=<your_username>
PASSWORD=<your_password>
```
Replace `<your_username>` and `<your_password>` with your login credentials for the genetic database.
## How to use
1. Navigate to the project directory in your terminal.
2. Activate your virtual environment (optional).
3. Run the script `esoma.py` with the path to your input file as an argument:sh
```sh
python esoma.py -i /path/to/your/input/file.txt
```
4. The script will output a CSV file containing the results of the search, including the gene name, mutation type, and location.
## Supported databases
Esoma currently supports the following public genetic databases:
- [Franklin by genoox](https://franklin.genoox.com/clinical-db/home)
- [Omim](https://www.omim.org/)

## Contributing
Contributions to Esom4 are welcome! If you would like to contribute, please submit a pull request with your changes.

## License

```
Copyright 2023 esom4

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

For more information, please see the ```LICENSE``` file.
