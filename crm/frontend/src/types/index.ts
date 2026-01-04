// CRM Frontend TypeScript Types

export interface Customer {
  id: string;
  name: string;
  email: string;
  phone?: string;
  company?: string;
  industry?: string;
  address?: string;
  city?: string;
  country?: string;
  status: 'active' | 'inactive' | 'prospect';
  createdAt: string;
  updatedAt: string;
}

export interface Lead {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  company?: string;
  source: 'website' | 'referral' | 'cold_call' | 'email' | 'social' | 'other';
  status: 'new' | 'contacted' | 'qualified' | 'converted' | 'lost';
  score: number;
  assignedTo?: string;
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Contact {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  title?: string;
  department?: string;
  customerId: string;
  isPrimary: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Account {
  id: string;
  name: string;
  industry?: string;
  size?: string;
  website?: string;
  phone?: string;
  address?: string;
  city?: string;
  country?: string;
  revenue?: number;
  description?: string;
  status: 'active' | 'inactive' | 'prospect';
  createdAt: string;
  updatedAt: string;
}

export interface Opportunity {
  id: string;
  name: string;
  accountId: string;
  contactId?: string;
  amount: number;
  currency: string;
  stage: 'prospecting' | 'qualification' | 'proposal' | 'negotiation' | 'closed_won' | 'closed_lost';
  probability: number;
  expectedCloseDate: string;
  actualCloseDate?: string;
  description?: string;
  assignedTo?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Campaign {
  id: string;
  name: string;
  type: 'email' | 'social' | 'webinar' | 'event' | 'content' | 'paid_ads';
  status: 'draft' | 'active' | 'paused' | 'completed' | 'cancelled';
  startDate: string;
  endDate?: string;
  budget?: number;
  description?: string;
  targetAudience?: string;
  metrics?: CampaignMetrics;
  createdAt: string;
  updatedAt: string;
}

export interface CampaignMetrics {
  sent?: number;
  delivered?: number;
  opened?: number;
  clicked?: number;
  converted?: number;
  revenue?: number;
}

export interface Activity {
  id: string;
  type: 'call' | 'email' | 'meeting' | 'task' | 'note';
  subject: string;
  description?: string;
  customerId?: string;
  leadId?: string;
  opportunityId?: string;
  assignedTo?: string;
  status: 'pending' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high';
  dueDate?: string;
  completedAt?: string;
  createdAt: string;
  updatedAt: string;
}

export interface SalesReport {
  period: string;
  totalRevenue: number;
  totalDeals: number;
  averageDealSize: number;
  conversionRate: number;
  pipelineValue: number;
  wonDeals: number;
  lostDeals: number;
}
