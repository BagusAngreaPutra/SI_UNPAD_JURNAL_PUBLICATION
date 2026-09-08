<?php
// Only removes the explicitly named local verification account and its test manuscripts.
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
require dirname(__DIR__) . '/ojs/tools/bootstrap.php';
$tool = new class([]) extends \PKP\cliTool\CommandLineTool {};
$user = \APP\facades\Repo::user()->getByUsername('local_test_author');
if ($user && $user->getEmail() !== 'local-test-author@localhost.test') { exit("Unexpected test account email.\n"); }
$context = \APP\core\Application::getContextDAO()->getByPath('jbmh');
$removed = 0;
foreach (\APP\facades\Repo::submission()->getCollector()->filterByContextIds([$context->getId()])->getMany() as $submission) {
    if ($submission->getCurrentPublication()->getData('title', 'en') !== 'LOCAL VERIFICATION - submission workflow') { continue; }
    $authors = $submission->getCurrentPublication()->getData('authors');
    $testAuthor = false;
    foreach ($authors as $author) { if ($author->getEmail() === 'local-test-author@localhost.test') { $testAuthor = true; } }
    if (!$testAuthor) { continue; }
    \APP\facades\Repo::submission()->delete($submission);
    $removed++;
}
if ($user) { \APP\facades\Repo::user()->delete($user); }
echo "Removed $removed test manuscripts and the local test account.\n";
