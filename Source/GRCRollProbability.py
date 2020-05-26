import random
import math
import matplotlib.pyplot as plt
import os
import platform
import statistics
from statistics import mean
from prettytable import PrettyTable

# --- Generator lock - uncomment for pseud-random generator
# random.seed(0)

# --- Loan Caps - unit loans
loan_cap = 2500  # Original loan cap

# scalars
avg_a_success_rate = 3778
avg_b_success_rate = 8352
cycle_current_loans = 0
fraud_a_alert = 0
fraud_b_alert = 0
index = 0
inno_a_unit_cost = 13.4
inno_b_unit_cost = 73.6
loan_size = 120468
y = 0

# counters
counter_a_activation_delay = 0
counter_a_app_down = 0
counter_a_client_cancel = 0
counter_a_fraud_risk = 0
counter_a_geogr_dispr = 0
counter_a_identity_service_down = 0
counter_a_insurance_risk = 0
counter_a_market_share_change = 0
counter_a_sign_service_down = 0
counter_b_activation_delay = 0
counter_b_app_down = 0
counter_b_client_cancel = 0
counter_b_fraud_risk = 0
counter_b_geogr_dispr = 0
counter_b_identity_service_down = 0
counter_b_insurance_risk = 0
counter_b_market_share_change = 0
counter_b_sign_service_down = 0
cycle_iteration_id = 0

# global arryas
glob_a_avg_interest = []
glob_a_segment = []
glob_a_success_list = []
glob_b_avg_interest = []
glob_b_segment = []
glob_b_success_list = []
glob_cashflow_a_unit = []
glob_cashflow_b_unit = []
glob_cost_a_unit = []
glob_cost_b_unit = []
glob_inno_id = ['a', 'b']
glob_loan_units_distr = [392382, 1057208, 1050394]

# global scalars
glob_a_current_loans = 0
glob_a_dism_loans_counter = 0
glob_a_loans = 0
glob_a_loans_counter = 0
glob_a_lost_loans = 0
glob_b_current_loans = 0
glob_b_dism_loans_counter = 0
glob_b_loans = 0
glob_b_loans_counter = 0
glob_b_lost_loans = 0
glob_cycle = 1
glob_loans_counter = 0
glob_lost_loans = 0


# logarithmic arrays
log_a_avg_interest = []
log_a_glob_loans = []
log_a_glob_lost_loans = []
log_a_iter_id = []
log_a_loans_counter = []
log_a_lost_loans = []
log_a_segment_a = []
log_a_segment_b = []
log_a_segment_c = []
log_b_avg_interest = []
log_b_glob_loans = []
log_b_glob_lost_loans = []
log_b_iter_id = []
log_b_loans_counter = []
log_b_lost_loans = []
log_b_segment_a = []
log_b_segment_b = []
log_b_segment_c = []


# system helpers
def cls():
    os.system("cls" if platform.system().lower() == "windows" else "clear")


# dice rolls
def roll_random(min, max):
    roll_rand = random.randint(min, max)
    return roll_rand


def roll_segment(min, max):
    roll_rand = random.randint(min, max)
    if roll_rand == 1:
        return 'a'
    elif roll_rand == 2:
        return 'b'
    else:
        return 'c'


def roll_loan():
    # List can be extended by different loan amounts
    loan_list = [1]
    loan = random.choice(loan_list)
    return loan


def roll_interest(segment):
    if segment == 'a':
        roll = round(random.uniform(3.01, 5.62), 2)
    elif segment == 'b':
        roll = round(random.uniform(4.10, 7.12), 2)
    else:
        roll = round(random.uniform(5.02, 8.80), 2)
    return roll


def roll_loan_prob(success_rate):
    roll = random.randint(1, 10000)
    return True if roll < success_rate else False


# ---=== KRI Section Start ===---
# R001 - Geographical disproportion
def geographical_disproportion(inno):
    global counter_a_geogr_dispr
    global counter_b_geogr_dispr

    roll = roll_random(1, 200)
    if inno == 'a' and roll >= 198:
        counter_a_geogr_dispr += 1
        return True
    elif inno == 'b' and roll == 200:
        counter_b_geogr_dispr += 1
        return True
    else:
        return False


