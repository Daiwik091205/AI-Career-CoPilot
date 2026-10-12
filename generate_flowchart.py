"""
generate_flowchart.py
Numerical Python script to programmatically render the publication-grade
system methodology flowchart using Matplotlib vector graphics.
Outputs: methodology_flowchart.png (300 DPI high resolution).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_flowchart(output_filename="methodology_flowchart.png"):
    # Set high-resolution canvas with a 16:9 aspect ratio
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")
    ax.axis("off")

    # Define stage data: (title, subtitle, y_center, edge_color, fill_color)
    stages = [
        (
            "STUDENT PROFILE + PROJECTS",
            "Input Layer: Academic Details, Projects, Stated Skills",
            8.4,
            "#1976D2",
            "#F0F7FF"
        ),
        (
            "LLM SKILL DECONSTRUCTION",
            "Gemini / OpenAI Natural Language Parsing & Skill Extraction",
            6.8,
            "#7B1FA2",
            "#FBF0FF"
        ),
        (
            "ONTOLOGY ALIGNMENT ENGINE",
            "Career Target Mapping vs. 8 Industry Role Taxonomies",
            5.2,
            "#512DA8",
            "#F3EFFF"
        ),
        (
            "CONSTRAINED OPTIMIZATION FORMULATION",
            r"Mathematical Readiness Score: $\Phi = 0.45 C_{skill} + 0.25 S_{proj} + 0.15 S_{dsa} + 0.15 \bar{I}_{norm}$",
            3.6,
            "#00796B",
            "#E0F2F1"
        ),
        (
            "AST-SANDBOXED CODING & INTERVIEW DRILLS",
            "Safe Local Python Execution, 14 DSA Topics, STAR Mock Interview Drills",
            2.0,
            "#0288D1",
            "#E1F5FE"
        ),
        (
            "CLOSED-LOOP ADAPTIVE RECALIBRATION",
            "Dynamic Milestone Mutation & Real-Time Curriculum Adaptation",
            0.5,
            "#0D47A1",
            "#E8EAF6"
        )
    ]

    box_width = 8.8
    box_height = 0.95
    x_center = 6.0

    # Draw nodes
    for title, subtitle, y, edge_c, fill_c in stages:
        rect = patches.FancyBboxPatch(
            (x_center - box_width / 2, y - box_height / 2),
            box_width,
            box_height,
            boxstyle="round,pad=0.2,rounding_size=0.18",
            linewidth=2.4,
            edgecolor=edge_c,
            facecolor=fill_c,
            zorder=3
        )
        ax.add_patch(rect)

        # Main Title Text
        ax.text(
            x_center,
            y + 0.14,
            title,
            fontsize=12.5,
            fontweight="bold",
            color="#1A202C",
            ha="center",
            va="center",
            zorder=4
        )

        # Subtitle Text
        ax.text(
            x_center,
            y - 0.18,
            subtitle,
            fontsize=9.5,
            color="#4A5568",
            ha="center",
            va="center",
            zorder=4
        )

    # Draw sequential downward arrows between consecutive blocks
    arrow_props = dict(
        arrowstyle="-|>",
        color="#1A202C",
        linewidth=2.2,
        mutation_scale=18,
        zorder=2
    )

    for i in range(len(stages) - 1):
        y_from = stages[i][2] - box_height / 2 - 0.05
        y_to = stages[i + 1][2] + box_height / 2 + 0.08
        ax.annotate(
            "",
            xy=(x_center, y_to),
            xytext=(x_center, y_from),
            arrowprops=arrow_props
        )

    # Draw closed-loop feedback loop from Stage 6 back to Stage 4
    y_rec = stages[5][2]
    y_opt = stages[3][2]
    left_x = x_center - box_width / 2 - 0.7
    right_x = x_center + box_width / 2 + 0.7

    # Left loop: Stage 6 left edge -> out -> up -> into Stage 4 left edge
    ax.annotate(
        "",
        xy=(x_center - box_width / 2 - 0.02, y_opt),
        xytext=(x_center - box_width / 2 - 0.02, y_rec),
        arrowprops=dict(
            arrowstyle="-|>",
            connectionstyle="angle,angleA=-180,angleB=90,rad=10",
            color="#00796B",
            linewidth=2.4,
            mutation_scale=16,
            zorder=2
        )
    )
    ax.text(
        left_x - 0.15,
        (y_rec + y_opt) / 2,
        "Recalibration Loop\n(Progress Feedback)",
        fontsize=8.5,
        color="#00796B",
        fontweight="semibold",
        ha="right",
        va="center",
        rotation=90
    )

    # Right loop: Stage 6 right edge -> out -> up -> into Stage 4 right edge
    ax.annotate(
        "",
        xy=(x_center + box_width / 2 + 0.02, y_opt),
        xytext=(x_center + box_width / 2 + 0.02, y_rec),
        arrowprops=dict(
            arrowstyle="-|>",
            connectionstyle="angle,angleA=0,angleB=90,rad=10",
            color="#00796B",
            linewidth=2.4,
            mutation_scale=16,
            zorder=2
        )
    )
    ax.text(
        right_x + 0.15,
        (y_rec + y_opt) / 2,
        "Adaptive Path Mutation\n(Score Feedback)",
        fontsize=8.5,
        color="#00796B",
        fontweight="semibold",
        ha="left",
        va="center",
        rotation=-90
    )

    # Set axis boundaries
    ax.set_xlim(0, 12)
    ax.set_ylim(-0.3, 9.4)

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[OK] High-resolution flowchart saved to {output_filename}")

if __name__ == "__main__":
    generate_flowchart()
