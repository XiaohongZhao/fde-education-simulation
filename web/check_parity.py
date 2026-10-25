"""Compare browser decisions and drafts with the original Python reference.

Run in the complete fde-education-simulation checkout; requires Node.js and Python.
The browser deliberately omits Python's input fingerprint.
"""
import json
from pathlib import Path
import subprocess
import sys

WEB = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(WEB.parent / 'prototype'))
from education import run, load_catalog
from evaluate import check_result

spec = json.loads((WEB.parent / 'prototype/evals/cases.json').read_text())
catalog = load_catalog()
browser_data = json.loads((WEB / 'dist/data.json').read_text())
assert browser_data['catalog'] == catalog, 'Browser catalogue differs from Python'
assert browser_data['examples'] == json.loads((WEB.parent / 'prototype/data/examples.json').read_text())
inputs = [{'lead': {**spec['base'], **c['patch']}, 'asOf': c.get('as_of', '2026-10-25')}
          for c in spec['cases'] for _ in range(5)]
script = """
import {readFileSync} from 'node:fs';
import {run} from './dist/engine.mjs';
const {inputs,catalog} = JSON.parse(readFileSync(0,'utf8'));
console.log(JSON.stringify(inputs.map(({lead,asOf}) => {
  try { return {result:run(lead,catalog,asOf)}; }
  catch (e) { return {error:true}; }
})));
"""
completed = subprocess.run(['node', '--input-type=module', '-e', script], cwd=WEB,
                           input=json.dumps({'inputs':inputs,'catalog':catalog}),
                           text=True, check=True, capture_output=True)
outputs = json.loads(completed.stdout)
assert len(outputs) == len(inputs)
for i, (item, output) in enumerate(zip(inputs, outputs)):
    case = spec['cases'][i // 5]
    try:
        expected = run(item['lead'], catalog=catalog, as_of=item['asOf'])
    except ValueError:
        assert output.get('error') and case['expected'].get('error'), case['id']
        continue
    expected['trace'][-1].pop('input_fingerprint')
    assert output.get('result') == expected, f"Python/browser mismatch: {case['id']}"
    assert not check_result(output['result'], case['expected'], catalog), case['id']
print(f"PASS: {len(spec['cases'])} cases × 5 = {len(inputs)} browser executions match Python decisions, drafts and expected behaviours.")
