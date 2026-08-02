import type { OptimizationOpportunity } from "@/lib/types";

const money = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

export function OpportunityTable({ opportunities }: { opportunities: OptimizationOpportunity[] }) {
  return (
    <div className="table-shell">
      <table>
        <thead>
          <tr>
            <th>Opportunity</th>
            <th>Owner</th>
            <th>Monthly value</th>
            <th>Confidence</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {opportunities.map((opportunity) => (
            <tr key={opportunity.id}>
              <td>
                <strong>{opportunity.title}</strong>
                <span>{opportunity.service} · {opportunity.account_name}</span>
              </td>
              <td>{opportunity.owner_team}</td>
              <td>{money.format(Number(opportunity.estimated_monthly_savings.amount))}</td>
              <td>{opportunity.confidence_percent}%</td>
              <td><span className="status">{opportunity.status.replaceAll("_", " ")}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