# R002 - Activation delay (no time to lose the time)
def activation_delay(inno):
    global counter_a_activation_delay
    global counter_b_activation_delay

    roll = roll_random(1, 100)
    if inno == 'a' and roll >= 98:
        counter_a_activation_delay += 1
        return True
    elif inno == 'b' and roll == 100:
        counter_b_activation_delay += 1
        return True
    else:
        return False


# R003 - Market Share Risk
def market_share_change(inno):
    global counter_a_market_share_change
    global counter_b_market_share_change

    roll = roll_random(1, 100)
    if inno == 'a' and roll >= 95:
        counter_a_market_share_change += 1
        return True
    elif inno == 'b' and roll == 100:
        counter_b_market_share_change += 1
        return True
    else:
        return False


# R004 - Fraud alert
def fraud_risk(inno):
    global counter_a_fraud_risk
    global counter_b_fraud_risk
    global fraud_a_alert
    global fraud_b_alert

    roll = roll_random(1, 500)
    if inno == 'a' and roll >= 490:
        counter_a_fraud_risk += 1
        fraud_a_alert = 40
        return True
    elif inno == 'b' and roll >= 499:
        counter_b_fraud_risk += 1
        fraud_b_alert = 40
        return True
    else:
        if inno == 'a':
            fraud_a_alert -= 1
        if inno == 'b':
            fraud_b_alert -= 1
        return False


# R005 - Applications cancelled by client
def app_client_cancel(inno):
    global counter_a_client_cancel
    global counter_b_client_cancel

    roll = roll_random(1, 200)
    if inno == 'a' and roll >= 185:
        counter_a_client_cancel += 1
        return True
    elif inno == 'b' and roll >= 197:
        # elif inno == 'b' and roll >= 199:
        counter_b_client_cancel += 1
        return True
    else:
        return False


# R006 - Insurance sell
def insurance_sell_risk(inno):
    global counter_a_insurance_risk
    global counter_b_insurance_risk

    # to implement penaliser at cross-sell 22.5%
    roll = roll_random(1, 200)
    if inno == 'a' and roll <= 162:
        counter_a_insurance_risk += 1
        return True
    elif inno == 'b' and roll <= 158:
        counter_b_insurance_risk += 1
        return True
    else:
        return False


# R007 - Identity service down
def identity_service_down(inno):
    global counter_a_identity_service_down
    global counter_b_identity_service_down

    roll = roll_random(1, 500)
    if inno == 'a' and roll == 500:
        counter_a_identity_service_down += 1
        return True
    elif inno == 'b' and roll == 500:
        counter_b_identity_service_down += 1
        return True
    else:
        return False


# R008 - App is down
def app_down(inno):
    global counter_a_app_down
    global counter_b_app_down

    roll = roll_random(1, 1000)
    if inno == 'a' and roll >= 998:
        counter_a_app_down += 1
        return True
    elif inno == 'b' and roll >= 999:
        counter_b_app_down += 1
        return True
    else:
        return False


# R009 - Signature service down
def sign_service_down(inno):
    global counter_a_sign_service_down
    global counter_b_sign_service_down

    roll = roll_random(1, 500)
    if inno == 'a' and roll == 500:
        counter_a_sign_service_down += 1
        return True
    elif inno == 'b' and roll == 500:
        counter_b_sign_service_down += 1
        return False
    else:
        return True


def kri_results(kri_idd, description, inno_1_value, inno_2_value):
    table = PrettyTable(['KRI ID', 'Description', 'Innovation 1', 'Innovation 2'])

    table.align = 'l'

    for n in range(0, len(kri_idd)):
        table.add_row([kri_idd[n], description[n], inno_1_value[n], inno_2_value[n]])
    return table
# ---=== KRI Section End ===---


