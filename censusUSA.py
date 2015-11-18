import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# loading data
pop_a_loc = '~/Downloads/csv_pus/ss13pusa.csv'
pop_b_loc = '~/Downloads/csv_pus/ss13pusb.csv'

pop_a = pd.read_csv(pop_a_loc, usecols = ['SERIALNO','SPORDER','CIT','PINCP','SCHL', 'POBP'])
pop_b = pd.read_csv(pop_b_loc, usecols = ['SERIALNO','SPORDER','CIT','PINCP','SCHL', 'POBP'])

pop_total = pd.DataFrame(pd.concat([pop_a, pop_b], axis = 0))

# consolidating citizenship data into two categories
pop_total.loc[pop_total["CIT"] < 3, "CIT"] = 1
pop_total.loc[pop_total["CIT"] > 2, "CIT"] = 2

# consolidating place of birth data into six categories
pop_total.loc[pop_total["POBP"] < 100, "POBP"] = 1   # Born in US
mask1 = (pop_total["POBP"] >= 100) & (pop_total["POBP"] < 200)
pop_total.loc[mask1, "POBP"] = 2    # Born in Europe
mask2 = (pop_total["POBP"] >= 200) & (pop_total["POBP"] < 300)
pop_total.loc[mask2, "POBP"] = 3    # Born in Asia
mask3 = (pop_total["POBP"] >= 300) & (pop_total["POBP"] < 400)
pop_total.loc[mask3, "POBP"] = 4    # Born in America
mask4 = (pop_total["POBP"] >= 400) & (pop_total["POBP"] < 500)
pop_total.loc[mask4, "POBP"] = 5    # Born in Africa
mask5 = (pop_total["POBP"] >= 500) & (pop_total["POBP"] < 600)
pop_total.loc[mask5, "POBP"] = 6    # Born in Oceania

# consolidating education data into 4 categories
pop_total.loc[pop_total["SCHL"] < 21, "SCHL"] = 1
pop_total.loc[pop_total["SCHL"] == 23, "SCHL"] = 22

# we only care about positive income
pop_total = pop_total[pop_total.PINCP > 0]

# income for US-born vs born abroad
pop_inc_pivot = pop_total.pivot_table(index = ['SERIALNO'], values = ['PINCP'], 
                                  columns = ['CIT'])

plt1 = pop_inc_pivot.plot(kind = 'box', showfliers = False, whis = [5, 95], 
                    showmeans = True)
                    
labelx = -0.12  # axes coords
xlabels = ['Born in US', 'Born Abroad']
plt1.set_xticklabels(xlabels)
plt1.set_xlabel('Place of Birth')
plt1.set_ylabel('2013 Annual Income (USD)')
plt1.yaxis.set_label_coords(labelx, 0.5)
plt.ylim(-5000,140000)

plt.savefig('Income_vs_birthPlace.jpg', dpi = 300)

# income for different ethnicities
pop_inc_pivot2 = pop_total.pivot_table(index = ['SERIALNO'], values = ['PINCP'], 
                                  columns = ['POBP'])

plt2 = pop_inc_pivot2.plot(kind = 'box', showfliers = False, whis = [5, 95], 
                    showmeans = True)
                    

xlabels = ['US', 'Europe', 'Asia', 'America', 'Africa', 'Oceania']
plt2.set_xticklabels(xlabels)
plt2.set_xlabel('Ethnicity')
plt2.set_ylabel('2013 Annual Income (USD)')
plt2.yaxis.set_label_coords(labelx, 0.5)
plt.ylim(-5000,200000)

plt.savefig('Income_vs_ethnicity.jpg', dpi = 300)

# Level of education vs place of birth

# calculating size of each segment
nt_dip = len(pop_total[(pop_total.CIT == 1) & (pop_total.SCHL == 1)])
nt_bac = len(pop_total[(pop_total.CIT == 1) & (pop_total.SCHL == 21)])
nt_mas = len(pop_total[(pop_total.CIT == 1) & (pop_total.SCHL == 22)])
nt_phd = len(pop_total[(pop_total.CIT == 1) & (pop_total.SCHL == 24)])
im_dip = len(pop_total[(pop_total.CIT == 2) & (pop_total.SCHL == 1)])
im_bac = len(pop_total[(pop_total.CIT == 2) & (pop_total.SCHL == 21)])
im_mas = len(pop_total[(pop_total.CIT == 2) & (pop_total.SCHL == 22)])
im_phd = len(pop_total[(pop_total.CIT == 2) & (pop_total.SCHL == 24)])

nt_num = len(pop_total[pop_total.CIT == 1])
im_num = len(pop_total[pop_total.CIT == 2])

nums_us = (100 * nt_dip / nt_num, 100 * nt_bac / nt_num, 100 * nt_mas / nt_num,
           100 * nt_phd / nt_num)
nums_abr = (100 * im_dip / im_num, 100 * im_bac / im_num, 100 * im_mas / im_num,
           100 * im_phd / im_num)

ind = np.arange(4)  # the x locations for the groups
width = 0.35       # the width of the bars
opacity = 0.4

fig, ax = plt.subplots()
rects1 = ax.bar(ind, nums_us, width, alpha = opacity, color = 'r', 
                label = 'Born in US')
rects2 = ax.bar(ind + width, nums_abr, width, alpha = opacity, color = 'b', 
                label = 'Born Abroad')

