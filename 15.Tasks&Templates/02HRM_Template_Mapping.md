# HRM SCREEN CLASSIFICATION & TEMPLATE MAPPING

## SECTION A — SCREEN CLASSIFICATION TABLE

| Module | Menu Item | Screen Nature | Template Type | Reasoning |
|--------|----------|--------------|--------------|----------|
| HR Dashboard | HR Dashboard | ANALYTICS / DASHBOARD | T6 | Central KPI and metrics visualization hub |
| Employee Management | Employee Directory | MASTER | T1 | Static employee reference data with search/filter capabilities |
| Employee Management | Organizational Chart | MASTER | T1 | Hierarchical structure visualization of reporting relationships |
| Employee Management | Employee Self-Service | SELF-SERVICE | T4 | Employee-initiated personal data management |
| Employee Management | Document Management | DOCUMENT / REPOSITORY | T7 | File-centric document storage with version control |
| Employee Management | Employee Lifecycle | MASTER | T1 | Historical tracking of employee status changes |
| Talent Acquisition | Job Requisitions | WORKFLOW | T3 | Multi-step approval process for job creation |
| Talent Acquisition | Candidate Management | TRANSACTION | T2 | Operational candidate data entry and tracking |
| Talent Acquisition | Interview Scheduling | WORKFLOW | T3 | Multi-step interview coordination process |
| Talent Acquisition | Offer Management | WORKFLOW | T3 | Multi-step offer approval and negotiation process |
| Talent Acquisition | Onboarding | WORKFLOW | T3 | Multi-step onboarding task coordination |
| Compensation & Payroll | Salary Structure | MASTER | T1 | Compensation grade and band reference data |
| Compensation & Payroll | Payroll Processing | TRANSACTION | T2 | High-volume payroll calculation and processing |
| Compensation & Payroll | Payslip Generation | TRANSACTION | T2 | Automated payslip creation and distribution |
| Compensation & Payroll | Tax Deductions | MASTER | T1 | Tax rule and deduction reference data |
| Compensation & Payroll | Benefits Administration | TRANSACTION | T2 | Benefits enrollment and management operations |
| Compensation & Payroll | Compensation Planning | PLANNING / FORECASTING | T8 | Future compensation modeling and budgeting |
| Time & Attendance | Attendance Tracking | TRANSACTION | T2 | Daily attendance data entry and validation |
| Time & Attendance | Shift Management | MASTER | T1 | Shift schedule and rule configuration |
| Time & Attendance | Leave Management | WORKFLOW | T3 | Multi-step leave request approval process |
| Time & Attendance | Overtime Management | TRANSACTION | T2 | Overtime calculation and approval workflow |
| Time & Attendance | Time Off Requests | SELF-SERVICE | T4 | Employee-initiated time off requests |
| Performance Management | Goal Setting | WORKFLOW | T3 | Multi-step goal creation and approval process |
| Performance Management | Performance Reviews | WORKFLOW | T3 | Multi-step review cycle management |
| Performance Management | 360-Degree Feedback | WORKFLOW | T3 | Multi-rater feedback collection process |
| Performance Management | Performance Improvement Plans | WORKFLOW | T3 | Structured PIP workflow with milestones |
| Performance Management | Competency Management | MASTER | T1 | Competency framework and skill definitions |
| Performance Management | Performance Analytics | ANALYTICS / DASHBOARD | T6 | Performance metrics and trend analysis |
| Learning & Development | Training Programs | MASTER | T1 | Training course and program catalog |
| Learning & Development | Course Management | MASTER | T1 | Course content and material management |
| Learning & Development | Skill Assessment | TRANSACTION | T2 | Skill evaluation and assessment data entry |
| Learning & Development | Certification Tracking | MASTER | T1 | Certification records and expiration tracking |
| Learning & Development | Learning Paths | MASTER | T1 | Structured learning path definitions |
| Learning & Development | Training Reports | ANALYTICS / DASHBOARD | T6 | Training effectiveness and completion metrics |
| Employee Engagement | Employee Surveys | WORKFLOW | T3 | Survey creation, distribution, and analysis |
| Employee Engagement | Recognition Programs | TRANSACTION | T2 | Recognition award and point management |
| Employee Engagement | Rewards & Incentives | MASTER | T1 | Reward program configuration and rules |
| Employee Engagement | Employee Feedback | SELF-SERVICE | T4 | Employee-initiated feedback submission |
| Employee Engagement | Engagement Analytics | ANALYTICS / DASHBOARD | T6 | Engagement metrics and trend analysis |
| Employee Engagement | Culture Initiatives | MASTER | T1 | Culture program definitions and tracking |
| Workforce Planning | Workforce Planning | PLANNING / FORECASTING | T8 | Strategic workforce demand forecasting |
| Workforce Planning | Headcount Analytics | ANALYTICS / DASHBOARD | T6 | Headcount metrics and trend analysis |
| Workforce Planning | Succession Planning | PLANNING / FORECASTING | T8 | Succession pipeline and risk analysis |
| Workforce Planning | Talent Analytics | ANALYTICS / DASHBOARD | T6 | Talent distribution and mobility analysis |
| Workforce Planning | Diversity & Inclusion | ANALYTICS / DASHBOARD | T6 | Diversity metrics and compliance reporting |
| Workforce Planning | HR Metrics Dashboard | ANALYTICS / DASHBOARD | T6 | Executive HR metrics visualization |
| Compliance & Policies | Policy Management | CONFIGURATION / SETTINGS | T5 | Policy creation, versioning, and distribution |
| Compliance & Policies | Compliance Tracking | SECURITY / GOVERNANCE | T9 | Compliance monitoring and violation tracking |
| Compliance & Policies | Labor Law Compliance | SECURITY / GOVERNANCE | T9 | Legal requirement tracking and compliance |
| Compliance & Policies | Audit Management | SECURITY / GOVERNANCE | T9 | Audit scheduling and evidence collection |
| Compliance & Policies | Document Repository | DOCUMENT / REPOSITORY | T7 | Compliance document storage and access |
| Compliance & Policies | Compliance Reports | ANALYTICS / DASHBOARD | T6 | Compliance status and violation reporting |
| Offboarding | Exit Interviews | WORKFLOW | T3 | Structured exit interview process |
| Offboarding | Clearance Process | WORKFLOW | T3 | Multi-step clearance and asset recovery |
| Offboarding | Final Settlement | TRANSACTION | T2 | Final pay calculation and processing |
| Offboarding | Alumni Network | MASTER | T1 | Former employee database and networking |
| Offboarding | Exit Analytics | ANALYTICS / DASHBOARD | T6 | Turnover analysis and exit trends |
| HR Reports | Headcount Reports | ANALYTICS / DASHBOARD | T6 | Headcount metrics and reporting |
| HR Reports | Turnover Analysis | ANALYTICS / DASHBOARD | T6 | Turnover rate and reason analysis |
| HR Reports | Recruitment Analytics | ANALYTICS / DASHBOARD | T6 | Recruitment metrics and pipeline analysis |
| HR Reports | Payroll Reports | ANALYTICS / DASHBOARD | T6 | Payroll cost and variance reporting |
| HR Reports | Attendance Reports | ANALYTICS / DASHBOARD | T6 | Attendance patterns and compliance reporting |
| HR Reports | Custom HR Reports | ANALYTICS / DASHBOARD | T6 | Ad-hoc report builder and visualization |
| Access & Security | Role-based Access | SECURITY / GOVERNANCE | T9 | User role and permission management |
| Access & Security | Data Privacy | SECURITY / GOVERNANCE | T9 | PII protection and privacy controls |
| Access & Security | Audit Logs | SECURITY / GOVERNANCE | T9 | System activity logging and monitoring |
| Access & Security | Security Settings | CONFIGURATION / SETTINGS | T5 | Security policy and system configuration |
| Integrations | Payroll Integration | INTEGRATION | T10 | Third-party payroll system connectivity |
| Integrations | Background Check Integration | INTEGRATION | T10 | Background check service integration |
| Integrations | Benefits Provider Integration | INTEGRATION | T10 | Benefits carrier system connectivity |
| Integrations | Learning Management System | INTEGRATION | T10 | LMS platform integration and sync |
| Integrations | HR System Settings | CONFIGURATION / SETTINGS | T5 | System configuration and policy management |

