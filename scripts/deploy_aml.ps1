param(
  [string]$Subscription,
  [string]$ResourceGroup,
  [string]$Workspace
)
az account set --subscription $Subscription
az extension add -n ml -y
az configure --defaults group=$ResourceGroup workspace=$Workspace
az ml job create -f ../azureml/job-train.yaml
az ml job create -f ../azureml/job-register-deploy.yaml