# Reporting table for unit loans performance
def macro_results(iter_id, loans_counter2, lost_loans_counter, avg_interest, segment_a, segment_b, segment_c):
    table = PrettyTable(
        ['Iteration', 'Loans Count', 'Avg. Interest', 'Segment A', 'Segment B', 'Segment C', 'Opport. Loans',
         'Real./Opport %'])
    table.align = 'r'

    for i in range(0, len(iter_id)):
        opp_loan_ratio = (loans_counter2[i] / (lost_loans_counter[i] + loans_counter2[i]) * 100)
        opp_loan_ratio = round(opp_loan_ratio, 2)
        table.add_row(
            ["{:,d}".format(iter_id[i]), "{:,d}".format(loans_counter2[i]), "{:.2f}".format(avg_interest[i], 2),
             segment_a[i], segment_b[i], segment_c[i], "{:,d}".format(lost_loans_counter[i]), opp_loan_ratio])
    return table


# Reporting table for unit loans performance
def assets_distr():
    global glob_cashflow_a_unit
    global glob_cashflow_b_unit
    global glob_cost_a_unit
    global glob_cost_b_unit

    line = str(glob_cashflow_a_unit + glob_cashflow_b_unit + glob_cost_a_unit + glob_cost_b_unit) + '\n'
    f = open("assets_and_costs_distr.txt", "a")
    f.write(str(line))
    f.close()


def loan_cycle_simulation(current_loans, loan_cap):

    global cycle_iteration_id
    cycle_iteration_id = 1

    while current_loans < loan_cap:

        # cycle globals
        global counter_a_activation_delay
        global counter_a_geogr_dispr
        global counter_b_activation_delay
        global counter_b_geogr_dispr
        global glob_a_current_loans
        global glob_a_dism_loans_counter
        global glob_a_loans
        global glob_a_loans_counter
        global glob_a_lost_loans
        global glob_a_success_list
        global glob_b_current_loans
        global glob_b_dism_loans_counter
        global glob_b_loans
        global glob_b_loans_counter
        global glob_b_lost_loans
        global glob_cycle
        global glob_lost_loans

        # iteration specific rolls
        gimmeSegment = roll_segment(1, 3)
        gimmeInterest = roll_interest(gimmeSegment)
        gimmeLoan = roll_loan()

        for inno in glob_inno_id:

            # KRIs check
            geographical_disproportion(inno)    # R001
            activation_delay(inno)              # R002
            market_share_change(inno)           # R003
            fraud_risk(inno)                    # R004 - results in this + 40 applications cancel
            app_client_cancel(inno)             # R005 - results in application cancel
            insurance_sell_risk(inno)           # R006
            identity_service_down(inno)         # R007
            app_down(inno)                      # R008 - results in applciaiton cancel
            sign_service_down(inno)             # R009

            # Evaluation of each specific loan according to risk rules from KPIs
            if inno == 'a':
                if fraud_a_alert <= 0 and not (app_client_cancel(inno) or app_down(inno)):
                    glob_a_current_loans += gimmeLoan
                    glob_a_loans += gimmeLoan
                    glob_a_segment.append(gimmeSegment)
                    glob_a_avg_interest.append(gimmeInterest)
                    glob_a_success_list.append(1)
                    glob_a_loans_counter += 1
                else:
                    glob_a_lost_loans += gimmeLoan
                    glob_a_success_list.append(0)
                    glob_a_dism_loans_counter += 1

            if inno == 'b':
                if fraud_b_alert <= 0 and not (app_client_cancel(inno) or app_down(inno)):
                    glob_b_current_loans += gimmeLoan
                    glob_b_loans += gimmeLoan
                    glob_b_segment.append(gimmeSegment)
                    glob_b_avg_interest.append(gimmeInterest)
                    glob_b_success_list.append(1)
                    glob_b_loans_counter += 1
                else:
                    glob_b_lost_loans += gimmeLoan
                    glob_b_success_list.append(0)
                    glob_b_dism_loans_counter += 1

            # Report interim results on logarithmic scale
            if glob_cycle > 1:
                if math.log10(glob_cycle).is_integer():
                    if inno == 'a':
                        log_a_iter_id.append(glob_cycle)
                        log_a_glob_loans.append(glob_a_loans)
                        log_a_loans_counter.append(glob_a_loans_counter)
                        log_a_glob_lost_loans.append(glob_a_lost_loans)
                        log_a_lost_loans.append(glob_a_dism_loans_counter)
                        log_a_segment_a.append(glob_a_segment.count('a'))
                        log_a_segment_b.append(glob_a_segment.count('b'))
                        log_a_segment_c.append(glob_a_segment.count('c'))
                        log_a_avg_interest.append(mean(glob_a_avg_interest))
                    else:
                        log_b_iter_id.append(glob_cycle)
                        log_b_glob_loans.append(glob_b_loans)
                        log_b_loans_counter.append(glob_b_loans_counter)
                        log_b_glob_lost_loans.append(glob_b_lost_loans)
                        log_b_lost_loans.append(glob_b_dism_loans_counter)
                        log_b_segment_a.append(glob_b_segment.count('a'))
                        log_b_segment_b.append(glob_b_segment.count('b'))
                        log_b_segment_c.append(glob_b_segment.count('c'))
                        log_b_avg_interest.append(mean(glob_b_avg_interest))

            # Chart data sampling / 5, ignored for first 1000 values (chart call is at bottom of this file)
            if glob_cycle < 1000 or cycle_iteration_id % 5 == 0:

                if inno == 'a':
                    iteration_a_x.append(cycle_iteration_id)
                    loan_a_y.append(glob_a_current_loans)
                else:
                    iteration_b_x.append(cycle_iteration_id)
                    loan_b_y.append(glob_b_current_loans)

        # 1up cycle & iteration
        current_loans += gimmeLoan
        cycle_iteration_id += 1
        glob_cycle += 1

    # plot results of each simulation
    plt.plot(iteration_a_x, loan_a_y, color='red', label='Inovace 1')
    plt.plot(iteration_b_x, loan_b_y, color='blue', label='Inovace 2')


