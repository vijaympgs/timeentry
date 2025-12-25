# HRM Task List (15.Tasks&Templates)

## Overview
This task list drives the execution of HRM screens using the standardized template
library defined in the companion files:

- **02HRM_Template_Mapping.md** – mapping of every screen to its template type (T1‑T10)  
- **03HRM_Template_Task_details.md** – detailed, reusable task lists for each template

All agents should use this file as the entry point for locating and running a specific
screen's implementation tasks.

---

## 📌 How an agent should run a task

> **Command pattern (conceptual)**  
> `Run <Screen‑ID> from <Task‑List‑Path>`

*Example for the Employee Directory screen:*

```
Run 1.1 Employee Directory from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

When an agent receives the above command it must:

1. **Locate the screen in the mapping file** (`02HRM_Template_Mapping.md`) to determine the
   applicable template (Employee Directory → **T1 – Master Management Template**).
2. **Open the detailed task list** (`03HRM_Template_Task_details.md`) and extract the
   section titled **"T1. MASTER MANAGEMENT TEMPLATE"**.
3. **Execute the tasks** in the order defined under the eight standard headings
   (Layout & Navigation, UI Components, Toolbar & Actions, CRUD & Data Operations,
   Generic Business Validation, Workflow & State, Security & Governance, Non‑Functional).
4. **Mark progress** in the appropriate sub‑task checklist (e.g., `- [x] Create data grid`).

---

## ✅ Current Tasks

### 1️⃣ 1.1 Employee Directory  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** See **02HRM_Template_Mapping.md** (row "Employee Directory → T1")  
- **Task Details:** See **03HRM_Template_Task_details.md**, section **"T1. MASTER MANAGEMENT TEMPLATE"**  

**Execution command for any agent:**  

```
Run 1.1 Employee Directory from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

*(Agents should follow the four‑step process described above.)*

### 2️⃣ 1.2 Organizational Chart  *(Master Management – T1)*
- **Template:** T1  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 1.2 Organizational Chart from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 3️⃣ 1.3 Employee Self‑Service  *(Self‑Service – T4)*
- **Template:** T4 – Employee Self‑Service Template  
- **Reference:** 02HRM_Template_Mapping.md → T4  
- **Task Details:** 03HRM_Template_Task_details.md → T4  

**Execution command:**  

```
Run 1.3 Employee Self-Service from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 4️⃣ 1.4 Document Management  *(Document/Repository – T7)*
- **Template:** T7 – Document Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T7  
- **Task Details:** 03HRM_Template_Task_details.md → T7  

**Execution command:**  

```
Run 1.4 Document Management from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 5️⃣ 1.5 Employee Lifecycle  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 1.5 Employee Lifecycle from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 0. HR Dashboard

### 0️⃣ 0.1 HR Dashboard Overview  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 0.1 HR Dashboard Overview from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 2. Talent Acquisition

### 2.1 Job Requisitions  *(Workflow – T3)*
- **Template:** T3 – Workflow Orchestration Template  
- **Reference:** 02HRM_Template_Mapping.md → T3  
- **Task Details:** 03HRM_Template_Task_details.md → T3  

**Execution command:**  

```
Run 2.1 Job Requisitions from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 2.2 Candidate Management  *(Transaction – T2)*
- **Template:** T2 – Transaction Entry Template  
- **Reference:** 02HRM_Template_Mapping.md → T2  
- **Task Details:** 03HRM_Template_Task_details.md → T2  

**Execution command:**  

```
Run 2.2 Candidate Management from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 2.3 Interview Scheduling  *(Workflow – T3)*
- **Template:** T3 – Workflow Orchestration Template  
- **Reference:** 02HRM_Template_Mapping.md → T3  
- **Task Details:** 03HRM_Template_Task_details.md → T3  

**Execution command:**  

```
Run 2.3 Interview Scheduling from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 2.4 Offer Management  *(Workflow – T3)*
- **Template:** T3 – Workflow Orchestration Template  
- **Reference:** 02HRM_Template_Mapping.md → T3  
- **Task Details:** 03HRM_Template_Task_details.md → T3  

**Execution command:**  

```
Run 2.4 Offer Management from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 2.5 Onboarding  *(Workflow – T3)*
- **Template:** T3 – Workflow Orchestration Template  
- **Reference:** 02HRM_Template_Mapping.md → T3  
- **Task Details:** 03HRM_Template_Task_details.md → T3  

**Execution command:**  

