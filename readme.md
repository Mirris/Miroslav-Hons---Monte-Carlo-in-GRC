# Sample of Monte Carlo simulation within GRC

This scipt has been created to support original assumptions of author to demonstrate probability calculations of Key Risk Indicators crystalizing from process innovations. Sampled code represents loans assets distribution in banking industry, while evaluating two competitive offers of process innovations.
* First part of code is dedicated to search for mean and standard deviation in estimating single loan probability of operating success or failure.
* Second part of code uses probability of operational success and runs a 3 year performance simulation. Simuation is finalised with provided estimates on assets throughput distribution of each proposed innovation model.

## Getting Started

Following instructions will let you know how to run and modify the code.

### Prerequisites

Following python modules (if not already part of host modules) have to be installed to successfully run the code:

```
random
math	
matplotlib
os
platform
statistics
prettytable
```

### Running the code

Without any given parametrs, the code is activated as follows:

```
python .\GRCRollProbability.py
```

## Code modifications

To modify "parameters" of Monte Carlo simmulation, following fields have to be considered:

```
random.seed(0)			- uncommenting this random function will turn the randomizer to pseudo-random mode
loan_cap				- number of single loans iterations within 1 cycle
cycles_counter			- number of cycles in estimating innovations performance
loan_size				- value of average loan
glob_loan_units_distr	- represents a "unit loans" distribution within observed years
ass_distrib_iteration	- number of iterations for modelling innovations' performance
```

## Built With

* [PyCharm EDU v.2020.1](https://blog.jetbrains.com/pycharm/2020/04/pycharm-2020-1-out-now/) - integrated Python SDK.


## Versioning

GIT versioning details are provided in [commits in this repository](https://github.com/Mirris/Miroslav-Hons---Monte-Carlo-in-GRC/commits/master).

## Author

* **Miroslav Hons** - *Initial work* - **Impact of Corporate Risk Management (GRC) on the Genesis and Implementation of Process Innovations**


## License

This project is licensed under the MIT License

## Disclaimer

Code has been provided in state of "as is" and "as available" and doesn't assure user with any author's responsibility by downloading and running the code.

* **1. Redistribution** - redistribution of the code is permitted, as followed by [GitHub T&Cs](https://help.github.com/en/github/site-policy/github-terms-of-service).
* **2. Names of contributors** - names of contributors may not be used in recognition or promotion of code from this repository.
* **3. Usage** - Methods and information provided within code are for illustratory purpose only. Usage of code in real environment provides no varanties of reliability, completeness or accuracy. Actions taken by using a code of this repository are, therefore, at full user's risk.