# add some text for labels, title and axes ticks
ax.set_xlabel('Degree')
ax.set_ylabel('Percent')
#ax.set_title('Degree Holders in US Based on Citizenship')
ax.set_xticks(ind + width)
ax.set_xticklabels(('No Degree', 'Bachelor', 'Masters', 'PhD'))
ax.legend()

def autolabel(rects1, rects2):
    height = []
    # attach some text labels
    for rect in rects2:
        height += [int(rect.get_height())]
    i = 0
    for rect in rects1:
        diff_perc = 100 * (height[i] - int(rect.get_height())) / int(rect.get_height())
        ax.text(rect.get_x() + 3 * rect.get_width() / 2., 1.1 * height[i],
                '%d%%' % diff_perc, ha = 'center', va = 'bottom')
        i += 1

autolabel(rects1, rects2)

plt.savefig('education_vs_birthPlace.jpg', dpi = 300)

# level of education for different ethnicities

# calculating the slices
eu_nd = 100 * len(pop_total[(pop_total.POBP == 2) & (pop_total.SCHL == 1)]) # EU no degree
eu_bc = 100 * len(pop_total[(pop_total.POBP == 2) & (pop_total.SCHL == 21)]) # EU Bachelor
eu_ms = 100 * len(pop_total[(pop_total.POBP == 2) & (pop_total.SCHL == 22)]) # EU Master
eu_phd = 100 * len(pop_total[(pop_total.POBP == 2) & (pop_total.SCHL == 24)]) # EU phd
eu_tot = len(pop_total[pop_total.POBP == 2])
sizes_eu = [round(eu_nd / eu_tot), round(eu_bc / eu_tot), round(eu_ms / eu_tot), 
            round(eu_phd / eu_tot)]

asia_nd = 100 * len(pop_total[(pop_total.POBP == 3) & (pop_total.SCHL == 1)]) # Asia no degree
asia_bc = 100 * len(pop_total[(pop_total.POBP == 3) & (pop_total.SCHL == 21)]) # Asia Bachelor
asia_ms = 100 * len(pop_total[(pop_total.POBP == 3) & (pop_total.SCHL == 22)]) # Asia Master
asia_phd = 100 * len(pop_total[(pop_total.POBP == 3) & (pop_total.SCHL == 24)]) # Asia phd
asia_tot = len(pop_total[pop_total.POBP == 3])
sizes_asia = [round(asia_nd / asia_tot), round(asia_bc / asia_tot), 
              round(asia_ms / asia_tot), round(asia_phd / asia_tot)]

amer_nd = 100 * len(pop_total[(pop_total.POBP == 4) & (pop_total.SCHL == 1)]) # America no degree
amer_bc = 100 * len(pop_total[(pop_total.POBP == 4) & (pop_total.SCHL == 21)]) # America Bachelor
amer_ms = 100 * len(pop_total[(pop_total.POBP == 4) & (pop_total.SCHL == 22)]) # America Master
amer_phd = 100 * len(pop_total[(pop_total.POBP == 4) & (pop_total.SCHL == 24)]) # America phd
amer_tot = len(pop_total[pop_total.POBP == 4])
sizes_america = [round(amer_nd / amer_tot), round(amer_bc / amer_tot), 
                 round(amer_ms / amer_tot), round(amer_phd / amer_tot)]

afr_nd = 100 * len(pop_total[(pop_total.POBP == 5) & (pop_total.SCHL == 1)]) # Africa no degree
afr_bc = 100 * len(pop_total[(pop_total.POBP == 5) & (pop_total.SCHL == 21)]) # Africa Bachelor
afr_ms = 100 * len(pop_total[(pop_total.POBP == 5) & (pop_total.SCHL == 22)]) # Africa Master
afr_phd = 100 * len(pop_total[(pop_total.POBP == 5) & (pop_total.SCHL == 24)]) # Africa phd
afr_tot = len(pop_total[pop_total.POBP == 5])
sizes_africa = [round(afr_nd / afr_tot), round(afr_bc / afr_tot), 
                round(afr_ms / afr_tot), round(afr_phd / afr_tot)]

labels = 'No Degree', 'Bachelor', 'Masters', 'PhD'
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

fig = plt.figure()
ax2 = fig.gca()
ax2.pie(sizes_eu, labels = labels, colors = colors, autopct = '%1.0f%%', 
        startangle = 90)
ax2.set_aspect('equal')
plt.savefig('education_for_europe.jpg', dpi = 300)

fig = plt.figure()
ax3 = fig.gca()
ax3.pie(sizes_asia, labels = labels, colors = colors, autopct = '%1.0f%%', 
        startangle = 90)
ax3.set_aspect('equal')
plt.savefig('education_for_asia.jpg', dpi = 300)

fig = plt.figure()
ax4 = fig.gca()
ax4.pie(sizes_america, labels = labels, colors = colors, autopct = '%1.0f%%', 
        startangle = 90)
ax4.set_aspect('equal')
plt.savefig('education_for_america.jpg', dpi = 300)

fig = plt.figure()
ax5 = fig.gca()
ax5.pie(sizes_africa, labels = labels, colors = colors, autopct = '%1.0f%%', 
        startangle = 90)
ax5.set_aspect('equal')
plt.savefig('education_for_africa.jpg', dpi = 300)