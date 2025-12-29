# 🎬 Demo Video / GIF Storyboard

Follow this script to create a compelling 30-60 second demo video for your portfolio.

## 🛠️ Setup
1.  Open **VS Code** with the terminal visible.
2.  Open **Browser** with Dashboard (`http://localhost:8501`) side-by-side or in a separate window.
3.  Ensure Docker containers are running.

## 🎥 Scene 1: The "Problem" (0:00 - 0:10)
*   **Visual**: Show the Dashboard with empty or low stats.
*   **Narrator/Text**: "Handling support emails manually is slow and expensive. Let's automate it."

## 🎥 Scene 2: The AI in Action (0:10 - 0:30)
*   **Action**: Switch to Terminal. Run the simulation script:
    ```bash
    python scripts/simulate_email.py
    ```
*   **Action**: Select option `1` (Order Status).
*   **Visual**: Show the terminal output: `✅ Simulated email sent!`.
*   **Action**: Quickly switch to the Dashboard.
*   **Visual**: Watch the **"Emails Today"** counter jump up. Watch the **"Recent Activity"** table update with the new email and status "Replied".
*   **Narrator/Text**: "The AI instantly analyzes the email, searches the knowledge base, and drafts a reply. Zero latency."

## 🎥 Scene 3: Handling Spam (0:30 - 0:40)
*   **Action**: Run simulation again. Select option `2` (Spam).
*   **Visual**: Dashboard updates. Status shows **"Ignored"**.
*   **Narrator/Text**: "It even filters out spam automatically, saving your team's focus."

## 🎥 Scene 4: The Analytics (0:40 - 0:50)
*   **Action**: Scroll down to the charts (Emails per Hour, Success Rate).
*   **Visual**: Hover over the charts.
*   **Narrator/Text**: "Full visibility into your support operations with real-time analytics."

## 🎥 Scene 5: Conclusion (0:50 - 1:00)
*   **Visual**: Show the GitHub repo or the `VALUE_PROPOSITION.md` title.
*   **Narrator/Text**: "100% Local. Privacy-First. Production Ready."

---
**💡 Tip**: Use a tool like **OBS Studio** (free) to record, or **ScreenToGif** for a lightweight GIF.
