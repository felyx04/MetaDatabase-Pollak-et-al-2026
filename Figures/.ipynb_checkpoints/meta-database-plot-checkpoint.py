#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 10:25:30 2026

@author: pollakf

Note: Code to generate a single plot (with pyleoclim) of all d18O/SST/terrestrial 
      records included for the analysis of the 2nd plot.
    
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as mcolors
import seaborn as sns
import scipy
import pdfkit
import os
import string
alphabet = string.ascii_lowercase  # 'a', 'b', 'c', ...
import pyleoclim as pyleo


# Load data sets
df = pd.read_csv('/home/pollakf/Python/Datasets/all-data.csv', header=[0, 1])

# Load MIS bounds
bounds_probstack = pd.read_csv('/home/pollakf/Python/Datasets/Prob-stack_MISboundaries.csv').to_numpy()   


colors = 'grey'

# Adds the MIS intervals as extra axis on top of each plot
add_mis_bounds = True

# -----------------------------------------------------------------------------
# Select records

# benthic d18O 
metrics_d18Ob = [
    'LR04',
    'Probstack',
    'Zhou et al. (2026) - BIGSTACK_mixed - Global benthic δ18O stack',
    'Zhou et al. (2026) - BIGSTACK_mixedA - Atlantic benthic δ18O stack',
    'Zhou et al. (2026) - BIGSTACK_mixedP - Pacific benthic δ18O stack'
]

# benthic d18O (tuned)
metrics_d18Ob_tuned = [
    'LR04',
    'Probstack',
    'PROBSTACK TUNED - Zhou et al. (2026) - BIGSTACK_mixed - Global benthic δ18O stack',
    'PROBSTACK TUNED - Zhou et al. (2026) - BIGSTACK_mixedA - Atlantic benthic δ18O stack',
    'PROBSTACK TUNED - Zhou et al. (2026) - BIGSTACK_mixedP - Pacific benthic δ18O stack'
]

# SST 
metrics_sst = [
    'Clark et al. (2024) - Global Mean ΔSST stack', 
    'Clark et al. (2024) - North Atlantic ΔSST stack', 
    'Clark et al. (2024) - Tropical Atlantic ΔSST stack',
    'Clark et al. (2024) - South Atlantic ΔSST stack', 
    'Clark et al. (2024) - North Pacific ΔSST stack', 
    'Clark et al. (2024) - Tropical Pacific ΔSST stack', 
    'Clark et al. (2024) - South Pacific ΔSST stack', 
    'Clark et al. (2024) - Tropical ΔSST stack', 
    'Herbert et al. (2010) - Tropical ΔSST stack'
]

# SST (tuned)
metrics_sst_tuned = [
    'PROBSTACK TUNED - Clark et al. (2024) - Global Mean ΔSST stack', 
    'PROBSTACK TUNED - Clark et al. (2024) - North Atlantic ΔSST stack', 
    'PROBSTACK TUNED - Clark et al. (2024) - Tropical Atlantic ΔSST stack',
    'PROBSTACK TUNED - Clark et al. (2024) - South Atlantic ΔSST stack', 
    'PROBSTACK TUNED - Clark et al. (2024) - North Pacific ΔSST stack', 
    'PROBSTACK TUNED - Clark et al. (2024) - Tropical Pacific ΔSST stack', 
    'PROBSTACK TUNED - Clark et al. (2024) - South Pacific ΔSST stack', 
    'PROBSTACK TUNED - Clark et al. (2024) - Tropical ΔSST stack', 
    'PROBSTACK TUNED - Herbert et al. (2010) - Tropical ΔSST stack'
]

# MOT 
metrics_mot = [
    'Clark et al. (2025) - Δ Mean Ocean Temperature (ΔMOT) - Global stack'
]

# MOT (tuned)
metrics_mot_tuned = [
    'PROBSTACK TUNED - Clark et al. (2025) - Δ Mean Ocean Temperature (ΔMOT) - Global stack'
]
    

