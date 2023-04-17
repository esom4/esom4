# Esom4
Esom4 is a tool that scrapes public genetic databases to find genetic mutations from an input file. This project can be used for academic research or clinical applications.
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
4. Create a keystore.properties file with the following properties:makefile
```makefile
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
## Contributing
Contributions to Esoma are welcome! If you would like to contribute, please submit a pull request with your changes.
## License
Esoma is released under the MIT License, which allows you to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, subject to the following conditions:
- The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please see the ```LICENSE``` file.
