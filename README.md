# SideProject-CurrencyConverter

## About The Project

Implement currency converter apis to get exchange rate from visa, mastercard, and mid-market.
FastApi and GoogleAppEngine are used in this repository.

## Getting Started
### Prerequisites
To setup the environment, install `pipenv` by running the following script (if you use Mac). For other devices, the instruction is in the [link](https://github.com/pypa/pipenv).
```shell
  brew install pipenv
```

#### Setup visa service
To access visa APIs, implement the following steps, and make sure to record the `API Key` and `Shared Secret`.

1. Sign up for visa developer account api through [official website](https://developer.visa.com/) to access APIs.

2. Go to [dashboard](https://developer.visa.com/portal/app/dashboard) and create new project.

3. In the summary page, click "Add API's" button on the top-right corner, and select API `Foreign Exchange Rates API`

4. In the credentials page, scroll down to the section `X-Pay Token` and generate new X-Pay Credentials.

5. Record the `API Key` and `Shared Secret`.

#### Setup mastercard service
To access mastercard APIs, implement the following steps, and make sure to record the `Private Key` and `Consumer Key`.

1. Sign up for mastercard developer account api through [official website](https://developer.mastercard.com/) to access APIs.

2. Go to [dashboard](https://developer.mastercard.com/dashboard) and create new project.

3. Select API `Standard Currency Conversion Calculator`, and download PKCS#12 Keystore file, which includes the extension `.p12`.

4. Use the following codes to get the `Private Key`.
```python
MASTERCARD_OPENSSL_KEY = <P12_FILEPATH>
MASTERCARD_OPENSSL_PASSWORD = <PASSWORD>  # default: keystorepassword
MASTERCARD_PKCS12 = OpenSSL.crypto.load_pkcs12(
    open(MASTERCARD_OPENSSL_KEY, "rb").read(),
    MASTERCARD_OPENSSL_PASSWORD,
)
PRIVATE_KEY = MASTERCARD_PKCS12.get_privatekey()
DUMP_KEY = OpenSSL.crypto.dump_privatekey(
    OpenSSL.crypto.FILETYPE_PEM, PRIVATE_KEY,
)
```

5. In the sandbox page, you can see your `Consumer Key` generate with the keystore password and keyalias you just get.

6. Record the private key and consumer key.

#### Setup google app engine (optional)
To access [google cloud service](https://cloud.google.com/sdk/gcloud), implement the following steps.

1. Download gcloud-cli install package based on device's platform from https://cloud.google.com/sdk/docs/install

2. Extract the archive by opening the downloaded `.tar.gz` archive file directly.

3. Run the following script to install `google-cloud-sdk`.
```shell
./google-cloud-sdk/install.sh
```

4. Run the following script to initialize the gcloud CLI.
```shell
gcloud init
```

5. Link the project where to deploy the server.
```shell
gcloud config set project <PROJECT_ID>
```

### Installation
To create the environment, run the following script from the root of your project’s directory (where it includes the file `pipfile.lock`).
```shell
  pipenv install
```

To activate the environment, run the following script from the root of your project’s directory (where it includes the file `pipfile.lock`).
```shell
  pipenv shell
```

To run it on google app engine, run the following script to create `requirements.txt`.
```shell
  pipenv lock -r
```

## Usage
### Local Server
1. To select a deploy environment, run the following script in pipenv.
```bash
export ENVIRONMENT=development
export ENVIRONMENT=production
```

2. To set necessary environment variables, run the following scripts in pipenv.
```shell
# Visa API Configs
export VISA_API_KEY="visa-api-key"
export VISA_SHARED_SECRET="visa-shared-secret"

# Mastercard API Configs
export MASTERCARD_PRIVATE_KEY="mastercard-private-key"
export MASTERCARD_CONSUMER_KEY"mastercard-consumer-key"
```

3. To deploy the server, run the following scripts from the root of your project’s directory (where it includes the file `main.py`).
```shell
uvicorn main:app --reload
```

### Google App Engine
1. To select a deploy environment and set necessary environment variables, add `env.yaml` under from the root of your project’s directory (where it includes the file `app.yaml`).
```yaml
env_variables:
  ENVIRONMENT: production

  # Visa API Configs
  VISA_API_KEY: visa-api-key
  VISA_SHARED_SECRET: visa-shared-secret

  # Mastercard API Configs
  MASTERCARD_PRIVATE_KEY: mastercard-private-key
  MASTERCARD_CONSUMER_KEY: mastercard-consumer-key
```

2. To deploy on the app engine, run the following scripts from the root of your project’s directory (where it includes the file `app.yaml`).
```shell
gcloud app deploy
```

## Authors
Scarlett Tseng

## License
Theis is released under the under terms of the  [MIT License](https://github.com/tseng1026/SideProject-CurrencyConverter/blob/master/LICENSE) .

## FAQ
### Problem: I can run on my local machine, but fail to deploy on app engine.
1. Install the gunicorn by running the following script.
```shell
pip install gunicorn
```

2. Generate the `requirements.txt` by running the following script. Note that `Pipfile` and `Pipfile.lock` is not accepted.
```shell
  pipenv lock -r
```

3. Set configure in `app.yaml` with the following configs.
```yaml
runtime: python39
entrypoint: gunicorn -w=2 -k=uvicorn.workers.UvicornWorker --bind=0.0.0.0:8080 main:app
env_variables:
  ENVIRONMENT: production
includes:
  - env.yaml
```

4. Set configure in `env.yaml` with the following configs.
```yaml
env_variables:
  # Visa API Configs
  VISA_API_KEY: visa-api-key
  VISA_SHARED_SECRET: visa-shared-secret

  # Mastercard API Configs
  MASTERCARD_PRIVATE_KEY: mastercard-private-key
  MASTERCARD_CONSUMER_KEY: mastercard-consumer-key
```

5. Setup `.gcloudignore` to avoid uploading unnecessary files, especially the following files.
```
.gcloudignore
.git
.gitignore
Pipfile
Pipfile.lock
```