# terrestrial
metrics_terrestrial = [
    'Ding et al. (2002) - Normalised mean loess size - Chiloparts stack',
    'Sun et al. (2021) - Loess mean size - Gulang Loess',
    'Sun et al. (2019) - Loess mean size - Jingyuan Loess',
    'Sun et al. (2019) - d13C of inorganic loess carbonates - Jingyuan Loess',
    'Sun et al. (2019) - Emulated Mean Annual Precipitation (MAP) - Jingyuan Loess',
    'Sun et al. (2019) - Emulated Mean Annual Temperature (MAT) - Jingyuan Loess',
    'Zhao et al. (2021) - 9pt-average  Mean Annual Temperature (MAT) - Paleolake at Zoige Basin (Core ZB13-C2)',
    'Tzedakis et al. (2006) - Arboreal pollen (AP%) - Tenaghi Philippon',
    'Donders et al. (2021) - Arboreal Pollen content (AP%) - Lake Ohrid',
    'Zhao et al. (2020) - Arboreal Pollen content (AP%) - Paleolake at Zoige Basin (Core ZB13-C2)',
    'Torres et al. (2013) - Arboreal Pollen content (AP%), excl. Quercus & Alnus - Bogotá Basin (Funza09)',
    "Melles et al. (2012) - Si/Ti - Lake El'gygytgyn",   
    'Prokopenko et al. (2006) - Biogenic Silicia (BioSi %) - Lake Baikal',
    'Sun et al. (2021) - Ca/K - Lake Ohrid'
]


# terrestrial (tuned)
metrics_terrestrial_tuned = [
    'PROBSTACK TUNED - Ding et al. (2002) - Normalised mean loess size - Chiloparts stack',
    'PROBSTACK TUNED - Sun et al. (2021) - Loess mean size - Gulang Loess',
    'PROBSTACK TUNED - Sun et al. (2019) - Loess mean size - Jingyuan Loess',
    'PROBSTACK TUNED - Sun et al. (2019) - d13C of inorganic loess carbonates - Jingyuan Loess',
    'PROBSTACK TUNED - Sun et al. (2019) - Emulated Mean Annual Precipitation (MAP) - Jingyuan Loess',
    'PROBSTACK TUNED - Sun et al. (2019) - Emulated Mean Annual Temperature (MAT) - Jingyuan Loess',
    'PROBSTACK TUNED - Zhao et al. (2021) - 9pt-average  Mean Annual Temperature (MAT) - Paleolake at Zoige Basin (Core ZB13-C2)',
    'PROBSTACK TUNED - Tzedakis et al. (2006) - Arboreal pollen (AP%) - Tenaghi Philippon',
    'PROBSTACK TUNED - Donders et al. (2021) - Arboreal Pollen content (AP%) - Lake Ohrid',
    'PROBSTACK TUNED - Zhao et al. (2020) - Arboreal Pollen content (AP%) - Paleolake at Zoige Basin (Core ZB13-C2)',
    'PROBSTACK TUNED - Torres et al. (2013) - Arboreal Pollen content (AP%), excl. Quercus & Alnus - Bogotá Basin (Funza09)',
    "Melles et al. (2012) - Si/Ti - Lake El'gygytgyn",   
    'PROBSTACK TUNED - Prokopenko et al. (2006) - Biogenic Silicia (BioSi %) - Lake Baikal',
    'PROBSTACK TUNED - Sun et al. (2021) - Ca/K - Lake Ohrid'
]

all_metrics = metrics_d18Ob + metrics_sst + metrics_mot + metrics_terrestrial 
all_metrics_tuned = metrics_d18Ob_tuned + metrics_sst_tuned + metrics_mot_tuned + metrics_terrestrial_tuned 
print("Length of all included records: ",len(all_metrics))


# -----------------------------------------------------------------------------

