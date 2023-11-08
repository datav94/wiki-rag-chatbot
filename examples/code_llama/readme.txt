## run the model locally
serve run llama_7b:gen_code_app

## Generate server config:yaml file for deployment

## To test the service locally, start the ray server locally

ray start --head

##deploy the service locally
serve deploy serve_llm_config.yaml
##Check the status 
serve status