# ---=== Main part of the code ===---
x = 0
cycles_counter = 1000

while x < cycles_counter:
    x += 1
    cls()
    print('\n Copyright (c) 2020 Cambridge Business School')
    print(' All Rights Reserved.')
    print(' Author: Miroslav Hons')
    print('\n Progress: ', "{:.1f}".format(x * (100 / cycles_counter)), '%')
    glob_a_current_loans = 0
    glob_b_current_loans = 0
    iteration_a_x = []
    iteration_b_x = []
    loan_a_y = []
    loan_b_y = []
    loan_cycle_simulation(cycle_current_loans, loan_cap)

# ---=== Inovation 1 Unit Loans Statistics ===---
print('\n Results Innovation 1')
print(macro_results(log_a_iter_id, log_a_loans_counter, log_a_lost_loans, log_a_avg_interest, log_a_segment_a,
                    log_a_segment_b, log_a_segment_c))
print(' Mean: ', "{:,f}".format(statistics.mean(glob_a_success_list)))
print(' Standard Deviation: ', "{:,f}".format(statistics.stdev(glob_a_success_list)))

# ---=== Inovation 2 Unit Loans Statistics ===---
print('\n Results Innovation 2')
print(macro_results(log_b_iter_id, log_b_loans_counter, log_b_lost_loans, log_b_avg_interest, log_b_segment_a,
                    log_b_segment_b, log_b_segment_c))
print(' Mean: ', "{:,f}".format(statistics.mean(glob_b_success_list)))
print(' Standard Deviation: ', "{:,f}".format(statistics.stdev(glob_b_success_list)))

# ---=== KRI Indicators Evaluation ===---
kri_id = []
kri_description = []
kri_inno_1_value = []
kri_inno_2_value = []

kri_id.append('KRI_001')
kri_description.append('Geographical Disproportion')
kri_inno_1_value.append(counter_a_geogr_dispr)
kri_inno_2_value.append(counter_b_geogr_dispr)