# # create Pyleoclim plot
# serieslist = []
# selected_metric = metrics_terrestrial

# for i, metric in enumerate(selected_metric):
#     ts = pyleo.Series(time=df[metric]['age'], value=df[metric]['data'], time_name='Age (ka)', time_unit='ka', value_name=df[metric].loc[0,'variable']
#                      )
#     ts = ts.slice(timespan=[0,1500]) 

#     serieslist.append(ts)    

# ts.plot()

# ms = pyleo.MultipleSeries(serieslist)

# labels = [df[metric].loc[0,'name'] for metric in selected_metric]

# fig, ax = ms.stackplot(figsize=(10,12), labels=labels, colors=colors)

# y_invert = [df[metric].loc[0,'y_invert'] for metric in selected_metric]

# for i, invert in enumerate(y_invert):
#     if invert:
#         ax[i].invert_yaxis()
        

# -------------------------------------------------------------------------------------------------------
# create d18O plot
# create Pyleoclim plot
serieslist = []
selected_metric = metrics_d18Ob

for i, metric in enumerate(selected_metric):
    ts = pyleo.Series(time=df[metric]['age'], value=df[metric]['data'], time_name='Age (ka)', time_unit='ka', value_name= '$\\delta^{18}$O (‰)'
                     )
    ts = ts.slice(timespan=[0,1500]) 

    serieslist.append(ts)    


ms = pyleo.MultipleSeries(serieslist)

names = ['LR04', 'Prob-stack', 'BIGSTACK$_{mixed}$', 'BIGSTACK$_{mixedA}$', 'BIGSTACK$_{mixedP}$']
labels = [df[metric].loc[0,'author'] + f' - {names[i]}'  for i, metric in enumerate(selected_metric)]

fig, ax = ms.stackplot(figsize=(10,6), labels=labels, colors=colors)

y_invert = [df[metric].loc[0,'y_invert'] for metric in selected_metric]

for i, invert in enumerate(y_invert):
    if invert:
        ax[i].invert_yaxis()

if add_mis_bounds:
    # -----------------------------------------------------------------------
    # Add MIS axis at the top
    # -----------------------------------------------------------------------
    # 1. Squeeze all existing axes downward to make room at the top
    top_margin   = 0.1   # fraction of figure height reserved for MIS axis
    gap          = 0.05   # small gap between MIS axis and the first stackplot
    xlim = 1500  # maximum age to show on the x-axis

    for a in ax.values():
        pos = a.get_position()          # Bbox in figure-fraction coords
        new_pos = [
            pos.x0,
            pos.y0 * (1 - top_margin - gap),   # compress y downward
            pos.width,
            pos.height * (1 - top_margin - gap)
        ]
        a.set_position(new_pos)

    # 2. Create the MIS axis spanning the full width of the plot area
    # Get the exact x bounds from an existing stackplot axis
    ref_ax = list(ax.values())[0]
    ref_pos = ref_ax.get_position()

    # Get the data x-limits and transform to figure coordinates
    # This accounts for any internal padding/margins
    x0_disp, _ = ref_ax.transAxes.transform((0, 0))   # left edge in display coords
    x1_disp, _ = ref_ax.transAxes.transform((1, 0))   # right edge in display coords

    # Convert display coords to figure-fraction coords
    fig_width, fig_height = fig.get_size_inches() * fig.dpi
    x0_fig = x0_disp / fig_width
    x1_fig = x1_disp / fig_width

    mis_ax = fig.add_axes([
        x0_fig,               # exact same left edge
        1 - top_margin,
        x1_fig - x0_fig,      # exact same width
        top_margin - gap
    ])

    # Make sure the MIS axis x-limits match the stackplot x-limits exactly
    mis_ax.set_xlim(ref_ax.get_xlim())

    for start, end, label, state in bounds_probstack:
        if start <= xlim and state == 1:
            mis_ax.axvspan(
                start, end,
                facecolor='red',
                edgecolor=None,
                alpha=0.2
            )
            midpoint = (start + end) / 2
            if midpoint <= xlim:
                mis_ax.text(
                    midpoint, 0.5, label,
                    ha='center', va='center',
                    fontsize=8, rotation=90
                )
        elif start <= xlim and state == 0:
            mis_ax.axvspan(
                start, end,
                facecolor='blue',
                edgecolor=None,
                alpha=0.2
            )
            midpoint = (start + end) / 2
            if midpoint <= xlim:
                mis_ax.text(
                    midpoint, 0.5, label,
                    ha='center', va='center',
                    fontsize=8, rotation=90
                )

    # 4. Clean up the MIS axis appearance
    mis_ax.set_xticks([])          # no x ticks (shared with stackplot below)
    mis_ax.set_yticks([])          # no y ticks needed
    mis_ax.set_ylabel('MIS', fontsize=8, rotation=0, labelpad=20, va='center')
    for spine in ['top', 'right', 'left', 'bottom']:
        mis_ax.spines[spine].set_visible(False)


