# Sports Results

Use the following API to retrieve sports results and sort into table of results. Each sport result
contains several data and always includes the publication time.
Method: POST
Content-Type: application/json
Url: https://ancient-wood-1161.getsandbox.com:443/results
Tasks:

- Create python script that displays the sports results in reverse chronological order.
- Add a parameter to the script to display only certain types or events (e.g. f1Results)
- Add a parameter to set the locale (e.g. en)
- How can you confirm the code works?
- Bonus: Implement the rest call asynchronously

## How to run

Use the sctipt `setup.sh` to create a virtual environment and install the required dependecies:

```bash
# chmod +x ./setup.sh
$ ./setup.sh
```

python3 -m venv /path/to/new/virtual/environment