kri_id.append('KRI_002')
kri_description.append('Account Activation Delay')
kri_inno_1_value.append(counter_a_activation_delay)
kri_inno_2_value.append(counter_b_activation_delay)

kri_id.append('KRI_003')
kri_description.append('Market Share Risk')
kri_inno_1_value.append(counter_a_market_share_change)
kri_inno_2_value.append(counter_b_market_share_change)

kri_id.append('KRI_004_a')
kri_description.append('Fraud Alert')
kri_inno_1_value.append(counter_a_fraud_risk)
kri_inno_2_value.append(counter_b_fraud_risk)

kri_id.append('KRI_004_b')
kri_description.append('Fraud Alert - Penalty Status')
kri_inno_1_value.append(fraud_a_alert)
kri_inno_2_value.append(fraud_b_alert)

kri_id.append('KRI_005')
kri_description.append('Applications Cancelled by Client')
kri_inno_1_value.append(counter_a_client_cancel)
kri_inno_2_value.append(counter_b_client_cancel)

kri_id.append('KRI_006')
kri_description.append('Insurance Sales Lost')
kri_inno_1_value.append(counter_a_insurance_risk)
kri_inno_2_value.append(counter_b_insurance_risk)

kri_id.append('KRI_007')
kri_description.append('Identity Service Down')
kri_inno_1_value.append(counter_a_identity_service_down)
kri_inno_2_value.append(counter_b_identity_service_down)

kri_id.append('KRI_008')
kri_description.append('Banking App Down')
kri_inno_1_value.append(counter_a_app_down)
kri_inno_2_value.append(counter_b_app_down)

kri_id.append('KRI_009')
kri_description.append('Signature check service down')
kri_inno_1_value.append(counter_a_sign_service_down)
kri_inno_2_value.append(counter_b_sign_service_down)

# KRI's evaluation table
print('\n KRIs Indicators via ', glob_cycle - 1, 'iterations.')
print(kri_results(kri_id, kri_description, kri_inno_1_value, kri_inno_2_value))


# ---=== Assets Distribution Model ===---

# Simulated iterations
ass_distrib_iteration = 100
print('\n')

# Report file cleanup
open('assets_and_costs_distr.txt', 'w').close()

while y < ass_distrib_iteration:
    y += 1

    print(' Modelling Loan Assets Distributbution: ', y, ' / ', ass_distrib_iteration)

    for current_loan_unit in glob_loan_units_distr:

        current_a_cashflow = 0
        current_a_cost = 0
        current_b_cashflow = 0
        current_b_cost = 0
        loan_unit_size = 0

        # cleanup CF lists
        glob_cashflow_a_unit = []
        glob_cashflow_b_unit = []
        glob_cost_a_unit = []
        glob_cost_b_unit = []

        while loan_unit_size <= current_loan_unit:

            for inno in glob_inno_id:

                if inno == 'a':
                    if roll_loan_prob(avg_a_success_rate):
                        current_a_cashflow += loan_size
                    current_a_cost += inno_a_unit_cost

                elif inno == 'b':
                    if roll_loan_prob(avg_b_success_rate):
                        current_b_cashflow += loan_size
                    current_b_cost += inno_b_unit_cost

            loan_unit_size += 1

        glob_cashflow_a_unit.append(current_a_cashflow)
        glob_cashflow_b_unit.append(current_b_cashflow)
        glob_cost_a_unit.append(current_a_cost)
        glob_cost_b_unit.append(current_b_cost)

        assets_distr()

# Report file info
print('\n Loans and investments costs distribution has been stored to assets_and_costs_distr.txt - 3 records per cycle.')

# ---=== Charting loan performance of Innovation 1 and Innovation 2 ===---

# English chart labels
# plt.ylabel('Unit Loans')
# plt.xlabel('Iterations')

# Czech chart labels
plt.ylabel('Jednotky úvěrů')
plt.xlabel('Iterace')

# Chart rendering
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc="upper left")
plt.show()