for a in ax.values():   
    a.spines['top'].set_visible(False)

# Save the figure
fig.savefig("/home/pollakf/Documents/Paper/Pollak_2026/Plots/d180-plots.pdf", bbox_inches='tight')
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
# # create SST+MOT plot
# create Pyleoclim plot
serieslist = []
selected_metric = metrics_sst + metrics_mot

for i, metric in enumerate(selected_metric):
    ts = pyleo.Series(time=df[metric]['age'], value=df[metric]['data'], time_name='Age (ka)', time_unit='ka', value_name=df[metric].loc[0,'variable']
                     )
    ts = ts.slice(timespan=[0,1500]) 

    serieslist.append(ts)    


ms = pyleo.MultipleSeries(serieslist)

# names = ['LR04', 'Prob-stack', r'BIGSTACK_{mixed}', r'BIGSTACK_{mixedA}', r'BIGSTACK_{mixedP}']
# labels = [df[metric].loc[0,'author'] + f' - {names[i]}'  for i, metric in enumerate(selected_metric)]
labels = [df[metric].loc[0,'name'] for metric in selected_metric]
labels[-1] = 'Clark et al. (2025) - ΔMOT'

fig, ax = ms.stackplot(figsize=(10,10), labels=labels, colors=colors)

y_invert = [df[metric].loc[0,'y_invert'] for metric in selected_metric]

for i, invert in enumerate(y_invert):
    if invert:
        ax[i].invert_yaxis()
        
