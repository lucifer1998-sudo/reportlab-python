import matplotlib.pyplot as plt
import numpy as np

# ----- JSON DATA -----
data = [
    {"competency": "Integrity", "score": 4.8, "benchmark": 4.4},
    {"competency": "Problem Solving", "score": 4.5, "benchmark": 4.2},
    {"competency": "Interpersonal Skills", "score": 4.2, "benchmark": 4.3},
    {"competency": "Flexibility", "score": 4.2, "benchmark": 4.3},
    {"competency": "Customer Service", "score": 4.2, "benchmark": 4.3},
    {"competency": "Accountability", "score": 4.3, "benchmark": 4.3},
    {"competency": "Oral Communication", "score": 4.3, "benchmark": 4.3},
    {"competency": "Resilience", "score": 4.3, "benchmark": 4.3},
    {"competency": "Decisiveness", "score": 4.0, "benchmark": 4.2},
    {"competency": "Written Communication", "score": 4.2, "benchmark": 4.2},
    {"competency": "Organizational Engagement", "barColor": "lightblue", "score": 4.2, "benchmark": 4.3},
    {"competency": "Proactive Personality", "barColor": "lightblue", "score": 3.9, "benchmark": 4.2},
    {"competency": "Leadership Confidence", "barColor": "lightblue", "score": 4.8, "benchmark": 4.4},
    {"competency": "Motivation to Lead", "barColor": "lightblue", "score": 4.5, "benchmark": 4.2}
]

# ----- Prepare Data -----
competencies = [item["competency"] for item in data]
scores = [item["score"] for item in data]
benchmarks = [item["benchmark"] for item in data]

# Colors
bar_colors = []
for item in data:
    if item.get("barColor") == "lightblue":
        bar_colors.append("#AEC6CF")  # light blue
    else:
        bar_colors.append("#1F3A5F")  # dark blue

y_pos = np.arange(len(competencies))

# ----- Create Plot -----
fig, ax = plt.subplots(figsize=(9, 8))

bars = ax.barh(y_pos, scores, color=bar_colors, edgecolor='none')

# Add benchmark markers
ax.scatter(benchmarks, y_pos, marker='D', color='darkorange', s=80, label='Benchmark')

# X-axis
ax.set_xlim(1, 5)
ax.set_xticks(range(1, 6))

# ----- X-axis labels on TOP -----
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')

# Adjust tick appearance
ax.tick_params(axis='x', which='both', direction='out', length=5, width=1.5, top=True, bottom=False)

ax.invert_yaxis()  # Highest score on top

# Remove plot borders except top spine
for spine in ['bottom', 'left', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['top'].set_visible(True)
ax.spines['top'].set_linewidth(1.5)

# Remove Y ticks
ax.set_yticks(y_pos)  # We still need y-ticks to align labels
ax.set_yticklabels(competencies, fontsize=12, weight='bold')
ax.tick_params(axis='y', length=0)  # Removes tick lines
ax.tick_params(axis='y', which='both', left=False)  # No ticks at all

# Grid lines
# ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.5)

# Score and benchmark values at the right
for i, (score, benchmark) in enumerate(zip(scores, benchmarks)):
    ax.text(5.05, i, f"{score:.1f}", va='center', ha='left', fontsize=12)
    ax.text(5.3, i, f"{benchmark:.1f}", va='center', ha='left', fontsize=12)

# ----- Legend -----
from matplotlib.patches import Patch

legend_elements = [
    Patch(facecolor="#1F3A5F", label='Competencies'),
    Patch(facecolor="#AEC6CF", label='Motivational/Personal'),
    plt.Line2D([0], [0], marker='D', color='w', label='Benchmark',
               markerfacecolor='darkorange', markersize=10)
]
# fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=3, labelspacing=1.5, frameon=False, handletextpad=2)
# plt.subplots_adjust(bottom=0.2)

# ----- Custom Legend -----
legend_y = -0.08  # Adjust as needed
spacing = 0.3  # Horizontal spacing between legend items

# First item - Competencies
ax.scatter(0.2, legend_y, marker='s', s=200, color="#1F3A5F", transform=ax.transAxes, clip_on=False)
ax.text(0.2, legend_y - 0.05, "Competencies", ha='center', va='top', fontsize=11, transform=ax.transAxes)

# Second item - Motivational/Personal
ax.scatter(0.5, legend_y, marker='s', s=200, color="#AEC6CF", transform=ax.transAxes, clip_on=False)
ax.text(0.5, legend_y - 0.05, "Motivational/Personal", ha='center', va='top', fontsize=11, transform=ax.transAxes)

# Third item - Benchmark
ax.scatter(0.8, legend_y, marker='D', s=80, color="darkorange", transform=ax.transAxes, clip_on=False)
ax.text(0.8, legend_y - 0.05, "Benchmark", ha='center', va='top', fontsize=11, transform=ax.transAxes)

plt.tight_layout(rect=[0, 0.15, 1, 1])

# ----- Titles -----
# ax.set_xlabel('')
# ax.set_title('Average of All Raters vs Benchmark', fontsize=14, weight='bold')

plt.savefig("score_summary_chart.png", dpi=300, bbox_inches='tight')
plt.show()