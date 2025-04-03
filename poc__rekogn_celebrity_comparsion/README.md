<img src="docs/img/ts_logo.png" alt="Diagram 1" width="80">

# Project: Celebrity Comparsion
This project is dedicated to comparing celebrity images to profile images stored either in S3 or locally within this repo. The project is utilizing AWS Rekognition to run the similarity comparsion between the two pictures.


## Setup Environment
Navigate into the project root:
```bash
cd poc__rekogn_celebrity_comparsion
```


Install dependencies via:
```bash
pipenv install
pipenv install -d
```


Set pythonpath:
```bash
export PYTHONPATH=$(pwd)
```


Add AWS Credentials:
```bash
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_SESSION_TOKEN=""
```


## Run Script
To run the script execute:
```bash
pipenv run pyhton3 src/main.py
```


## Results
The results are being written to: `./src/results/utput.json`.
Example:
```
{
    "Results": [
        {
            "Celebrity": "./data/celebrities/robert-deniro.jpeg",
            "Profile": "./data/profiles/maybe-robert-deniro-1.jpeg",
            "Similarity_Score": 99.84273529052734
        },
        {
            "Celebrity": "./data/celebrities/robert-deniro.jpeg",
            "Profile": "./data/profiles/maybe-robert-deniro-2.jpeg",
            "Similarity_Score": 98.18474578857422
        }
    ]
}
```


## Add More Images
Add more images for celebrities in `./data/celebrities/` and profiles in `./data/profiles/`. Add the file paths to the arrays in `src/main.py`.
