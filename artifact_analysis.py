# coding: utf-8
"""
Quick script to analyse what different artifacts there are in the script.

Artifacts are two digit hexadecimal numbers with curly braces, such as `{00}`
and `{1E}`.
"""
import re


with open('data/script.txt') as f:
    script = f.read()


artifact_counts = {}

for artifact in re.findall(r'{..}', script):
    try:
        artifact_counts[artifact] += 1
    except KeyError:
        artifact_counts[artifact] = 1


with open('artifact_analysis.csv', 'w') as f:
    f.write('artifact,count\n')
    for k, v in artifact_counts.items():
        f.write(f"{k},{v}\n")
