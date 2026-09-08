<?php
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
require dirname(__DIR__) . '/ojs/tools/bootstrap.php';
$tool = new class([]) extends \PKP\cliTool\CommandLineTool {};
$dao = \APP\core\Application::getContextDAO();
$context = $dao->getByPath('jbmh');
if (!$context) {
    $context = $dao->newDataObject();
    $context->setData('urlPath', 'jbmh');
    $context->setData('enabled', true);
    $context->setData('primaryLocale', 'en');
    $context->setData('supportedLocales', ['en', 'id']);
    $context->setData('supportedFormLocales', ['en', 'id']);
    $context->setData('name', 'Jurnal Bina Mulia Hukum', 'en');
    $context->setData('name', 'Jurnal Bina Mulia Hukum', 'id');
    $context->setData('acronym', 'JBMH', 'en');
    $context->setData('contactName', 'Journal Administrator');
    $context->setData('contactEmail', 'admin@localhost.test');
    $context->setData('supportName', 'Journal Administrator');
    $context->setData('supportEmail', 'admin@localhost.test');
    $context->setData('onlineIssn', '2540-9034');
    $context->setData('printIssn', '2528-7273');
    $context->setData('publisherInstitution', 'Universitas Padjadjaran');
    $context->setData('themePluginPath', 'default');
    $context = \APP\core\Services::get('context')->add($context, \APP\core\Application::get()->getRequest());
}
$context->setData('themePluginPath', 'unpad');
\PKP\db\DAORegistry::getDAO('PluginSettingsDAO')->updateSetting($context->getId(), 'unpadthemeplugin', 'enabled', true, 'bool');
$context->setData('disableUserReg', false);
$context->setData('disableSubmissions', false);
foreach (['authorGuidelines' => 'pages/authorguidelines.html', 'about' => 'About/about_journal.html'] as $setting => $source) {
    $doc = new DOMDocument();
    @$doc->loadHTML(file_get_contents(dirname(__DIR__) . '/' . $source));
    $main = $doc->getElementById('main-content');
    if ($main) {
        $html = '';
        foreach ($main->childNodes as $node) { $html .= $doc->saveHTML($node); }
        $context->setData($setting, $html, 'en');
    }
}
$dao->updateObject($context);
echo 'Journal ready: ' . $context->getPath() . ' (ID ' . $context->getId() . ")\n";
