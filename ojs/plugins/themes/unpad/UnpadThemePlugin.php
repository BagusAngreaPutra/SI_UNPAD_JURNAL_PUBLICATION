<?php
namespace APP\plugins\themes\unpad;

class UnpadThemePlugin extends \PKP\plugins\ThemePlugin
{
    public function init()
    {
        $this->setParent('defaultthemeplugin');
    }
    public function getDisplayName() { return 'UNPAD Public Website'; }
    public function getDescription() { return 'Original public header and sidebar with native OJS forms.'; }
}
