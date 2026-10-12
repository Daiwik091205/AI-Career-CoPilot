"""
generate_algorithm_flowchart.py
Generates a publication-grade, high-legibility block flow diagram for:
Algorithm 1: Dynamic Roadmap Synthesis and Pruning
Optimized for 2-column IEEE conference paper rendering as well as high-res artifact display.
Outputs: algorithm_flowchart.png (300 DPI high resolution).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_algorithm_flowchart(output_path="algorithm_flowchart.png"):
    # Aspect ratio calibrated for publication readability (9.5 x 10.2 inches at 300 DPI)
    fig, ax = plt.subplots(figsize=(9.5, 10.5), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.axis("off")
    ax.set_xlim(0, 9.5)
    ax.set_ylim(0, 10.5)

    cx = 4.45  # central spine alignment axis

    # Draw rounded rectangular container block
    def draw_card(x, y, w, h, border_color, bg_color, title, subtitle="", badge="", title_bg=None, title_color="#FFFFFF"):
        hdr_bg = title_bg if title_bg else border_color
        # Outer Card
        card = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.14",
            facecolor=bg_color, edgecolor=border_color, linewidth=1.8, zorder=3
        )
        ax.add_patch(card)

        # Header bar
        hdr_h = 0.38
        hdr = patches.FancyBboxPatch(
            (x + 0.02, y + h - hdr_h - 0.02), w - 0.04, hdr_h,
            boxstyle="round,pad=0.05,rounding_size=0.10",
            facecolor=hdr_bg, edgecolor="none", zorder=4
        )
        ax.add_patch(hdr)

        # Optional Badge on left
        badge_right = x
        if badge:
            badge_w = 0.90
            badge_h = 0.25
            badge_x = x + 0.12
            badge_patch = patches.FancyBboxPatch(
                (badge_x, y + h - hdr_h / 2 - badge_h / 2 - 0.02), badge_w, badge_h,
                boxstyle="round,pad=0.03,rounding_size=0.08",
                facecolor="#FFFFFF", edgecolor="none", zorder=6
            )
            ax.add_patch(badge_patch)
            ax.text(badge_x + badge_w / 2, y + h - hdr_h / 2 - 0.02, badge,
                    fontsize=8.0, fontweight="bold", color=hdr_bg, ha="center", va="center", family="sans-serif", zorder=7)
            badge_right = badge_x + badge_w

        # Title text (centered across remaining space to right of badge)
        title_cx = (badge_right + 0.10 + x + w) / 2 if badge else (x + w / 2)
        ax.text(title_cx, y + h - hdr_h / 2 - 0.02, title,
                fontsize=10.6, fontweight="bold", color=title_color, ha="center", va="center", family="sans-serif", zorder=5)

        # Subtitle/Body text inside card
        if subtitle:
            ax.text(x + w / 2, y + (h - hdr_h) / 2 - 0.01, subtitle,
                    fontsize=9.8, color="#1E293B", ha="center", va="center", family="sans-serif", zorder=5)

    def draw_step_badge(x, y, text, color="#2563EB", bg="#EFF6FF"):
        pill = patches.FancyBboxPatch(
            (x - 0.55, y - 0.13), 1.10, 0.26,
            boxstyle="round,pad=0.04,rounding_size=0.10",
            facecolor=bg, edgecolor=color, linewidth=1.2, zorder=8
        )
        ax.add_patch(pill)
        ax.text(x, y, text, fontsize=8.5, fontweight="bold", color=color, ha="center", va="center", family="sans-serif", zorder=9)

    def draw_arrow(x1, y1, x2, y2, color="#2563EB", lw=2.0):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>", color=color, lw=lw,
                mutation_scale=14, shrinkA=0, shrinkB=0
            ), zorder=6
        )

    # =========================================================================
    # 1. INPUT BLOCK
    # =========================================================================
    w_main = 7.8
    x_main = cx - w_main / 2  # 0.55
    y_input = 9.35
    h_input = 0.95
    draw_card(
        x_main, y_input, w_main, h_input,
        border_color="#1E3D7B", bg_color="#F0F4FC",
        title="INPUT: CANDIDATE PROFILE & TARGET SPECIFICATION",
        subtitle="• Candidate Profile (S_user) with proficiency tiers  |  • Target Track Requirements (R_target)\n• Current Active 4-Phase Chronological Roadmap (M)",
        badge="INPUT", title_bg="#1E3D7B"
    )

    # Connector to Step 1
    draw_arrow(cx, y_input, cx, y_input - 0.45)
    draw_step_badge(cx, y_input - 0.225, "Step 1")

    # =========================================================================
    # 2. STEP 1: DEFICIT VECTOR
    # =========================================================================
    y_s1 = y_input - 0.45 - 0.95  # 7.95
    h_s1 = 0.95
    draw_card(
        x_main, y_s1, w_main, h_s1,
        border_color="#0D8070", bg_color="#E6F5F3",
        title=r"STEP 1: COMPUTE SKILL DEFICIT VECTOR  $\mathbf{\Delta}$",
        subtitle=r"$\mathbf{\Delta = R_{target} \setminus \{ s \in S_{user} \mid \omega(p_s) \geq 0.75 \}}$" + "\nFilters unverified claims (ω < 0.75 discounted) to identify hiring readiness gaps",
        badge="STEP 1", title_bg="#0D8070"
    )

    # Connector to Step 2
    draw_arrow(cx, y_s1, cx, y_s1 - 0.45)
    draw_step_badge(cx, y_s1 - 0.225, "Step 2")

    # =========================================================================
    # 3. STEP 2: DEPENDENCY TIER PARTITIONING
    # =========================================================================
    y_s2 = y_s1 - 0.45 - 0.98  # 6.52
    h_s2 = 0.98
    draw_card(
        x_main, y_s2, w_main, h_s2,
        border_color="#6A1B9A", bg_color="#F7EFFD",
        title="STEP 2: PARTITION DEFICIT ACROSS 4 DEPENDENCY TIERS (DAG)",
        subtitle="Tier 1: Foundations (Core Language & Syntax)  →  Tier 2: Frameworks (APIs & SQL Data)\nTier 3: Distributed Systems (Brokers & Cloud)  →  Tier 4: Production Capstone (DevOps)",
        badge="STEP 2", title_bg="#6A1B9A"
    )

    # Connector to Step 3 Loop
    draw_arrow(cx, y_s2, cx, y_s2 - 0.45)
    draw_step_badge(cx, y_s2 - 0.225, "Step 3")

    # =========================================================================
    # 4. STEP 3: PHASE MUTATION LOOP CONTAINER
    # =========================================================================
    y_s3 = 2.45
    h_s3 = 3.62
    w_s3 = 8.4
    x_s3 = cx - w_s3 / 2  # 0.25

    # Outer Dashed Container
    container = patches.FancyBboxPatch(
        (x_s3, y_s3), w_s3, h_s3,
        boxstyle="round,pad=0.08,rounding_size=0.18",
        facecolor="#F8FAFC", edgecolor="#2563EB", linewidth=1.8, linestyle="--", zorder=2
    )
    ax.add_patch(container)

    # Container Header Bar
    cont_hdr_h = 0.38
    cont_hdr = patches.FancyBboxPatch(
        (x_s3 + 0.03, y_s3 + h_s3 - cont_hdr_h - 0.03), w_s3 - 0.06, cont_hdr_h,
        boxstyle="round,pad=0.05,rounding_size=0.12",
        facecolor="#1E3D7B", edgecolor="none", zorder=3
    )
    ax.add_patch(cont_hdr)
    ax.text(cx, y_s3 + h_s3 - cont_hdr_h / 2 - 0.03,
            r"STEP 3: FOR EACH PHASE $P_k$ IN ROADMAP $M$ (Iterate $k \in \{1, 2, 3, 4\}$)",
            fontsize=11.5, fontweight="bold", color="#FFFFFF", ha="center", va="center", family="sans-serif", zorder=5)

    # Sub-steps inside container
    w_sub = 6.8
    x_sub = x_s3 + 0.35  # leaves room on right for loopback line
    cx_sub = x_sub + w_sub / 2  # 4.10

    # Sub-step 3A: Prune
    y_3a = y_s3 + 2.25
    h_sub = 0.82
    draw_card(
        x_sub, y_3a, w_sub, h_sub,
        border_color="#B71C1C", bg_color="#FDF2F2",
        title=r"3A: PRUNE MASTERED MILESTONES  $(m.skill \notin \mathbf{\Delta})$",
        subtitle="Purge mastered/completed competencies from Phase schedule to prevent stagnation",
        badge="PRUNE", title_bg="#B71C1C"
    )

    # Arrow 3A -> 3B
    draw_arrow(cx_sub, y_3a, cx_sub, y_3a - 0.26)

    # Sub-step 3B: Populate
    y_3b = y_3a - 0.26 - h_sub  # 1.17 + 2.45 - ...
    draw_card(
        x_sub, y_3b, w_sub, h_sub,
        border_color="#0D8070", bg_color="#E6F5F3",
        title=r"3B: INJECT REQUISITE TIER_$k$ DEFICIT COMPETENCIES",
        subtitle=r"Populate $P_k$ with unblocked skills matching candidate's dependency clearance",
        badge="INJECT", title_bg="#0D8070"
    )

    # Arrow 3B -> 3C
    draw_arrow(cx_sub, y_3b, cx_sub, y_3b - 0.26)

    # Sub-step 3C: Link Drills
    y_3c = y_3b - 0.26 - h_sub
    draw_card(
        x_sub, y_3c, w_sub, h_sub,
        border_color="#BF360C", bg_color="#FDF3E7",
        title=r"3C: LINK AST CODING DRILLS & STAR MOCK INTERVIEWS",
        subtitle=r"Attach unit-tested DSA problems & rubric-driven oral interviews to Phase $P_k$",
        badge="LINK", title_bg="#BF360C"
    )

    # Dedicated Loopback Channel on Right
    x_loop = x_s3 + w_s3 - 0.40  # 8.25
    y_start_loop = y_3c + h_sub / 2
    y_end_loop = y_3a + h_sub / 2

    # Draw loopback lines: Right from 3C, Up, Left into 3A
    ax.plot([x_sub + w_sub, x_loop, x_loop, x_sub + w_sub],
            [y_start_loop, y_start_loop, y_end_loop, y_end_loop],
            color="#2563EB", lw=2.0, zorder=6)
    # Arrow head pointing into 3A
    ax.annotate(
        "", xy=(x_sub + w_sub, y_end_loop), xytext=(x_sub + w_sub + 0.15, y_end_loop),
        arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=2.0, mutation_scale=14), zorder=7
    )
    # Loop Badge
    pill_loop = patches.FancyBboxPatch(
        (x_loop - 0.50, (y_start_loop + y_end_loop) / 2 - 0.22), 1.00, 0.44,
        boxstyle="round,pad=0.04,rounding_size=0.10",
        facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=1.2, zorder=8
    )
    ax.add_patch(pill_loop)
    ax.text(x_loop, (y_start_loop + y_end_loop) / 2 + 0.05, "Next Phase",
            fontsize=8.5, fontweight="bold", color="#1D4ED8", ha="center", va="center", family="sans-serif", zorder=9)
    ax.text(x_loop, (y_start_loop + y_end_loop) / 2 - 0.11, r"($k \leftarrow k+1$)",
            fontsize=8.0, color="#1D4ED8", ha="center", va="center", family="sans-serif", zorder=9)

    # Exit arrow from Step 3 container to Step 4
    draw_arrow(cx, y_s3, cx, y_s3 - 0.45)
    pill_exit = patches.FancyBboxPatch(
        (cx - 0.80, y_s3 - 0.32), 1.60, 0.24,
        boxstyle="round,pad=0.03,rounding_size=0.08",
        facecolor="#EFF6FF", edgecolor="#1D4ED8", linewidth=1.0, zorder=8
    )
    ax.add_patch(pill_exit)
    ax.text(cx, y_s3 - 0.20, "All 4 Phases Updated",
            fontsize=8.2, fontweight="bold", color="#1D4ED8", ha="center", va="center", family="sans-serif", zorder=9)

    # =========================================================================
    # 5. STEP 4: RECALCULATE READINESS
    # =========================================================================
    y_s4 = y_s3 - 0.42 - 0.90  # 1.13
    h_s4 = 0.90
    draw_card(
        x_main, y_s4, w_main, h_s4,
        border_color="#0D8070", bg_color="#E6F5F3",
        title=r"STEP 4: RECALCULATE GLOBAL READINESS INDEX  $\mathbf{\Phi_{readiness}}$",
        subtitle=r"$\mathbf{\Phi_{readiness} = 0.45 \cdot C_{skill} + 0.25 \cdot S_{project} + 0.15 \cdot S_{dsa} + 0.15 \cdot \bar{I}_{norm}}$" + "\nClosed-form multi-factor evaluation updates candidate's overall readiness (0–100%)",
        badge="STEP 4", title_bg="#0D8070"
    )

    # Connector to Output
    draw_arrow(cx, y_s4, cx, y_s4 - 0.32)
    draw_step_badge(cx, y_s4 - 0.16, "Step 5")

    # =========================================================================
    # 6. OUTPUT BLOCK
    # =========================================================================
    y_out = 0.15
    h_out = 0.66
    draw_card(
        x_main, y_out, w_main, h_out,
        border_color="#1E3D7B", bg_color="#F0F4FC",
        title=r"OUTPUT: UPDATED 4-PHASE MILESTONE SCHEDULE  $\mathbf{M'}$",
        subtitle=r"Personalized, unblocked, non-redundant roadmap ready for real-time dashboard execution",
        badge="OUTPUT", title_bg="#1E3D7B"
    )

    plt.tight_layout(pad=0.2)
    plt.savefig(output_path, dpi=300, facecolor="#FFFFFF", bbox_inches="tight")
    plt.close()
    print(f"[FLOWCHART SAVED] {output_path}")

if __name__ == "__main__":
    create_algorithm_flowchart()