```
Run 2.5 Onboarding from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 3. Compensation & Payroll

### 3.1 Salary Structure  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 3.1 Salary Structure from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 3.2 Payroll Processing  *(Transaction – T2)*
- **Template:** T2 – Transaction Entry Template  
- **Reference:** 02HRM_Template_Mapping.md → T2  
- **Task Details:** 03HRM_Template_Task_details.md → T2  

**Execution command:**  

```
Run 3.2 Payroll Processing from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 3.3 Payslip Generation  *(Transaction – T2)*
- **Template:** T2 – Transaction Entry Template  
- **Reference:** 02HRM_Template_Mapping.md → T2  
- **Task Details:** 03HRM_Template_Task_details.md → T2  

**Execution command:**  

```
Run 3.3 Payslip Generation from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 3.4 Tax Deductions  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 3.4 Tax Deductions from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 3.5 Benefits Administration  *(Transaction – T2)*
- **Template:** T2 – Transaction Entry Template  
- **Reference:** 02HRM_Template_Mapping.md → T2  
- **Task Details:** 03HRM_Template_Task_details.md → T2  

**Execution command:**  

```
Run 3.5 Benefits Administration from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 3.6 Compensation Planning  *(Planning/Forecasting – T8)*
- **Template:** T8 – Planning & Scenario Template  
- **Reference:** 02HRM_Template_Mapping.md → T8  
- **Task Details:** 03HRM_Template_Task_details.md → T8  

**Execution command:**  

```
Run 3.6 Compensation Planning from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 4. Time & Attendance

### 4.1 Attendance Tracking  *(Transaction – T2)*
- **Template:** T2 – Transaction Entry Template  
- **Reference:** 02HRM_Template_Mapping.md → T2  
- **Task Details:** 03HRM_Template_Task_details.md → T2  

**Execution command:**  

```
Run 4.1 Attendance Tracking from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 4.2 Shift Management  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 4.2 Shift Management from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 4.3 Leave Management  *(Workflow – T3)*
- **Template:** T3 – Workflow Orchestration Template  
- **Reference:** 02HRM_Template_Mapping.md → T3  
- **Task Details:** 03HRM_Template_Task_details.md → T3  

**Execution command:**  

```
Run 4.3 Leave Management from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 4.4 Overtime Management  *(Transaction – T2)*
- **Template:** T2 – Transaction Entry Template  
- **Reference:** 02HRM_Template_Mapping.md → T2  
- **Task Details:** 03HRM_Template_Task_details.md → T2  

**Execution command:**  

```
Run 4.4 Overtime Management from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 4.5 Time Off Requests  *(Self‑Service – T4)*
- **Template:** T4 – Employee Self‑Service Template  
- **Reference:** 02HRM_Template_Mapping.md → T4  
- **Task Details:** 03HRM_Template_Task_details.md → T4  

**Execution command:**  

```
Run 4.5 Time Off Requests from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 5. Performance Management

### 5.1 Goal Setting  *(Workflow – T3)*
- **Template:** T3 – Workflow Orchestration Template  
- **Reference:** 02HRM_Template_Mapping.md → T3  
- **Task Details:** 03HRM_Template_Task_details.md → T3  

**Execution command:**  

```
Run 5.1 Goal Setting from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 5.2 Performance Reviews  *(Workflow – T3)*
- **Template:** T3 – Workflow Orchestration Template  
- **Reference:** 02HRM_Template_Mapping.md → T3  
- **Task Details:** 03HRM_Template_Task_details.md → T3  

**Execution command:**  

```
Run 5.2 Performance Reviews from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 5.3 360‑Degree Feedback  *(Workflow – T3)*
- **Template:** T3 – Workflow Orchestration Template  
- **Reference:** 02HRM_Template_Mapping.md → T3  
- **Task Details:** 03HRM_Template_Task_details.md → T3  

**Execution command:**  

```
Run 5.3 360-Degree Feedback from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 5.4 Performance Improvement Plans  *(Workflow – T3)*
- **Template:** T3 – Workflow Orchestration Template  
- **Reference:** 02HRM_Template_Mapping.md → T3  
- **Task Details:** 03HRM_Template_Task_details.md → T3  

**Execution command:**  

```
Run 5.4 Performance Improvement Plans from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 5.5 Competency Management  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 5.5 Competency Management from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 5.6 Performance Analytics  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 5.6 Performance Analytics from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 6. Learning & Development

### 6.1 Training Programs  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 6.1 Training Programs from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 6.2 Course Management  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 6.2 Course Management from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 6.3 Skill Assessment  *(Transaction – T2)*
- **Template:** T2 – Transaction Entry Template  
- **Reference:** 02HRM_Template_Mapping.md → T2  
- **Task Details:** 03HRM_Template_Task_details.md → T2  

**Execution command:**  

```
Run 6.3 Skill Assessment from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 6.4 Certification Tracking  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 6.4 Certification Tracking from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 6.5 Learning Paths  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 6.5 Learning Paths from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 6.6 Training Reports  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 6.6 Training Reports from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 7. Employee Engagement & Recognition