## SECTION B — TEMPLATE DEFINITIONS

### T1. Master Management Template
**Intended Use**: Static or slowly changing reference data management with search, filter, and CRUD operations

**UI Structure Spec**:
- Page layout: List-detail with advanced filtering
- Navigation pattern: Tabbed interface with master-detail drill-down
- Filters: Multi-criteria search with saved filters
- Bulk actions: Import/export, mass update, archive/restore
- Read-only zones: Historical data, system-generated fields
- Role-based UI visibility: Admin full access, Manager read-only on team data, Employee self-only

**Business Validation Rules**:
- Mandatory fields: Code, description, effective dates
- Cross-entity dependencies: Parent-child relationships, foreign key validation
- Effective date handling: Date ranges, overlap prevention
- State transitions: Draft → Active → Inactive → Archived
- Role-based action permissions: Create/Update limited to admin roles
- Audit & traceability: Full change history with user attribution

**Data Behavior Rules**:
- Create / Update / Archive / Soft-delete: Full lifecycle management
- Versioning requirements: Major version for structural changes
- Historical snapshot requirements: Effective date-based versioning
- Legal or compliance retention flags: Configurable retention periods

**Non-Functional Expectations**:
- Performance sensitivity: Medium (moderate data volumes)
- Security sensitivity: Low (reference data, limited PII)
- Audit depth: Full (complete change tracking required)

