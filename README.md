# Sports Results

Use the following API to retrieve sports results and sort into table of results. Each sport result
contains several data and always includes the publication time.
Method: POST
Content-Type: application/json
Url: https://ancient-wood-1161.getsandbox.com:443/results
Tasks:

- Create python script that displays the api call.
  - `./run.sh -url https://ancient-wood-1161.getsandbox.com:443/results`
- ( OR ) Run without target to default to "https://ancient-wood-1161.getsandbox.com:443/results"
  - `./run.sh`
- Create python script that displays the sports results in reverse chronological order.
  - `./run.sh -chronological-reverse`
- Add a parameter to the script to display only certain types or events (e.g. f1Results)
  - `./run.sh -filer f1Results`
- Add a parameter to the script to display only certain types or events (e.g. f1Results or Tennis)
  - `./run.sh -filer f1Results,Tennis`
- Add a parameter to set the locale (e.g. en)
  - `./run.sh -url -set-locale en`
- How can you confirm the code works?
  - `./run.sh -t`
- [x] Bonus: Implement the rest call asynchronously

## How to run

Use the sctipt `run.sh` to create a virtual environment and install the required dependecies:

```bash
# chmod +x ./run.sh
$ ./run.sh -v -r
```

To change the name of the venv directory:

```bash
$ ./run.sh -v my-awesome-module
```

To change the name of the `pypi` requirements file:

```bash
$ ./run.sh -r my-awesome-requirements.txt
```

To change the default tests directory:

```bash
$ ./run.sh -t my-test-directory
```