### 7.1 Employee Surveys  *(Workflow – T3)*
- **Template:** T3 – Workflow Orchestration Template  
- **Reference:** 02HRM_Template_Mapping.md → T3  
- **Task Details:** 03HRM_Template_Task_details.md → T3  

**Execution command:**  

```
Run 7.1 Employee Surveys from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 7.2 Recognition Programs  *(Transaction – T2)*
- **Template:** T2 – Transaction Entry Template  
- **Reference:** 02HRM_Template_Mapping.md → T2  
- **Task Details:** 03HRM_Template_Task_details.md → T2  

**Execution command:**  

```
Run 7.2 Recognition Programs from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 7.3 Rewards & Incentives  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 7.3 Rewards & Incentives from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 7.4 Employee Feedback  *(Self‑Service – T4)*
- **Template:** T4 – Employee Self‑Service Template  
- **Reference:** 02HRM_Template_Mapping.md → T4  
- **Task Details:** 03HRM_Template_Task_details.md → T4  

**Execution command:**  

```
Run 7.4 Employee Feedback from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 7.5 Engagement Analytics  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 7.5 Engagement Analytics from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 7.6 Culture Initiatives  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 7.6 Culture Initiatives from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 8. Workforce Planning & Analytics

### 8.1 Workforce Planning  *(Planning/Forecasting – T8)*
- **Template:** T8 – Planning & Scenario Template  
- **Reference:** 02HRM_Template_Mapping.md → T8  
- **Task Details:** 03HRM_Template_Task_details.md → T8  

**Execution command:**  

```
Run 8.1 Workforce Planning from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 8.2 Headcount Analytics  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 8.2 Headcount Analytics from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 8.3 Succession Planning  *(Planning/Forecasting – T8)*
- **Template:** T8 – Planning & Scenario Template  
- **Reference:** 02HRM_Template_Mapping.md → T8  
- **Task Details:** 03HRM_Template_Task_details.md → T8  

**Execution command:**  

```
Run 8.3 Succession Planning from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 8.4 Talent Analytics  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 8.4 Talent Analytics from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 8.5 Diversity & Inclusion  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 8.5 Diversity & Inclusion from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 8.6 HR Metrics Dashboard  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 8.6 HR Metrics Dashboard from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 9. Compliance & Policies

### 9.1 Policy Management  *(Configuration/Settings – T5)*
- **Template:** T5 – Policy & Configuration Template  
- **Reference:** 02HRM_Template_Mapping.md → T5  
- **Task Details:** 03HRM_Template_Task_details.md → T5  

**Execution command:**  

```
Run 9.1 Policy Management from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 9.2 Compliance Tracking  *(Security/Governance – T9)*
- **Template:** T9 – Security & Audit Template  
- **Reference:** 02HRM_Template_Mapping.md → T9  
- **Task Details:** 03HRM_Template_Task_details.md → T9  

**Execution command:**  

```
Run 9.2 Compliance Tracking from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 9.3 Labor Law Compliance  *(Security/Governance – T9)*
- **Template:** T9 – Security & Audit Template  
- **Reference:** 02HRM_Template_Mapping.md → T9  
- **Task Details:** 03HRM_Template_Task_details.md → T9  

**Execution command:**  

```
Run 9.3 Labor Law Compliance from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 9.4 Audit Management  *(Security/Governance – T9)*
- **Template:** T9 – Security & Audit Template  
- **Reference:** 02HRM_Template_Mapping.md → T9  
- **Task Details:** 03HRM_Template_Task_details.md → T9  

**Execution command:**  

```
Run 9.4 Audit Management from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 9.5 Document Repository  *(Document/Repository – T7)*
- **Template:** T7 – Document Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T7  
- **Task Details:** 03HRM_Template_Task_details.md → T7  

**Execution command:**  

```
Run 9.5 Document Repository from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 9.6 Compliance Reports  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 9.6 Compliance Reports from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 10. Offboarding & Exit Management

### 10.1 Exit Interviews  *(Workflow – T3)*
- **Template:** T3 – Workflow Orchestration Template  
- **Reference:** 02HRM_Template_Mapping.md → T3  
- **Task Details:** 03HRM_Template_Task_details.md → T3  

**Execution command:**  

```
Run 10.1 Exit Interviews from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 10.2 Clearance Process  *(Workflow – T3)*
- **Template:** T3 – Workflow Orchestration Template  
- **Reference:** 02HRM_Template_Mapping.md → T3  
- **Task Details:** 03HRM_Template_Task_details.md → T3  

**Execution command:**  

```
Run 10.2 Clearance Process from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 10.3 Final Settlement  *(Transaction – T2)*
- **Template:** T2 – Transaction Entry Template  
- **Reference:** 02HRM_Template_Mapping.md → T2  
- **Task Details:** 03HRM_Template_Task_details.md → T2  

