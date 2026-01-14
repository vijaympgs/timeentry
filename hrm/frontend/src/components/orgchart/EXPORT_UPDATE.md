# Export PDF and Zoom Updates

## ✅ Key Features Added
1.  **Export as PDF**:
    - Added an **"Export PDF" button** to the toolbar.
    - When clicked, it captures the **entire organizational chart** (even parts not currently visible on screen) and saves it as `organizational-chart.pdf`.
    - Supports high-quality capture (2x scale).

2.  **Enhanced Zoom**:
    - Zoom Out limit extended to **10%** (0.1x scale) as requested.
    - Allows viewing the entire massive Level 6 hierarchy in one view.

## 📦 Dependencies Installed
- `html2canvas`: For capturing the DOM.
- `jspdf`: For generating the PDF file.

## How to Verify
1.  **Zoom Out**: Click the `(-)` zoom button repeatedly until it reaches **10%**.
2.  **Export**: Click the **"Export PDF"** button (with Download icon). 
    - Wait a moment for generation ("Exporting...").
    - A PDF file will download containing the full chart.

---
**Status**: ✅ **Implemented**
