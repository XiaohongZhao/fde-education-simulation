import { run } from './engine.mjs';

const $ = id => document.getElementById(id);
const escape = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels = {matched:'A suitable course is available',minor:'Adult service scope needs confirmation',refund:'Refund request needs a person',job_guarantee:'Employment outcomes cannot be promised',enrollment:'Enrolment needs human confirmation',stale_catalog:'Catalogue needs an update',conflicting_request:'Requested course does not fit',no_match:'No course meets every requirement',missing_fields:'A few details are still needed'};
const names = {age:'age',goal:'learning goal',budget:'budget',level:'skill level',availability:'available times',format:'learning format'};
let data, result, dirty = false;

function readLead() {
  const number = id => $(id).value === '' ? null : Number($(id).value);
  return {id:'BROWSER-DEMO',age:number('age'),budget:number('budget'),level:number('level'),goal:$('goal').value,format:$('format').value,intent:$('intent').value,availability:['weekend','weekday_evening'].filter(id => $(id).checked),consent_followup:$('consent_followup').checked,opt_out:$('opt_out').checked,requested_course:$('requested_course').value};
}
function setPreset(index) {
  const lead = data.examples[index];
  for (const id of ['age','budget','level','goal','format','intent']) $(id).value = lead[id] ?? '';
  for (const id of ['weekend','weekday_evening']) $(id).checked = lead.availability.includes(id);
  $('consent_followup').checked = lead.consent_followup;
  $('opt_out').checked = false; $('requested_course').value = ''; $('as_of').value = '2026-10-25';
  document.querySelectorAll('[data-preset]').forEach(b => b.setAttribute('aria-pressed', String(Number(b.dataset.preset) === index)));
  activateTab('reply'); simulate();
}
function simulate() {
  try {
    result = run(readLead(), data.catalog, $('as_of').value);
    dirty = false; $('stale').hidden = true; $('form-error').hidden = true;
    $('action-status').textContent = ''; $('copy').disabled = false; $('download').disabled = false;
    renderResult();
  } catch (error) {
    $('form-error').textContent = error.message; $('form-error').hidden = false;
    markDirty();
  }
}
function markDirty() {
  dirty = true; $('stale').hidden = false; $('copy').disabled = true; $('download').disabled = true;
  $('action-status').textContent = '';
  document.querySelectorAll('[data-preset]').forEach(b => b.setAttribute('aria-pressed','false'));
}
function renderResult() {
  const r = result;
  const mode = r.route === 'recommend' ? '' : r.route === 'clarify' ? 'clarify' : 'review';
  const title = r.route === 'recommend' ? 'Course match found' : r.route === 'clarify' ? 'Clarification needed' : 'Hand over to an adviser';
  const subtitle = r.route === 'clarify' ? `Please confirm ${r.missing.map(k => names[k]).join(', ')}.` : labels[r.reason];
  const courseCards = r.recommendations.map(c => `<article class="course-card"><span class="code">${escape(c.id)} · CATALOGUE MATCH</span><h3>${escape(c.name)}</h3><div class="price"><span>CNY</span><strong>${c.price.toLocaleString('en-GB')}</strong></div><div class="course-meta"><span>${c.weeks} weeks</span><span>${c.slot === 'weekend' ? 'Weekends' : 'Weekday evenings'}</span><span>${c.format === 'online' ? 'Online' : 'In person'}</span></div><p class="source">Source: ${escape(c.source)}</p></article>`).join('');
  const trials = r.trial_proposals.map(t => `<strong>${escape(t.course_id)} · ${escape(t.trial_at.slice(0,10))}</strong><p>${escape(t.trial_at.slice(11,16))} (UTC+08:00) · proposal only</p>`).join('');
  const trialNote = r.trial_proposals.length ? trials : '<strong>No trial proposed</strong><p>Requires a matching course, a trial request and a future session.</p>';
  const followup = r.followup_task ? `<strong>Draft ready for review</strong><p>${r.followup_task.kind === 'contact_after_trial' ? 'After the trial, once attendance and contact permission are confirmed.' : 'Reconfirm contact permission before contacting the learner.'}</p>` : '<strong>No follow-up task</strong><p>Requires a course match and valid contact permission.</p>';
  $('result').innerHTML = `<div class="outcome-banner ${mode}"><span class="outcome-icon" aria-hidden="true">${r.route === 'recommend' ? '✓' : '↗'}</span><div><h3>${title}</h3><p>${escape(subtitle)}</p></div></div>${courseCards}<div class="actions-grid"><div class="action-card"><span class="section-label">TRIAL SESSION</span>${trialNote}</div><div class="action-card"><span class="section-label">FOLLOW-UP</span>${followup}</div></div>`;
  $('draft').textContent = r.draft;
  const steps = [
    ['Intake',r.missing.length ? `Missing details: ${r.missing.map(k => names[k]).join(', ')}.` : 'All six required fields are present. Decisions use the structured profile.'],
    ['Catalogue match',`${labels[r.reason]}. Catalogue ${r.catalog_version}; simulation date ${r.as_of}.`],
    ['Response draft','An English template uses only the verified result and source references. No live model call.'],
    ['Contact permission',r.followup_task ? 'Permission is present and not withdrawn. A draft task is proposed; no external action is taken.' : 'No follow-up task is created for this profile.'],
    ['Review & handoff','Human review remains required. Nothing has been sent, booked, charged or written to a CRM.'],
  ];
  $('trace').innerHTML = steps.map(([title,body],i) => `<li><span class="step">${i+1}</span><div><h4>${title}</h4><p>${escape(body)}</p></div></li>`).join('');
  $('json').textContent = JSON.stringify(r,null,2);
}
function activateTab(view, focus = false) {
  document.querySelectorAll('[data-view]').forEach(button => {
    const active = button.dataset.view === view;
    button.setAttribute('aria-selected',String(active)); button.tabIndex = active ? 0 : -1;
    $('view-'+button.dataset.view).hidden = !active;
    if (active && focus) button.focus();
  });
}
document.querySelectorAll('[data-view]').forEach(button => {
  button.addEventListener('click', () => activateTab(button.dataset.view));
  button.addEventListener('keydown', e => {
    const tabs = [...document.querySelectorAll('[data-view]')]; const index = tabs.indexOf(button);
    const next = {ArrowRight:(index+1)%3,ArrowLeft:(index+2)%3,Home:0,End:2}[e.key];
    if (next !== undefined) { e.preventDefault(); activateTab(tabs[next].dataset.view,true); }
  });
});
$('lead-form').addEventListener('submit', e => { e.preventDefault(); simulate(); });
$('lead-form').addEventListener('input', markDirty);
$('lead-form').addEventListener('change', markDirty);
$('reset').addEventListener('click', () => setPreset(0));
document.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => setPreset(Number(button.dataset.preset))));
$('copy').addEventListener('click', async () => {
  if (dirty || !result) return;
  try { await navigator.clipboard.writeText(result.draft); $('action-status').textContent = 'Draft copied.'; }
  catch { $('action-status').textContent = 'Copy is unavailable in this browser. Select the draft text to copy it.'; }
});
$('download').addEventListener('click', () => {
  if (dirty || !result) return;
  const url = URL.createObjectURL(new Blob([JSON.stringify(result,null,2)+'\n'],{type:'application/json'}));
  const a = document.createElement('a'); a.href = url; a.download = 'course-advisory-result.json'; a.click();
  setTimeout(() => URL.revokeObjectURL(url),1000); $('action-status').textContent = 'Result prepared for download.';
});
try {
  const response = await fetch('./data.json'); if (!response.ok) throw Error('Data could not be loaded');
  data = await response.json();
  data.catalog.courses.forEach(c => {
    const option = document.createElement('option'); option.value = c.id;
    option.textContent = `${c.name}${!c.active ? ' (discontinued)' : c.seats === 0 ? ' (full)' : ''}`;
    $('requested_course').append(option);
  });
  setPreset(0); $('workspace').hidden = false; $('loading').hidden = true;
} catch (error) {
  $('loading').textContent = 'The simulator could not load. Please refresh the page or open the GitHub project for the offline version.';
  $('loading').className = 'error';
  document.querySelectorAll('[data-preset]').forEach(b => b.disabled = true);
}
