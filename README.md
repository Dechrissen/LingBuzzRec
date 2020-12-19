# buzzrec
 A content-based filtering recommendation engine for academic papers in linguistics from [LingBuzz](https://ling.auf.net/lingbuzz).

## Requirements

Python 3

## Installation

Download this repository with the green Code button, or

To download via `git`:
```cmd
 $ git clone https://github.com/Dechrissen/buzzrec.git
 ```
To install requirements, `cd` to the `buzzrec` directory, then:
```cmd
$ pip install -r requirements.txt
```

## Usage

### Initial setup
Populate `config.json` with the following information:
- your email address,
- keywords that define your interests (`buzzrec` will take these into consideration for its initial data collection).  

For example:
```json
{
  "email" : "john.smith@email.com",
  "keywords" : ["computational phonology", "context free grammars", "french"]
}
```

*Note*: Try to make your keywords more specific than 'phonology' or 'syntax', otherwise the initial data collection will take a while. Each keyword will make a new query to  LingBuzz; the narrower the term, the more specific the results.

### Using the tool

`cd` to the `buzzrec` directory, then:

```cmd
$ python recommender.py
```

The 10 most recent LingBuzz paper uploads will be compared against your specific tastes, and the most similar paper will be recommended to you along with a link to its PDF.

### Deleting a user model

To have `buzzrec` to recreate your user model according to new keywords in `config.json`, simply delete the `user.csv` file before running the tool. Otherwise, your user model will be saved for repeated use.
