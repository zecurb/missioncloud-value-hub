export type Money = {
  amount: string;
  currency: string;
};

export type ValueSummary = {
  period_start: string;
  period_end: string;
  total_cloud_spend: Money;
  budget_variance_percent: string;
  identified_annual_savings: Money;
  realized_monthly_savings: Money;
  optimization_coverage_percent: string;
  allocation_coverage_percent: string;
  policy_compliance_percent: string;
  open_opportunities: number;
};

export type OptimizationOpportunity = {
  id: string;
  title: string;
  category: string;
  owner_team: string;
  service: string;
  account_name: string;
  estimated_monthly_savings: Money;
  confidence_percent: number;
  effort: string;
  risk: string;
  status: string;
  rationale: string;
};
