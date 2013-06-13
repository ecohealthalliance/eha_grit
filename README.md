grit
====

requires libsvm
  
  brew install libsvm

requires scikit-learn

  pip install scikit-learn

example

  python run.py -training ProMED_master_clean.csv -classifier svm_standard -test ProMED_undiagnosed.csv 