**Execution command:**  

```
Run 10.3 Final Settlement from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 10.4 Alumni Network  *(Master Management – T1)*
- **Template:** T1 – Master Management Template  
- **Reference:** 02HRM_Template_Mapping.md → T1  
- **Task Details:** 03HRM_Template_Task_details.md → T1  

**Execution command:**  

```
Run 10.4 Alumni Network from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 10.5 Exit Analytics  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 10.5 Exit Analytics from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 11. HR Reports & Analytics

### 11.1 Headcount Reports  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 11.1 Headcount Reports from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 11.2 Turnover Analysis  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 11.2 Turnover Analysis from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 11.3 Recruitment Analytics  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 11.3 Recruitment Analytics from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 11.4 Payroll Reports  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 11.4 Payroll Reports from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 11.5 Attendance Reports  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 11.5 Attendance Reports from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 11.6 Custom HR Reports  *(Analytics/Dashboard – T6)*
- **Template:** T6 – Analytics & Dashboard Template  
- **Reference:** 02HRM_Template_Mapping.md → T6  
- **Task Details:** 03HRM_Template_Task_details.md → T6  

**Execution command:**  

```
Run 11.6 Custom HR Reports from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 12. Access & Security

### 12.1 Role‑based Access  *(Security/Governance – T9)*
- **Template:** T9 – Security & Audit Template  
- **Reference:** 02HRM_Template_Mapping.md → T9  
- **Task Details:** 03HRM_Template_Task_details.md → T9  

**Execution command:**  

```
Run 12.1 Role-based Access from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 12.2 Data Privacy  *(Security/Governance – T9)*
- **Template:** T9 – Security & Audit Template  
- **Reference:** 02HRM_Template_Mapping.md → T9  
- **Task Details:** 03HRM_Template_Task_details.md → T9  

**Execution command:**  

```
Run 12.2 Data Privacy from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 12.3 Audit Logs  *(Security/Governance – T9)*
- **Template:** T9 – Security & Audit Template  
- **Reference:** 02HRM_Template_Mapping.md → T9  
- **Task Details:** 03HRM_Template_Task_details.md → T9  

**Execution command:**  

```
Run 12.3 Audit Logs from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 12.4 Security Settings  *(Configuration/Settings – T5)*
- **Template:** T5 – Policy & Configuration Template  
- **Reference:** 02HRM_Template_Mapping.md → T5  
- **Task Details:** 03HRM_Template_Task_details.md → T5  

**Execution command:**  

```
Run 12.4 Security Settings from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 13. Integrations & Configuration

### 13.1 Payroll Integration  *(Integration – T10)*
- **Template:** T10 – Integration Configuration Template  
- **Reference:** 02HRM_Template_Mapping.md → T10  
- **Task Details:** 03HRM_Template_Task_details.md → T10  

**Execution command:**  

```
Run 13.1 Payroll Integration from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 13.2 Background Check Integration  *(Integration – T10)*
- **Template:** T10 – Integration Configuration Template  
- **Reference:** 02HRM_Template_Mapping.md → T10  
- **Task Details:** 03HRM_Template_Task_details.md → T10  

**Execution command:**  

```
Run 13.2 Background Check Integration from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 13.3 Benefits Provider Integration  *(Integration – T10)*
- **Template:** T10 – Integration Configuration Template  
- **Reference:** 02HRM_Template_Mapping.md → T10  
- **Task Details:** 03HRM_Template_Task_details.md → T10  

**Execution command:**  

```
Run 13.3 Benefits Provider Integration from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 13.4 Learning Management System  *(Integration – T10)*
- **Template:** T10 – Integration Configuration Template  
- **Reference:** 02HRM_Template_Mapping.md → T10  
- **Task Details:** 03HRM_Template_Task_details.md → T10  

**Execution command:**  

```
Run 13.4 Learning Management System from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

### 13.5 HR System Settings  *(Configuration/Settings – T5)*
- **Template:** T5 – Policy & Configuration Template  
- **Reference:** 02HRM_Template_Mapping.md → T5  
- **Task Details:** 03HRM_Template_Task_details.md → T5  

**Execution command:**  

```
Run 13.5 HR System Settings from Learning01\01\15.Tasks&Templates\01HRM_TaskList.md
```

---

## 📋 Tracking & Updates
- Each screen's entry should be kept in the same format: **ID Title**, **Template**, **Reference files**, **Execution command**.
- When a template evolves, update **03HRM_Template_Task_details.md**; the task list will automatically point to the latest version.
- Agents can query this file to discover the exact command they need to run any screen.

---

*File updated to serve as the central hub linking to the template mapping and detailed task specifications, ready for downstream agents to consume.*
