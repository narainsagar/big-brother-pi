#!/bin/bash
touch ~/.bash_profile
echo "please enter the company ID"
read -r companyID

echo "Setting Environment Variable COMPANY_ID"
echo "export COMPANY_ID="$companyID >> ~/.bash_profile
echo "COMPANY_ID Set"