if add_mis_bounds:
    # -----------------------------------------------------------------------
    # Add MIS axis at the top
    # -----------------------------------------------------------------------
    # 1. Squeeze all existing axes downward to make room at the top
    top_margin   = 0.06   # fraction of figure height reserved for MIS axis
    gap          = 0.03   # small gap between MIS axis and the first stackplot
    xlim = 1500  # maximum age to show on the x-axis

    for a in ax.values():
        pos = a.get_position()          # Bbox in figure-fraction coords
        new_pos = [
            pos.x0,
            pos.y0 * (1 - top_margin - gap),   # compress y downward
            pos.width,
            pos.height * (1 - top_margin - gap)
        ]
        a.set_position(new_pos)

    # 2. Create the MIS axis spanning the full width of the plot area
    # Get the exact x bounds from an existing stackplot axis
    ref_ax = list(ax.values())[0]
    ref_pos = ref_ax.get_position()

    # Get the data x-limits and transform to figure coordinates
    # This accounts for any internal padding/margins
    x0_disp, _ = ref_ax.transAxes.transform((0, 0))   # left edge in display coords
    x1_disp, _ = ref_ax.transAxes.transform((1, 0))   # right edge in display coords

    # Convert display coords to figure-fraction coords
    fig_width, fig_height = fig.get_size_inches() * fig.dpi
    x0_fig = x0_disp / fig_width
    x1_fig = x1_disp / fig_width

    mis_ax = fig.add_axes([
        x0_fig,               # exact same left edge
        1 - top_margin,
        x1_fig - x0_fig,      # exact same width
        top_margin - gap
    ])

    # Make sure the MIS axis x-limits match the stackplot x-limits exactly
    mis_ax.set_xlim(ref_ax.get_xlim())

    for start, end, label, state in bounds_probstack:
        if start <= xlim and state == 1:
            mis_ax.axvspan(
                start, end,
                facecolor='red',
                edgecolor=None,
                alpha=0.2
            )
            midpoint = (start + end) / 2
            if midpoint <= xlim:
                mis_ax.text(
                    midpoint, 0.5, label,
                    ha='center', va='center',
                    fontsize=8, rotation=90
                )
        elif start <= xlim and state == 0:
            mis_ax.axvspan(
                start, end,
                facecolor='blue',
                edgecolor=None,
                alpha=0.2
            )
            midpoint = (start + end) / 2
            if midpoint <= xlim:
                mis_ax.text(
                    midpoint, 0.5, label,
                    ha='center', va='center',
                    fontsize=8, rotation=90
                )

    # 4. Clean up the MIS axis appearance
    mis_ax.set_xticks([])          # no x ticks (shared with stackplot below)
    mis_ax.set_yticks([])          # no y ticks needed
    mis_ax.set_ylabel('MIS', fontsize=8, rotation=0, labelpad=20, va='center')
    for spine in ['top', 'right', 'left', 'bottom']:
        mis_ax.spines[spine].set_visible(False)


for a in ax.values():   
    a.spines['top'].set_visible(False)
        
# Save the figure
fig.savefig("/home/pollakf/Documents/Paper/Pollak_2026/Plots/SST-plots.pdf", bbox_inches='tight')
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
# create Terrestrial plot
# create Pyleoclim plot
serieslist = []
selected_metric = metrics_terrestrial
value_names = ['Loess (norm.)', 'Loess (μm)', 'Loess (μm)', '$\\delta^{13}$C (‰)', 'MAP (mm/day)', 'MAT (°C)', 'MAT (°C)', 'AP (%)', 'AP (%)', 'AP (%)', 'AP (%)', 'Si/Ti', 'BioSi (%)', 'Ca/K']

for i, metric in enumerate(selected_metric):
    ts = pyleo.Series(time=df[metric]['age'], value=df[metric]['data'], time_name='Age (ka)', time_unit='ka', value_name=value_names[i]
                     )
    ts = ts.slice(timespan=[0,1500]) 

    serieslist.append(ts)    


ms = pyleo.MultipleSeries(serieslist)

names = ['Normalised mean loess size\nChiloparts stack',
         'Mean loess size - Gulang Loess',
         'Mean loess size - Jingyuan Loess',
         '$\delta^{13}$C of inorganic loess carbonates\nJingyuan Loess',
         'Emulated Mean Annual Precipitation (MAP)\nJingyuan Loess',
         'Emulated Mean Annual Temperature (MAT)\nJingyuan Loess',
         'Mean Annual Temperature (MAT)\nPaleolake at Zoige Basin',
         'Arboreal pollen content (AP%)\nTenaghi Philippon',
         'Arboreal pollen content (AP%)\nLake Ohrid',
         'Arboreal pollen content (AP%)\nPaleolake at Zoige Basin',
         'Arboreal pollen content (AP%)\nBogotá Basin (Funza09)',
         "Si/Ti - Lake El'gygytgyn",
         'Biogenic Silicia (BioSi %) - Lake Baikal',
         'Ca/K - Lake Ohrid'
         ]

labels = [df[metric].loc[0,'author'] + f'\n{names[i]}'  for i, metric in enumerate(selected_metric)]

fig, ax = ms.stackplot(figsize=(10,16), labels=labels, colors=colors)

