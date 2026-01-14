# PowerShell script to commit Org Chart changes
# Run this from the repository root

git add hrm/frontend/src/components/orgchart/VirtualOrgChart.tsx
git add hrm/frontend/src/components/orgchart/useVirtualTree.ts
git add hrm/frontend/src/components/orgchart/orgChart.virtual.css
git add hrm/backend/hrm/management/commands/distribute_all_levels.py
git add hrm/backend/hrm/management/commands/distribute_l6_to_l5.py
git add hrm/frontend/package.json
git add hrm/frontend/package-lock.json

git commit -m "feat(org-chart): complete implementation (virtualization, layout, pdf export, data balancing)"

# Uncomment the following line to push automatically if remote is configured
# git push
