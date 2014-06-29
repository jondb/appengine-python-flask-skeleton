PYTHONPATH=lib pip freeze > local_freeze.pip
pip freeze > system_freeze.pip
grep -v -f system_freeze.pip local_freeze.pip > requirements.txt
echo "Didn't include the following from system paths: "
echo `cat system_freeze.pip`
rm local_freeze.pip system_freeze.pip