### T2. Transaction Entry Template
**Intended Use**: High-volume operational data entry with business impact and validation

**UI Structure Spec**:
- Page layout: Form-centric with supporting data panels
- Navigation pattern: Wizard for complex transactions, single-page for simple
- Filters: Date ranges, status filters, entity-specific filters
- Bulk actions: Batch processing, mass approval, bulk import
- Read-only zones: Approved transactions, calculated fields
- Role-based UI visibility: Edit rights based on transaction state and role

**Business Validation Rules**:
- Mandatory fields: Business-critical fields with real-time validation
- Cross-entity dependencies: Account validation, policy compliance checks
- Effective date handling: Transaction dates, posting periods
- State transitions: Draft → Submitted → Approved → Posted → Reversed
- Role-based action permissions: Submit/approve based on authorization matrix
- Audit & traceability: Transaction logging with approval chain

**Data Behavior Rules**:
- Create / Update / Archive / Soft-delete: Immutable posted transactions
- Versioning requirements: None (transaction immutability)
- Historical snapshot requirements: Transaction log with reversal capability
- Legal or compliance retention flags: Extended retention for financial data

**Non-Functional Expectations**:
- Performance sensitivity: High (large transaction volumes)
- Security sensitivity: High (financial and sensitive data)
- Audit depth: Full (complete transaction audit trail)

### T3. Workflow Orchestration Template
**Intended Use**: Multi-step, approval-based processes with state management and routing

**UI Structure Spec**:
- Page layout: Workflow canvas with step visualization
- Navigation pattern: Linear progression with branching support
- Filters: Workflow status, initiator, date ranges
- Bulk actions: Mass approval, bulk rejection, workflow reassignment
- Read-only zones: Completed steps, system decisions
- Role-based UI visibility: Current step actions based on workflow role

**Business Validation Rules**:
- Mandatory fields: Step-specific required fields
- Cross-entity dependencies: Inter-step data validation
- Effective date handling: Workflow initiation and completion dates
- State transitions: Custom workflow states with business rules
- Role-based action permissions: Step-based approval authorities
- Audit & traceability: Complete workflow history with decision rationale

**Data Behavior Rules**:
- Create / Update / Archive / Soft-delete: Workflow instance management
- Versioning requirements: Workflow definition versioning
- Historical snapshot requirements: Workflow state changes and decisions
- Legal or compliance retention flags: Extended retention for audit trails

**Non-Functional Expectations**:
- Performance sensitivity: Medium (workflow processing overhead)
- Security sensitivity: High (approval and decision data)
- Audit depth: Full (complete workflow audit trail)

### T4. Employee Self-Service Template
**Intended Use**: Employee-initiated transactions with role restrictions and data scope limitations

**UI Structure Spec**:
- Page layout: Simplified forms with contextual help
- Navigation pattern: Task-oriented with guided workflows
- Filters: Personal data filters, status tracking
- Bulk actions: Limited to personal data operations
- Read-only zones: Company policies, system-calculated fields
- Role-based UI visibility: Employee data only, no cross-employee access

**Business Validation Rules**:
- Mandatory fields: Employee-specific required information
- Cross-entity dependencies: Personal data validation against master data
- Effective date handling: Request effective dates and policy compliance
- State transitions: Request → Submitted → Approved → Processed
- Role-based action permissions: Self-only actions, no administrative overrides
- Audit & traceability: Employee action logging with data changes

**Data Behavior Rules**:
- Create / Update / Archive / Soft-delete: Personal data management only
- Versioning requirements: None (personal data immutability)
- Historical snapshot requirements: Request history and status changes
- Legal or compliance retention flags: Standard employee data retention

**Non-Functional Expectations**:
- Performance sensitivity: Low (individual transaction volumes)
- Security sensitivity: High (personal and sensitive data)
- Audit depth: Basic (employee action logging)

### T5. Policy & Configuration Template
**Intended Use**: System behavior control, rules, policies, and administrative settings

