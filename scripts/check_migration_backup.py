"""Read-only inventory of an extracted OJS backup; never prints configuration values."""
import argparse
import json
from pathlib import Path
import re


def inspect_backup(folder):
    root = Path(folder).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Backup harus berupa folder yang sudah diekstrak.')
    paths = list(root.rglob('*'))
    files = [p for p in paths if p.is_file()]
    relative = lambda p: p.relative_to(root).as_posix()
    sql = [relative(p) for p in files if p.name.lower().endswith(('.sql', '.sql.gz'))]
    configs = [p for p in files if p.name == 'config.inc.php']
    code = [p.parent for p in configs if (p.parent / 'index.php').is_file()
            and (p.parent / 'lib' / 'pkp').is_dir()]
    versions = []
    for base in code:
        version = base / 'dbscripts' / 'xml' / 'version.xml'
        if version.is_file():
            match = re.search(r'<release>([^<]+)</release>', version.read_text(encoding='utf-8'))
            if match:
                versions.append(match.group(1))
    # The original files_dir may refer to a server-only path. Do not expose it.
    storage_configured = any(re.search(r'^\s*files_dir\s*=\s*\S+',
        p.read_text(encoding='utf-8', errors='replace'), re.M) for p in configs)
    public = [relative(p) for p in paths if p.is_dir() and p.name == 'public']
    plugins = [relative(p / 'plugins') for p in code if (p / 'plugins').is_dir()]
    archives = [relative(p) for p in files if p.name.lower().endswith(('.zip', '.tar', '.tar.gz', '.tgz'))]
    return {
        'database_dumps': sql,
        'ojs_config_files': [relative(p) for p in configs],
        'ojs_code_roots': [relative(p) for p in code],
        'ojs_versions_from_code': versions,
        'public_directories': public,
        'plugin_directories': plugins,
        'private_storage_configured': storage_configured,
        'archives_not_inspected': archives,
        'restore_ready': False,
        'remaining_checks': [
            'Cocokkan versi database dengan kode OJS.',
            'Identifikasi salinan files_dir dan cocokkan berkasnya dengan database.',
            'Pastikan tema/plugin asli tersedia dan kompatibel.',
            'Pulihkan ke database terpisah; uji login, submission, review, dan publikasi.',
        ],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('backup_folder')
    args = parser.parse_args()
    try:
        print(json.dumps(inspect_backup(args.backup_folder), indent=2, ensure_ascii=False))
    except (OSError, ValueError) as error:
        parser.exit(1, f'Pemeriksaan gagal: {error}\n')
