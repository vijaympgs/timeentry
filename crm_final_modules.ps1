# PowerShell script to create remaining CRM modules 13-18
# This handles spaces in directory names better than batch files

Write-Host "Creating final CRM modules 13-18 using PowerShell..."

# Create Partner & Channel Management files
Write-Host "Creating Partner & Channel Management files..."

$module13Path = "CRM\13.Partner & Channel Management"
if (!(Test-Path $module13Path)) {
    New-Item -ItemType Directory -Path $module13Path -Force
}

# 13.1 Partner Portal
@"
# Partner Portal

## Overview
Partner relationship management portal

## Features
- Partner dashboard
- Resource access
- Collaboration tools
"@ | Out-File -FilePath "$module13Path\13.1 Partner Portal.md" -Encoding UTF8

# 13.2 Partner Onboarding
@"
# Partner Onboarding

## Overview
Streamline partner onboarding process

## Features
- Onboarding workflows
- Document management
- Training tracking
"@ | Out-File -FilePath "$module13Path\13.2 Partner Onboarding.md" -Encoding UTF8

# 13.3 Partner Performance
@"
# Partner Performance

## Overview
Track and analyze partner performance

## Features
- Performance metrics
- Goal tracking
- Benchmarking
"@ | Out-File -FilePath "$module13Path\13.3 Partner Performance.md" -Encoding UTF8

# 13.4 Deal Registration
@"
# Deal Registration

## Overview
Partner deal registration system

## Features
- Deal validation
- Conflict checking
- Commission tracking
"@ | Out-File -FilePath "$module13Path\13.4 Deal Registration.md" -Encoding UTF8

# 13.5 Partner Incentives
@"
# Partner Incentives

## Overview
Manage partner incentive programs

## Features
- Incentive plans
- Commission calculation
- Reward management
"@ | Out-File -FilePath "$module13Path\13.5 Partner Incentives.md" -Encoding UTF8

# 13.6 Co-marketing Programs
@"
# Co-marketing Programs

## Overview
Collaborative marketing initiatives

## Features
- Campaign collaboration
- Fund management
- ROI tracking
"@ | Out-File -FilePath "$module13Path\13.6 Co-marketing Programs.md" -Encoding UTF8

# 13.7 Partner Training
@"
# Partner Training

## Overview
Partner training and certification

## Features
- Course management
- Certification tracking
- Progress monitoring
"@ | Out-File -FilePath "$module13Path\13.7 Partner Training.md" -Encoding UTF8

# 13.8 Partner Resources
@"
# Partner Resources

## Overview
Partner resource management

## Features
- Resource library
- Asset management
- Access control
"@ | Out-File -FilePath "$module13Path\13.8 Partner Resources.md" -Encoding UTF8

# 13.9 Partner Analytics
@"
# Partner Analytics

## Overview
Partner performance analytics

## Features
- Performance dashboards
- Trend analysis
- Predictive insights
"@ | Out-File -FilePath "$module13Path\13.9 Partner Analytics.md" -Encoding UTF8

# 13.10 Channel Conflict Resolution
@"
# Channel Conflict Resolution

## Overview
Manage and resolve channel conflicts

## Features
- Conflict detection
- Resolution workflows
- Policy enforcement
"@ | Out-File -FilePath "$module13Path\13.10 Channel Conflict Resolution.md" -Encoding UTF8

# Create Sales Enablement files
Write-Host "Creating Sales Enablement files..."

$module14Path = "CRM\14.Sales Enablement"
if (!(Test-Path $module14Path)) {
    New-Item -ItemType Directory -Path $module14Path -Force
}

# 14.1 Sales Content Library
@"
# Sales Content Library

## Overview
Central repository for sales content

## Features
- Content organization
- Version control
- Access management
"@ | Out-File -FilePath "$module14Path\14.1 Sales Content Library.md" -Encoding UTF8

# 14.2 Sales Playbooks
@"
# Sales Playbooks

## Overview
Guided selling methodologies