**UI Structure Spec**:
- Page layout: Configuration forms with policy editors
- Navigation pattern: Categorized settings with search and hierarchy
- Filters: Configuration categories, effective dates, status
- Bulk actions: Policy import/export, mass activation/deactivation
- Read-only zones: System-critical settings, compliance fields
- Role-based UI visibility: Admin-only access, read-only for auditors

**Business Validation Rules**:
- Mandatory fields: Policy-critical configuration parameters
- Cross-entity dependencies: System impact validation, dependency checking
- Effective date handling: Policy effective dates and transition periods
- State transitions: Draft → Review → Approved → Active → Deprecated
- Role-based action permissions: Administrative approval workflows
- Audit & traceability: Policy change logging with business justification

**Data Behavior Rules**:
- Create / Update / Archive / Soft-delete: Configuration lifecycle management
- Versioning requirements: Policy versioning with rollback capability
- Historical snapshot requirements: Policy history and compliance tracking
- Legal or compliance retention flags: Extended retention for policy evidence

**Non-Functional Expectations**:
- Performance sensitivity: Low (configuration changes are infrequent)
- Security sensitivity: High (system-critical settings)
- Audit depth: Full (complete configuration audit trail)

### T6. Analytics & Dashboard Template
**Intended Use**: KPI visualization, trend analysis, and executive reporting

**UI Structure Spec**:
- Page layout: Dashboard with widget-based layout
- Navigation pattern: Tabbed dashboards with drill-down capabilities
- Filters: Date ranges, dimensions, metrics, comparative periods
- Bulk actions: Export, subscription, report scheduling
- Read-only zones: All data is read-only with time-based refresh
- Role-based UI visibility: Data scope based on organizational hierarchy

**Business Validation Rules**:
- Mandatory fields: Report parameters and filter criteria
- Cross-entity dependencies: Data source validation and integrity checks
- Effective date handling: Reporting periods and data currency
- State transitions: None (read-only analytics)
- Role-based action permissions: View-only with export capabilities
- Audit & traceability: Report generation and access logging

**Data Behavior Rules**:
- Create / Update / Archive / Soft-delete: Report definitions and subscriptions
- Versioning requirements: Report template versioning
- Historical snapshot requirements: Data warehouse snapshots for trend analysis
- Legal or compliance retention flags: Standard reporting retention

**Non-Functional Expectations**:
- Performance sensitivity: High (complex queries and aggregations)
- Security sensitivity: Medium (aggregated data, limited PII)
- Audit depth: Basic (report access and generation logging)

### T7. Document Management Template
**Intended Use**: File-centric operations with version control and metadata management

**UI Structure Spec**:
- Page layout: Document library with preview and metadata panels
- Navigation pattern: Folder hierarchy with search and filters
- Filters: Document type, date, status, metadata, full-text search
- Bulk actions: Mass upload, version control, access permission changes
- Read-only zones: Archived documents, approved versions
- Role-based UI visibility: Access based on document permissions

**Business Validation Rules**:
- Mandatory fields: Document metadata, classification, retention schedule
- Cross-entity dependencies: Entity association validation
- Effective date handling: Document effective dates and expiration
- State transitions: Draft → Review → Approved → Published → Archived
- Role-based action permissions: Upload, approve, publish based on permissions
- Audit & traceability: Document lifecycle and access logging

**Data Behavior Rules**:
- Create / Update / Archive / Soft-delete: Document lifecycle with versioning
- Versioning requirements: Full document versioning with change tracking
- Historical snapshot requirements: Document version history and metadata
- Legal or compliance retention flags: Extended retention for legal documents

**Non-Functional Expectations**:
- Performance sensitivity: Medium (file storage and retrieval)
- Security sensitivity: High (confidential and legal documents)
- Audit depth: Full (complete document access and change audit)

### T8. Planning & Scenario Template
**Intended Use**: Future-oriented modeling, simulations, and strategic planning

**UI Structure Spec**:
- Page layout: Modeling interface with scenario comparison
- Navigation pattern: Wizard-based planning with assumption inputs
- Filters: Planning horizons, scenarios, business units
- Bulk actions: Scenario cloning, batch calculation, model export
- Read-only zones: Approved plans, locked assumptions
- Role-based UI visibility: Planning rights based on organizational level

**Business Validation Rules**:
- Mandatory fields: Planning assumptions, key drivers, target metrics
- Cross-entity dependencies: Master data validation, constraint checking
- Effective date handling: Planning periods and forecast horizons
- State transitions: Draft → Review → Approved → Published → Archived
- Role-based action permissions: Create/approve based on planning authority
- Audit & traceability: Planning assumptions and model changes

