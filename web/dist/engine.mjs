// Browser port of prototype/education.py. No network calls or external writes.
const required = ['age', 'goal', 'budget', 'level', 'availability', 'format'];
const allowed = new Set(['id', ...required, 'consent_followup', 'intent', 'message', 'requested_course', 'opt_out']);
const intents = new Set(['consult', 'trial', 'enroll', 'refund', 'job_guarantee']);
export function validateInput(lead) {
  if (!lead || Array.isArray(lead) || typeof lead !== 'object') throw Error('Input must be a JSON object');
  if (Object.keys(lead).some(k => !allowed.has(k))) throw Error('Unsupported input fields');
  for (const key of ['id', 'goal', 'format', 'intent', 'message', 'requested_course']) {
    if (lead[key] != null && typeof lead[key] !== 'string') throw Error(`${key} must be a string`);
  }
  for (const key of ['age', 'level']) {
    if (lead[key] != null && (!Number.isInteger(lead[key]) || lead[key] < 0)) throw Error(`${key} must be a non-negative integer`);
  }
  if (lead.age > 120) throw Error('age is outside the supported range');
  if (lead.level > 2) throw Error('level must be 0, 1 or 2');
  if (lead.budget != null && (typeof lead.budget !== 'number' || !Number.isFinite(lead.budget) || lead.budget < 0)) throw Error('budget must be a finite non-negative number');
  for (const key of ['consent_followup', 'opt_out']) {
    if (key in lead && typeof lead[key] !== 'boolean') throw Error(`${key} must be a boolean`);
  }
  if (lead.availability != null && (!Array.isArray(lead.availability) || lead.availability.some(x => typeof x !== 'string'))) throw Error('availability must be a list of strings');
  if (!intents.has('intent' in lead ? lead.intent : 'consult')) throw Error('intent is not supported');
  if ([...(lead.message || '')].length > 8000) throw Error('message exceeds 8,000 characters');
}
function validDate(s) {
  return typeof s === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(s) && !Number.isNaN(Date.parse(s)) && new Date(s).toISOString().slice(0,10) === s;
}
export function run(lead, catalog, asOf = '2026-10-25') {
  validateInput(lead);
  if (!validDate(asOf)) throw Error('Enter a valid simulation date');
  if (!catalog?.version) throw Error('Catalogue version is missing');
  if (!validDate(catalog.valid_from) || !validDate(catalog.valid_until) || catalog.valid_from > catalog.valid_until) throw Error('Invalid catalogue validity period');
  const ids = new Set();
  for (const c of catalog.courses) {
    if (ids.has(c.id)) throw Error('Duplicate course ID');
    ids.add(c.id);
    if (!Number.isInteger(c.price) || c.price < 0) throw Error('Invalid course price');
    if (!Number.isInteger(c.seats) || c.seats < 0) throw Error('Invalid course capacity');
    if (c.level_min > c.level_max) throw Error('Invalid course-level range');
    if (Number.isNaN(Date.parse(c.trial_at))) throw Error('Invalid trial date');
  }
  const missing = required.filter(k => lead[k] == null || lead[k] === '' || (Array.isArray(lead[k]) && !lead[k].length));
  let route = 'human_review', reason = 'no_match', selected = [];
  if (lead.age != null && lead.age < 18) reason = 'minor';
  else if (['refund','job_guarantee','enroll'].includes(lead.intent)) reason = lead.intent === 'enroll' ? 'enrollment' : lead.intent;
  else if (asOf < catalog.valid_from || asOf > catalog.valid_until) reason = 'stale_catalog';
  else if (missing.length) { route = 'clarify'; reason = 'missing_fields'; }
  else {
    selected = catalog.courses.filter(c => c.active && c.seats > 0 && c.goals.includes(lead.goal) && lead.budget >= c.price && c.level_min <= lead.level && lead.level <= c.level_max && lead.availability.includes(c.slot) && ['any', c.format].includes(lead.format)).sort((a,b) => a.price-b.price || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
    if (lead.requested_course && !selected.some(c => c.id === lead.requested_course)) { selected = []; reason = 'conflicting_request'; }
    else if (selected.length) {
      if (lead.requested_course) selected = selected.filter(c => c.id === lead.requested_course);
      route = 'recommend'; reason = 'matched';
    }
  }
  const recommendations = selected.map(c => ({id:c.id,name:c.name,price:c.price,weeks:c.weeks,slot:c.slot,format:c.format,source:`catalog:${catalog.version}:${c.id}`}));
  const trial_proposals = lead.intent === 'trial' && route === 'recommend' ? selected.filter(c => c.trial_at.slice(0,10) > asOf).map(c => ({course_id:c.id,trial_at:c.trial_at,status:'proposal_only'})) : [];
  const eligible = lead.consent_followup === true && !lead.opt_out && route === 'recommend' && lead.age >= 18;
  const followup_task = eligible ? {kind:trial_proposals.length ? 'contact_after_trial' : 'course_consultation',status:'draft',owner:'Admissions adviser',prerequisite:trial_proposals.length ? 'actual_trial_attendance_and_contact_permission_confirmed' : 'contact_permission_reconfirmed'} : null;
  const result = {mode:'offline',as_of:asOf,route,reason,missing,catalog_version:catalog.version,recommendations,trial_proposals,followup_task,requires_human_review:true,external_actions:[],llm:{status:'not_requested'}};
  result.draft = draftText(result);
  result.trace = [
    {stage:'intake',missing,note:'Decisions use structured fields; message is for human reference only, without automated intent recognition'},
    {stage:'match',route,reason,selected:selected.map(c => c.id),catalog_version:catalog.version},
    {stage:'draft',type:'deterministic_template',sources:recommendations.map(c => c.source)},
    {stage:'policy',followup_allowed:eligible,external_write_enabled:false},
    {stage:'audit',review_required:true},
  ];
  return result;
}
function draftText(r) {
  let text;
  if (r.route === 'clarify') {
    const labels = {age:'age',goal:'learning goal',budget:'budget ceiling',level:'current skill level',availability:'available class times',format:'online or in-person preference'};
    text = `Please provide: ${r.missing.map(k => labels[k]).join(', ')}. We can then check suitable courses.`;
  } else if (r.route === 'recommend') {
    const lines = [`Based on the confirmed information, consider these courses (catalogue ${r.catalog_version}):`];
    r.recommendations.forEach(c => lines.push(`${c.name}: CNY ${c.price}, ${c.weeks} weeks, ${c.slot}, ${c.format}. [${c.source}]`));
    lines.push('This is course advice, not confirmation of enrolment or a promise of employment outcomes.');
    if (r.trial_proposals.length) lines.push('Trial times for human confirmation: ' + r.trial_proposals.map(t => t.course_id+' '+t.trial_at).join('; ') + '; no booking has been made.');
    text = lines.join('\n');
  } else {
    text = {
      minor:'This case serves adults only. A person must confirm the service scope for this enquiry.',
      refund:'Refunds require a person to check the order, contract and attendance. No amount or payment date is determined here.',
      job_guarantee:'The courses do not guarantee employment, salary or admission outcomes. An adviser should explain these expectations.',
      enrollment:'Enrolment requires a person to check capacity, the contract and payment status. No enrolment or payment has been completed here.',
      stale_catalog:'The catalogue is outside its validity period. A person must update and confirm prices and schedules.',
      conflicting_request:'The requested course conflicts with confirmed goals, budget or availability. An adviser should check before selecting a course.',
      no_match:'No current course satisfies the goal, budget, prior knowledge and timing together. Please discuss alternatives with an adviser.',
    }[r.reason];
  }
  if (r.followup_task) text += '\nA follow-up task draft is ready for adviser review. No message has been sent.';
  return text;
}
