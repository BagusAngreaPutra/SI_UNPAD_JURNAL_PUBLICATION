"""Browser smoke check of the local OJS author/editor workflow using a test account."""
from pathlib import Path
import json
import re
import subprocess
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT.parent / 'UNPAD-runtime'
BASE = 'http://127.0.0.1:8000/ojs/index.php/jbmh'
secrets = json.loads((RUNTIME / 'local-secrets.json').read_text())

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', headless=True)
    author = browser.new_context()
    page = author.new_page()
    page.goto(BASE + '/user/register', wait_until='domcontentloaded')
    for name, value in {'givenName': 'Local Test', 'familyName': 'Author', 'affiliation': 'Local verification',
                        'country': 'ID', 'email': 'local-test-author@localhost.test', 'username': 'local_test_author',
                        'password': secrets['test_author_password'], 'password2': secrets['test_author_password']}.items():
        if name == 'country':
            page.locator('[name=country]').select_option(value)
        else:
            page.locator(f'[name="{name}"]').fill(value)
    page.locator('[name=privacyConsent]').check()
    page.locator('form button[type=submit]').click()
    page.get_by_text('Registration complete', exact=True).first.wait_for()
    # Start a fresh session to verify password authentication independently.
    author.close()
    author = browser.new_context()
    page = author.new_page()
    page.goto(BASE + '/login', wait_until='domcontentloaded')
    page.locator('[name=username]').fill('local_test_author')
    page.locator('[name=password]').fill(secrets['test_author_password'])
    page.locator('form button[type=submit]').click()
    page.wait_for_url('**/dashboard/**')
    page.goto(BASE + '/submission', wait_until='domcontentloaded')
    title = page.frame_locator('iframe').first.locator('body')
    title.click()
    title.press_sequentially('LOCAL VERIFICATION - submission workflow', delay=5)
    page.locator('[name=submissionRequirements]').check()
    page.locator('[name=privacyConsent]').check()
    page.get_by_role('button', name='Begin Submission', exact=True).click()
    page.get_by_text('Submission Details', exact=True).wait_for()
    submission_id = int(re.search(r'(\d+) / Author / LOCAL VERIFICATION', page.locator('body').inner_text()).group(1))
    abstract = page.frame_locator('#titleAbstract-abstract-control-en_ifr').locator('body')
    abstract.click()
    abstract.press_sequentially('Local verification of registration, file upload and editorial submission. Test content only.', delay=5)
    page.get_by_text('Submission Details', exact=True).click()
    page.wait_for_timeout(800)
    page.get_by_role('button', name='Continue', exact=True).click()
    page.locator('input[type=file]').set_input_files(str(RUNTIME / 'local-verification.docx'))
    page.get_by_role('button', name='Article Text', exact=True).click()
    for _ in range(3):
        page.get_by_role('button', name='Continue', exact=True).click()
        page.wait_for_timeout(400)
    page.get_by_role('button', name='Submit', exact=True).click()
    with page.expect_response(lambda response: response.url.endswith(f'/submissions/{submission_id}/submit') and response.request.method == 'POST') as submitted:
        page.get_by_role('button', name='Submit', exact=True).last.click()
    response = submitted.value
    assert response.status == 200, f'Submission failed: HTTP {response.status}'
    page.get_by_text('Submission complete', exact=False).first.wait_for(timeout=30000)
    text = page.locator('body').inner_text()
    print('AUTHOR:', text[-1100:])
    assert 'Submission complete' in text or 'submission has been' in text or 'Thank you' in text, 'Missing submission confirmation'
    page.goto(BASE + '/management/settings/website', wait_until='domcontentloaded')
    assert 'authorizationDenied' in page.url, 'Author could access manager settings'
    admin = browser.new_context()
    page = admin.new_page()
    page.goto(BASE + '/login', wait_until='domcontentloaded')
    page.locator('[name=username]').fill('admin')
    page.locator('[name=password]').fill(secrets['admin_password'])
    page.locator('form button[type=submit]').click()
    page.wait_for_url('**/dashboard/**')
    page.get_by_text('Needs editor', exact=True).click()
    page.get_by_text('LOCAL VERIFICATION - submission workflow', exact=False).first.wait_for()
    print('PASS: Submitted manuscript is visible in the editor queue.')
    print('PASS: Author cannot access manager settings.')
    (RUNTIME / 'smoke-result.json').write_text(json.dumps({'submission_id': submission_id, 'author_login': True, 'file_upload': True, 'submission_completed': True, 'editor_received': True, 'author_role_restricted': True}, indent=2))
    admin.storage_state(path=str(RUNTIME / 'admin-session.json'))
    browser.close()
subprocess.run(['php', '-d', 'extension=intl', str(ROOT / 'scripts/cleanup_local_test.php')], check=True, cwd=ROOT)