**Data Behavior Rules**:
- Create / Update / Archive / Soft-delete: Plan versioning with scenario management
- Versioning requirements: Plan versioning with assumption tracking
- Historical snapshot requirements: Plan history and comparison capabilities
- Legal or compliance retention flags: Extended retention for strategic plans

**Non-Functional Expectations**:
- Performance sensitivity: Medium (complex calculations and simulations)
- Security sensitivity: Medium (strategic and competitive data)
- Audit depth: Full (planning assumptions and decision audit)

### T9. Security & Audit Template
**Intended Use**: Access control, audit trails, compliance monitoring, and governance

**UI Structure Spec**:
- Page layout: Security console with audit trail viewer
- Navigation pattern: Tabbed interface with drill-down investigation
- Filters: Time ranges, users, actions, risk levels, compliance categories
- Bulk actions: Bulk permission changes, report generation, alert configuration
- Read-only zones: Historical audit logs, system-generated events
- Role-based UI visibility: Security admin full access, auditor read-only

**Business Validation Rules**:
- Mandatory fields: Security parameters, compliance requirements
- Cross-entity dependencies: Access control validation and segregation checks
- Effective date handling: Policy effective dates and compliance deadlines
- State transitions: None (security events are immutable)
- Role-based action permissions: Security admin only for changes
- Audit & traceability: Complete security event logging with tamper protection

**Data Behavior Rules**:
- Create / Update / Archive / Soft-delete: Security configuration with immutable audit
- Versioning requirements: Security policy versioning with rollback protection
- Historical snapshot requirements: Complete audit trail with long-term retention
- Legal or compliance retention flags: Extended retention for security evidence

**Non-Functional Expectations**:
- Performance sensitivity: Low (security operations are infrequent)
- Security sensitivity: Critical (system security and compliance data)
- Audit depth: Full (complete security audit with tamper protection)

### T10. Integration Configuration Template
**Intended Use**: External system connectivity, data synchronization, and API management

**UI Structure Spec**:
- Page layout: Integration console with connection status monitoring
- Navigation pattern: System-specific configuration with testing tools
- Filters: Integration status, system type, sync frequency, error status
- Bulk actions: Mass sync, connection testing, configuration export
- Read-only zones: Active connections, system-generated sync data
- Role-based UI visibility: Integration admin full access, monitoring read-only

**Business Validation Rules**:
- Mandatory fields: Connection parameters, authentication credentials, sync rules
- Cross-entity dependencies: Data mapping validation and integrity checks
- Effective date handling: Integration activation and deactivation scheduling
- State transitions: Configured → Testing → Active → Inactive → Error
- Role-based action permissions: Integration admin only for configuration
- Audit & traceability: Integration events and data sync logging

**Data Behavior Rules**:
- Create / Update / Archive / Soft-delete: Integration configuration with sync history
- Versioning requirements: Integration definition versioning
- Historical snapshot requirements: Sync history and error tracking
- Legal or compliance retention: Standard integration logging retention

**Non-Functional Expectations**:
- Performance sensitivity: High (real-time data synchronization)
- Security sensitivity: High (external system credentials and data)
- Audit depth: Full (complete integration audit trail)

## SECTION C — REUSE & GOVERNANCE NOTES

**Highly Reused Templates:**
- T6 (Analytics & Dashboard) - Used across 15+ screens for reporting and metrics
- T1 (Master Management) - Used for 12+ reference data management screens
- T3 (Workflow Orchestration) - Used for 8+ multi-step approval processes
- T9 (Security & Audit) - Used for 6+ security and compliance screens

**Template Exceptions:**
- T4 (Employee Self-Service) - Highly specialized for employee-only interactions
- T10 (Integration Configuration) - Specialized for external system connectivity
- T8 (Planning & Scenario) - Specialized for forward-looking strategic functions

**Future-Proofing Observations:**
- Template-based approach ensures consistent user experience across similar screen types
- Clear separation between reference data (T1) and transactional data (T2) maintains data integrity
- Workflow templates (T3) provide consistent approval experiences across different business processes
- Analytics templates (T6) enable standardized reporting and KPI visualization
- Security templates (T9) ensure consistent governance and compliance management
- Self-service templates (T4) empower employees while maintaining data boundaries
- Integration templates (T10) provide standardized external system connectivity patterns

**Governance Benefits:**
- Reduced development time through template reuse
- Consistent user experience across similar functional areas
- Standardized validation and audit patterns
- Simplified maintenance and updates
- Clear separation of concerns between different screen natures
- Role-based access control consistently applied across templates
- Standardized non-functional requirements for similar screen types
