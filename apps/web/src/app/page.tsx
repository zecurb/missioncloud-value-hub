import { KpiCard } from "@/components/KpiCard";
import { OpportunityTable } from "@/components/OpportunityTable";
import { getOptimizationOpportunities, getValueSummary } from "@/lib/api";

const money = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

export default async function DashboardPage() {
  const [summary, opportunities] = await Promise.all([
    getValueSummary(),
    getOptimizationOpportunities(),
  ]);

  return (
    <main>
      <header className="hero">
        <div>
          <p className="eyebrow">FinOps command center</p>
          <h1>MissionCloud Value Hub</h1>
          <p className="hero-copy">
            Connect cloud economics, governance, and engineering action to measurable business value.
          </p>
        </div>
        <div className="period">
          Reporting period
          <strong>{summary.period_start} — {summary.period_end}</strong>
        </div>
      </header>

      <section className="kpi-grid" aria-label="Executive KPIs">
        <KpiCard
          label="Cloud spend"
          value={money.format(Number(summary.total_cloud_spend.amount))}
          detail={`${summary.budget_variance_percent}% above budget`}
        />
        <KpiCard
          label="Annual value identified"
          value={money.format(Number(summary.identified_annual_savings.amount))}
          detail={`${summary.open_opportunities} open opportunities`}
        />
        <KpiCard
          label="Monthly value realized"
          value={money.format(Number(summary.realized_monthly_savings.amount))}
          detail={`${summary.optimization_coverage_percent}% optimization coverage`}
        />
        <KpiCard
          label="Allocation coverage"
          value={`${summary.allocation_coverage_percent}%`}
          detail={`${summary.policy_compliance_percent}% policy compliance`}
        />
      </section>

      <section className="panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Prioritized action</p>
            <h2>Optimization opportunities</h2>
          </div>
          <p className="muted">Ranked by estimated value, confidence, effort, and operational risk.</p>
        </div>
        <OpportunityTable opportunities={opportunities} />
      </section>
    </main>
  );
}