y_invert = [df[metric].loc[0,'y_invert'] for metric in selected_metric]
for i, invert in enumerate(y_invert):
    if invert:
        ax[i].invert_yaxis()

if add_mis_bounds:
    # -----------------------------------------------------------------------
    # Add MIS axis at the top
    # -----------------------------------------------------------------------
    # 1. Squeeze all existing axes downward to make room at the top
    top_margin   = 0.05   # fraction of figure height reserved for MIS axis
    gap          = 0.025   # small gap between MIS axis and the first stackplot
    xlim = 1500  # maximum age to show on the x-axis

    for a in ax.values():
        pos = a.get_position()          # Bbox in figure-fraction coords
        new_pos = [
            pos.x0,
            pos.y0 * (1 - top_margin - gap),   # compress y downward
            pos.width,
            pos.height * (1 - top_margin - gap)
        ]
        a.set_position(new_pos)

    # 2. Create the MIS axis spanning the full width of the plot area
    # Get the exact x bounds from an existing stackplot axis
    ref_ax = list(ax.values())[0]
    ref_pos = ref_ax.get_position()

    # Get the data x-limits and transform to figure coordinates
    # This accounts for any internal padding/margins
    x0_disp, _ = ref_ax.transAxes.transform((0, 0))   # left edge in display coords
    x1_disp, _ = ref_ax.transAxes.transform((1, 0))   # right edge in display coords

    # Convert display coords to figure-fraction coords
    fig_width, fig_height = fig.get_size_inches() * fig.dpi
    x0_fig = x0_disp / fig_width
    x1_fig = x1_disp / fig_width

    mis_ax = fig.add_axes([
        x0_fig,               # exact same left edge
        1 - top_margin,
        x1_fig - x0_fig,      # exact same width
        top_margin - gap
    ])

    # Make sure the MIS axis x-limits match the stackplot x-limits exactly
    mis_ax.set_xlim(ref_ax.get_xlim())

    for start, end, label, state in bounds_probstack:
        if start <= xlim and state == 1:
            mis_ax.axvspan(
                start, end,
                facecolor='red',
                edgecolor=None,
                alpha=0.2
            )
            midpoint = (start + end) / 2
            if midpoint <= xlim:
                mis_ax.text(
                    midpoint, 0.5, label,
                    ha='center', va='center',
                    fontsize=8, rotation=90
                )
        elif start <= xlim and state == 0:
            mis_ax.axvspan(
                start, end,
                facecolor='blue',
                edgecolor=None,
                alpha=0.2
            )
            midpoint = (start + end) / 2
            if midpoint <= xlim:
                mis_ax.text(
                    midpoint, 0.5, label,
                    ha='center', va='center',
                    fontsize=8, rotation=90
                )

    # 4. Clean up the MIS axis appearance
    mis_ax.set_xticks([])          # no x ticks (shared with stackplot below)
    mis_ax.set_yticks([])          # no y ticks needed
    mis_ax.set_ylabel('MIS', fontsize=8, rotation=0, labelpad=20, va='center')
    for spine in ['top', 'right', 'left', 'bottom']:
        mis_ax.spines[spine].set_visible(False)


for a in ax.values():   
    a.spines['top'].set_visible(False)


# Save the figure
fig.savefig("/home/pollakf/Documents/Paper/Pollak_2026/Plots/Terrestrial-plots.pdf", bbox_inches='tight')    

# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
# GET STATS OF RECORDS FOR PAPER
for i, record in enumerate(all_metrics):
    print(f'----------------------------------\nRecord {i+1}:')
    record_name = df[record].loc[0,'name']
    record_t = df[record].loc[:,'age']
    old_t_max = np.nanmax(record_t)
    # get age between 0 and 1.5 Ma
    record_t = record_t[np.logical_and(record_t>=0, record_t<=1500)]
    print(f"{record_name}: Mean temp. resolution={np.nanmean(np.diff(record_t)):.1f} kyr, t_max={np.nanmax(record_t)}, t_min={np.nanmin(record_t)}, old t_max={old_t_max}")
    
    

