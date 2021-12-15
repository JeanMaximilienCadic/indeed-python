
<h1 align="center">
  <br>
  <a href="https://drive.google.com/uc?id=1G7-wQtubqNCrpKrLkQrs4NSSxqmb13U2"><img src="https://drive.google.com/uc?id=1G7-wQtubqNCrpKrLkQrs4NSSxqmb13U2" alt="IDGraph" width="200"></a>
  <br>
  INDEED
  <br>
</h1>

<p align="center">
  <a href="#code-structure">Code</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#docker">Docker</a> •

[comment]: <> (  <a href="#notebook">Notebook </a> •)
</p>


### Code structure
```python
from setuptools import setup
from indeed import __version__

setup(
    name="indeed",
    version=__version__,
    short_description="indeed",
    long_description="indeed",
    packages=[
        "indeed",
        "indeed.core",
        "indeed.tests",
        "indeed.models",
    ],
    include_package_data=True,
    package_data={'': ['*.yml']},
    url='https://cadic.jp',
    license='MIT',
    author='CADIC Jean-Maximilien',
    python_requires='>=3.8',
    install_requires=[r.rsplit()[0] for r in open("requirements.txt")],
    author_email='me@cadic.jp',
    description='indeed',
    platforms="linux_debian_10_x86_64",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: CMJ License",
    ]
)

```
### Configuration file
```yaml
features:
  cat   : ["companyId", "jobType", "degree", "major", "industry"]
  num   : ["yearsExperience", "milesFromMetropolis"]
  y     : ["salary"]
  best  : ['companyId', 'degree', 'industry', 'jobType', 'major', 'milesFromMetropolis', 'yearsExperience']

etl:
  xtrain_csv  : "filestore/landing/train/train_features.csv"
  ytrain_csv  : "filestore/landing/train/train_salaries.csv"
  output_csv  : "filestore/gold/indeed_training_data.csv"
  x:
    mu:
      companyId           : 31.027123
      jobType             : 3.50532
      degree              : 2.061605
      major               : 2.581721
      industry            : 2.998658
      yearsExperience     : 11.992386
      milesFromMetropolis : 49.52926
    std:
      companyId           : 18.20198897525415
      jobType             : 2.2918099724874548
      degree              : 1.4343423166430256
      major               : 2.3988183408687767
      industry            : 1.9995544996959191
      yearsExperience     : 7.212390868885715
      milesFromMetropolis : 28.877732628720043
  y:
    mu  : 116.06182
    std : 38.71794


models:
  regression_tree :
    max_depth: 13

```

### How to use
To clone and run this application, you'll need [Git](https://git-scm.com) and [ https://docs.docker.com/docker-for-mac/install/]( https://docs.docker.com/docker-for-mac/install/) and Python installed on your computer. 
From your command line:

Install the package:
```bash
# Unzip the zip file
unzip indeed.zip

# Go into the repository
cd indeed
```

Run the exploration:
```shell
python -m indeed.core
```

You should be able to get some similar output
```shell
Grid processing: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1000/1000 [04:57<00:00,  3.36it/s]
+-----+-------------+---------------------------------------------------------------------------------------------------+----------+
|     |   max_depth | features                                                                                          |    score |
+=====+=============+===================================================================================================+==========+
| 834 |          13 | ['companyId', 'degree', 'industry', 'jobType', 'major', 'milesFromMetropolis', 'yearsExperience'] | 0.723503 |
+-----+-------------+---------------------------------------------------------------------------------------------------+----------+
| 838 |          13 | ['companyId', 'degree', 'industry', 'jobType', 'major', 'milesFromMetropolis', 'yearsExperience'] | 0.723488 |
+-----+-------------+---------------------------------------------------------------------------------------------------+----------+
| 614 |          14 | ['companyId', 'degree', 'industry', 'jobType', 'major', 'milesFromMetropolis', 'yearsExperience'] | 0.723127 |
+-----+-------------+---------------------------------------------------------------------------------------------------+----------+
| 618 |          14 | ['companyId', 'degree', 'industry', 'jobType', 'major', 'milesFromMetropolis', 'yearsExperience'] | 0.723108 |
+-----+-------------+---------------------------------------------------------------------------------------------------+----------+
| 836 |          13 | ['companyId', 'industry', 'jobType', 'major', 'milesFromMetropolis', 'yearsExperience']           | 0.722435 |
+-----+-------------+---------------------------------------------------------------------------------------------------+----------+

```


### Docker
```shell
cd scripts && ./build && ./docker
```