## Features
- Playbook templates
- Step-by-step guidance
- Best practices
"@ | Out-File -FilePath "$module14Path\14.2 Sales Playbooks.md" -Encoding UTF8

# 14.3 Competitive Intelligence
@"
# Competitive Intelligence

## Overview
Track and analyze competition

## Features
- Competitor profiles
- Market analysis
- Battle cards
"@ | Out-File -FilePath "$module14Path\14.3 Competitive Intelligence.md" -Encoding UTF8

# 14.4 Product Training
@"
# Product Training

## Overview
Sales team product knowledge

## Features
- Training modules
- Certification tracking
- Knowledge assessments
"@ | Out-File -FilePath "$module14Path\14.4 Product Training.md" -Encoding UTF8

# 14.5 Sales Scripts
@"
# Sales Scripts

## Overview
Pre-defined sales conversation guides

## Features
- Script templates
- Customization options
- Performance tracking
"@ | Out-File -FilePath "$module14Path\14.5 Sales Scripts.md" -Encoding UTF8

# 14.6 Objection Handling
@"
# Objection Handling

## Overview
Manage customer objections effectively

## Features
- Objection database
- Response templates
- Training scenarios
"@ | Out-File -FilePath "$module14Path\14.6 Objection Handling.md" -Encoding UTF8

# 14.7 Best Practices
@"
# Best Practices

## Overview
Sales methodology best practices

## Features
- Practice library
- Implementation guides
- Success stories
"@ | Out-File -FilePath "$module14Path\14.7 Best Practices.md" -Encoding UTF8

# 14.8 Sales Tools
@"
# Sales Tools

## Overview
Productivity tools for sales team

## Features
- Tool integration
- Workflow automation
- Performance analytics
"@ | Out-File -FilePath "$module14Path\14.8 Sales Tools.md" -Encoding UTF8

# 14.9 Mobile Sales App
@"
# Mobile Sales App

## Overview
Mobile access for sales team

## Features
- Mobile CRM access
- Offline capabilities
- Real-time sync
"@ | Out-File -FilePath "$module14Path\14.9 Mobile Sales App.md" -Encoding UTF8

# 14.10 Offline Access
@"
# Offline Access

## Overview
Work without internet connectivity

## Features
- Offline data sync
- Local storage
- Conflict resolution
"@ | Out-File -FilePath "$module14Path\14.10 Offline Access.md" -Encoding UTF8

# Create Analytics & Reporting files
Write-Host "Creating Analytics & Reporting files..."

$module15Path = "CRM\15.Analytics & Reporting"
if (!(Test-Path $module15Path)) {
    New-Item -ItemType Directory -Path $module15Path -Force
}

# 15.1 Sales Performance Reports
@"
# Sales Performance Reports

## Overview
Track sales team performance

## Features
- Performance metrics
- Goal tracking
- Leaderboards
"@ | Out-File -FilePath "$module15Path\15.1 Sales Performance Reports.md" -Encoding UTF8

# 15.2 Win_Loss Analysis
@"
# Win_Loss Analysis

## Overview
Analyze won and lost opportunities

## Features
- Loss reason tracking
- Success patterns
- Competitive insights
"@ | Out-File -FilePath "$module15Path\15.2 Win_Loss Analysis.md" -Encoding UTF8

# 15.3 Sales Cycle Analysis
@"
# Sales Cycle Analysis

## Overview
Analyze sales cycle duration

## Features
- Cycle metrics
- Bottleneck identification
- Process optimization
"@ | Out-File -FilePath "$module15Path\15.3 Sales Cycle Analysis.md" -Encoding UTF8

# 15.4 Revenue Reports
@"
# Revenue Reports

## Overview
Revenue tracking and forecasting

## Features
- Revenue metrics
- Trend analysis
- Forecast accuracy
"@ | Out-File -FilePath "$module15Path\15.4 Revenue Reports.md" -Encoding UTF8

Write-Host "CRM modules 13-15 created successfully!"