# -------------------------------------------------------------------------------------------------------
# CREATE GLOBAL MAP WITH LOCATIONS OF TERRESTRIAL RECORDS

serieslist = []
selected_metric = metrics_terrestrial
value_names = ['Loess (norm.)', 'Loess (μm)', 'Loess (μm)', 'δ13C (‰)', 'MAP (mm/day)', 'MAT (°C)', 'MAT (°C)', 
                'AP (%)', 'AP (%)', 'AP (%)', 'AP (%)', 'Si/Ti', 'BioSi (%)', 'Ca/K']
coords = {
    'labels': ['Chiloparts (CLP stack)', 'Gulang Loess', 'Jingyuan Loess', 'Zoige Basin', 'Tenaghi Phillippon', 
                'Lake Ohrid', 'Bogota Basin (Funza09)', "Lake El'gygytgyn", 'Lake Baikal'],
    'lats': [35.36, 37.50, 36.35, 33.97, 41.17, 41.05, 4.83, 67.5, 53.7],
    'lons': [107.93, 102.88, 104.6, 102.33, 24.33, 20.72, -74.2, 172.1, 108.35],
    'archiveType': ["Loess", "Loess", "Loess", "Lake", "Pollen", "Lake", "Pollen", "Lake", "Lake"], 
    'observationTypes': ["Loess", "Loess", "Loess", "Lake", "Pollen", "Lake", "Pollen", "Lake", "Lake"],
    }

marker_map = {
    "Loess": "o",
    "Lake": "s",
    "Pollen": "^"
}

for i, metric in enumerate(selected_metric):
    if i < 9:
        gs = pyleo.GeoSeries(time=df[metric]['age'], value=df[metric]['data'], time_name='Age (ka)', time_unit='ka', 
                              value_name=value_names[i], label=coords['labels'][i], lat=coords['lats'][i], lon=coords['lons'][i], 
                              archiveType=coords['archiveType'][i], observationType=coords['observationTypes'][i])
        
        serieslist.append(gs)    


geo_ms = pyleo.MultipleGeoSeries(serieslist)

fig, ax = geo_ms.map(
    # projection="Robinson",
    projection="Robinson",
    proj_default={"central_longitude": 10},
    scatter_kwargs={
        "s": 150,        # instead of 150
        # "edgecolor": "k",
        # "linewidth": 0.5,
        # "zorder": 5,
    },
    hue="label",
    legend=True,
    marker="label",
)

legend_handles = ax["map"].get_legend_handles_labels()

cmap = {}
marker_dict = {}

for idx, handle in enumerate(legend_handles[0]):
    cmap[legend_handles[1][idx]] = handle._color
    marker_dict[legend_handles[1][idx]] = handle._marker

legend = ax["map"].legend(
            loc="center right",
            bbox_to_anchor=(1.4, 0.52),
            title="Terrestrial records",
            title_fontsize=14,        # font size of the legend title
            prop={'size': 12}  # font size and weight of legend labels
        )
legend.get_title().set_fontweight('bold')  # make only the title bold


ax["leg"].legend().remove

plt.savefig('/home/pollakf/Documents/Paper/Pollak_2026/Plots/Map-terrestrial-records.pdf', bbox_inches='tight')


# -----------------------------------------------------------------------------
# Display Resolution and data gaps
for metric in all_metrics:
    age = df[metric]['age']
    age = age[age<=1500]
    diff_age = np.diff(age)
    mean_res = np.nanmean(diff_age)
    min_gap = np.nanmin(diff_age)     
    max_gap = np.nanmax(diff_age)

    print(f"Mean res={mean_res:.1f} kyr, Min gap={min_gap:.1f} kyr, Max gap={max_gap:.1f}kyr")

