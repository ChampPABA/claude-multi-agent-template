// /admin/teams (P1), approved by Champ, merged to development
const partnerStatus = {
  awaiting_info: 'Awaiting info',
  needs_review: 'Needs review',
  returned: 'Returned for edits',
  active: 'Active',
}

export function TeamsPage() {
  const { teams, q, setQ, status, setStatus } = useTeams()
  return (
    <Page title="Teams" actions={<Button to="/admin/teams/new">Create team</Button>}>
      <SearchInput placeholder="Search team or team leader" value={q} onChange={setQ} />
      <Select label="Partner status" options={partnerStatus} value={status} onChange={setStatus} />
      {teams.length === 0 ? (
        <EmptyState title="No teams yet" action={<Button to="/admin/teams/new">Create team</Button>} />
      ) : (
        <Table columns={['Team', 'Team leader', 'Members', 'Partner status']} rows={teams} rowLink={(t) => `/admin/teams/${t.id}`} />
      )}
    </Page>
  )
}
