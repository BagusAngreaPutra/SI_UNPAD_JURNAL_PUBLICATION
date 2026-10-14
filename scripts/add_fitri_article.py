"""Add the supplied Fitri Anita and Muhammad Amri Bintang article."""
from pathlib import Path
from bs4 import BeautifulSoup
import shutil

ROOT = Path(__file__).resolve().parents[1]
source_pdf = ROOT / "Artikel Fitri dan Bintang JBMH.pdf"
pdf_dir = ROOT / "assets" / "pdfs"
pdf_dir.mkdir(parents=True, exist_ok=True)
pdf_target = pdf_dir / "Artikel_Fitri_dan_Bintang_JBMH.pdf"
if source_pdf.exists():
    shutil.copy2(source_pdf, pdf_target)

slug = "2534"
url = f"/index.php/jbmh/article/view/{slug}"
pdf_url = "/article-stats.php?action=download&v=" + __import__('hashlib').sha256(pdf_target.read_bytes()).hexdigest()[:12]
title = ("Reformulasi Pengaturan Victim Impact Statement (VIS) sebagai Penguatan Hak "
         "Korban dalam Sistem Peradilan Pidana Indonesia")
abstract = ("Undang-Undang Nomor 20 Tahun 2025 tentang Kitab Undang-Undang Hukum Acara "
            "Pidana mengakui hak korban untuk menyampaikan Victim Impact Statement (VIS) "
            "dalam Pasal 144 huruf x. Pengakuan ini memperkuat orientasi peradilan pidana "
            "yang berpusat pada korban, tetapi normanya masih deklaratif karena belum "
            "mengatur definisi, subjek, bentuk, waktu penyampaian, pendampingan, kewajiban "
            "hakim, dan hubungan VIS dengan pemulihan korban. Penelitian ini menganalisis "
            "urgensi reformulasi VIS dan merumuskan desain pengaturan yang operasional. "
            "Hasil penelitian menunjukkan bahwa VIS harus diposisikan sebagai hak prosedural "
            "sekaligus instrumen pengakuan, partisipasi, dan pemulihan korban.")
authors = ["Fitri Anita", "Muhammad Amri Bintang"]
keywords = ["Victim Impact Statement", "Hak Korban", "Peradilan Pidana", "KUHAP"]
simulation_url = "https://doi-reg.org/10.2498.jbmh.v10i2.2330"
references = [
    "Cruz, Peter de. Comparative Law in a Changing World. 4th ed. London: Routledge, 2020.",
    "Hadjon, Philipus M. Perlindungan Hukum bagi Rakyat Indonesia. Surabaya: Bina Ilmu, 1987.",
    "Hadjon, Philipus M., dan Tatiek Sri Djatmiati. Argumentasi Hukum. Yogyakarta: Gadjah Mada University Press, 2020.",
    "Hall, Matthew. Victims of Crime: Policy and Practice in Criminal Justice. New York: Routledge, 2022.",
    "Honneth, Axel. The Struggle for Recognition. Cambridge: Polity Press, 1995.",
    "Hutchinson, Terry. Researching and Writing in Law. 5th ed. Sydney: Thomson Reuters, 2021.",
    "Ibrahim, Johnny. Teori dan Metodologi Penelitian Hukum Normatif. Malang: Bayumedia Publishing, 2019.",
    "Indrati, Maria Farida. Ilmu Perundang-Undangan. Yogyakarta: Kanisius, 2023.",
    "Karmen, Andrew. Crime Victims: An Introduction to Victimology. 10th ed. Boston: Cengage Learning, 2024.",
    "Marshall, Tony F. Restorative Justice: An Overview. London: Home Office Research Development and Statistics Directorate, 1999.",
    "Marzuki, Peter Mahmud. Penelitian Hukum. Edisi Revisi. Jakarta: Kencana, 2021.",
    "Soeharto, H. Perlindungan Hak Tersangka, Terdakwa, dan Korban Tindak Pidana dalam Sistem Peradilan Pidana Indonesia. Bandung: Refika Aditama, 2007.",
    "Wemmers, Jo-Anne. Victims in the Criminal Justice System. Leiden: Brill, 2023.",
    "Batchelor, Diana. “Talking Punishment: How Victim Perceptions of Punishment Change When They Communicate with Offenders.” Punishment & Society Vol. 25, No. 2 (2023): 519-536.",
    "Cassell, Paul G., dan Edna Erez. “How Victim Impact Statements Promote Justice: Evidence from the Content of Statements Delivered in Larry Nassar’s Sentencing.” Marquette Law Review Vol. 107, No. 4 (2024): 861.",
    "Herman, dan Ufran. “Victim Impact Statement sebagai Instrumen Penguatan Hak Korban dalam Sistem Peradilan Pidana Indonesia.” Indonesian Journal of Criminal Law and Criminology Vol. 5, No. 2 (2024): 175-189.",
    "Kragting, Marleen, Freya Augusteijn, Alice Bosma, Nieke Elbers, dan Antony Pemberton. “Victim Impact Statements in the Courtroom: Agency and Communion in Communication with Victims.” International Review of Victimology, OnlineFirst (2025). DOI: 10.1177/02697580251389013.",
    "Laxminarayan, Malini, Mark Bosmans, Robert Porter, dan Lorena Sosa. “Victim Satisfaction with Criminal Justice: A Systematic Review.” Victims & Offenders Vol. 8, No. 2 (2013): 119-147.",
    "Lens, Kim M.E., Antony Pemberton, dan Stefan Bogaerts. “Heterogeneity in Victim Participation: A New Perspective on Delivering a Victim Impact Statement.” European Journal of Criminology Vol. 10, No. 4 (2013): 479-495.",
    "Lens, Kim M.E., Antony Pemberton, Karen Brans, Johan Braeken, Stefan Bogaerts, dan Esmah Lahlah. “Delivering a Victim Impact Statement: Emotionally Effective or Counter-Productive?” European Journal of Criminology Vol. 12, No. 1 (2015): 17-34.",
    "Mastrocinque, Jeanna M. “Victim Personal Statements: An Analysis of Notification and Utilization.” Criminology & Criminal Justice Vol. 14, No. 2 (2014): 216-234.",
    "Pemberton, Antony, Pauline G.M. Aarten, dan Eva Mulder. “Beyond Retribution, Restoration and Procedural Justice: The Big Two of Communion and Agency in Victims’ Perspectives on Justice.” Psychology, Crime & Law Vol. 23, No. 7 (2017): 682-698.",
    "Ramadianto, Anang Riyan, Milda Istiqomah, dan Nurini Aprilianda. “Victim Impact Statement as a Model of Victim-Centered Justice.” Jurnal Hukum IUS QUIA IUSTUM Vol. 32, No. 2 (2025): 337-360.",
    "Roberts, Julian V., dan Edna Erez. “Communication in Sentencing: Exploring the Expressive Function of Victim Impact Statements.” International Review of Victimology Vol. 10, No. 3 (2004): 223-244.",
    "Susetyo, Heru. “Pemenuhan dan Perlindungan Hak-Hak Prosedural Korban Terorisme atas Victim Impact Statements dalam Sistem Peradilan Pidana.” The Southeast Asian Journal of Victimology Vol. 3, No. 1 (2024): 90-108.",
    "Walklate, Sandra, JaneMaree Maher, Jude McCulloch, Kate Fitz-Gibbon, dan Kara Beavis. “Victim Stories and Victim Policy: Is There a Case for a Narrative Victimology?” Crime, Media, Culture Vol. 15, No. 2 (2019): 199-215.",
    "Indonesia. Undang-Undang Nomor 1 Tahun 2023 tentang Kitab Undang-Undang Hukum Pidana.",
    "Indonesia. Undang-Undang Nomor 20 Tahun 2025 tentang Kitab Undang-Undang Hukum Acara Pidana.",
    "Mahkamah Agung Republik Indonesia. Putusan Nomor 5642 K/Pid.Sus/2022.",
    "United Nations. Declaration of Basic Principles of Justice for Victims of Crime and Abuse of Power. A/RES/40/34. New York: United Nations, 1985.",
]

target = ROOT / "pages" / "article" / "view" / f"{slug}.html"
if True:
    soup = BeautifulSoup((ROOT / "pages/article/view/1997.html").read_text(encoding="utf-8"), "html.parser")
    soup.title.string = f"{title} | Jurnal Bina Mulia Hukum"
    for meta in soup.find_all("meta"):
        name = (meta.get("name") or "").lower()
        if name in {"description", "og:description", "dc.description"}: meta["content"] = abstract
        elif name == "author": meta["content"] = ",".join(authors)
        elif name in {"keywords", "citation_keywords"}: meta["content"] = ",".join(keywords)
        elif name in {"dc.identifier.doi", "citation_doi"}: meta.decompose()
        elif name == "dc.identifier": meta["content"] = slug
        elif name in {"dc.identifier.uri", "citation_abstract_html_url"}: meta["content"] = url
        elif name == "citation_pdf_url": meta["content"] = pdf_url
        elif name in {"dc.title", "citation_title"}: meta["content"] = title
        elif name == "dc.identifier.pagenumber": meta["content"] = "179-186"
        elif name == "citation_firstpage": meta["content"] = "179"
        elif name == "citation_lastpage": meta["content"] = "186"
        elif name == "dc.date.issued": meta["content"] = "2026-09"
        elif name == "citation_date": meta["content"] = "2026/09"
        elif name in {"dc.date.created", "dc.date.datesubmitted", "dc.date.modified"}: meta.decompose()
        elif name in {"dc.language", "citation_language"}: meta["content"] = "id"
        elif name == "dc.rights" and "Copyright" in meta.get("content", ""):
            meta["content"] = "Copyright (c) 2026 Fitri Anita, Muhammad Amri Bintang"
        elif name == "generator" and "Sarak Opat" in meta.get("content", ""): meta.decompose()
        elif name == "citation_journal_abbrev": meta["content"] = "JBMH"
    soup.select_one("h1.article-title").string = title
    creator_metas = soup.find_all("meta", attrs={"name": "DC.Creator.PersonalName"})
    citation_authors = soup.find_all("meta", attrs={"name": "citation_author"})
    citation_affiliations = soup.find_all("meta", attrs={"name": "citation_author_institution"})
    subject_metas = soup.find_all("meta", attrs={"name": "DC.Subject"})
    for metas, values in ((creator_metas, authors), (citation_authors, authors)):
        for meta, value in zip(metas, values): meta["content"] = value
        for meta in metas[len(values):]: meta.decompose()
    for meta in citation_affiliations:
        meta["content"] = "Fakultas Hukum, Universitas Prof. Hazairin, SH."
    for meta, keyword in zip(subject_metas, keywords): meta["content"] = keyword
    for meta in subject_metas[len(keywords):]: meta["content"] = ""
    doi = soup.select_one(".list-group-item.doi")
    if doi:
        doi_link = doi.select_one("a.doi_link")
        doi_link["href"] = simulation_url
        doi_link.string = simulation_url
    author_nodes = soup.select(".authors .author")
    for node in author_nodes[2:]: node.decompose()
    for node, name in zip(author_nodes, authors):
        node.select_one(".full_name").string = name
        affiliation = node.select_one(".article-author-affilitation")
        if affiliation: affiliation.string = "Fakultas Hukum, Universitas Prof. Hazairin, SH."
    contact = author_nodes[0].select_one(".primary_contact")
    if contact: contact.clear(); contact.append(" fnita7489@gmail.com (Primary Contact)")
    summary = soup.select_one(".article-abstract")
    summary.clear(); paragraph = soup.new_tag("p"); paragraph.string = abstract; summary.append(paragraph)
    keyword_box = soup.select_one(".article-details-keywords-value")
    keyword_box.clear()
    for keyword in keywords:
        span = soup.new_tag("span", attrs={"class": "keyword_item"}); span.string = keyword; keyword_box.append(span)
    galley = soup.select_one("a.galley-link.pdf"); galley["href"] = pdf_url
    statistic_values = soup.select(".article-sidebar .galley_list b")
    for value, key, initial in zip(statistic_values[:2], ['read', 'download'], ['10', '3']):
        value.string = initial
        value['data-vis-' + key] = ''
    soup.body['data-vis-article'] = ''
    soup.body.append(soup.new_tag('script', src='/assets/article-stats.js', defer=True))
    badge = soup.select_one(".dimension_badge")
    if badge: badge.decompose()
    citation = soup.select_one(".csl-entry")
    if citation: citation.string = f"Anita, F., & Bintang, M. A. (2026). {title}. Jurnal Bina Mulia Hukum, 10(2), 179-186."
    for group in soup.select('.how-to-cite .btn-group'): group.decompose()
    for link in soup.select('.citation_download a'):
        format_name = 'ris' if '/ris?' in link.get('href', '') else 'bib'
        link['href'] = f'/assets/citations/2534.{format_name}'
        link['download'] = ''
    reference_box = soup.select_one("#articleCitations > div")
    if reference_box:
        reference_box.clear()
        for reference in references:
            item = soup.new_tag("p"); item.string = reference; reference_box.append(item)
    reference_list = soup.select_one(".article-references-content ol")
    if reference_list:
        reference_list.clear()
        for reference in references:
            item = soup.new_tag("li"); item.string = reference; reference_list.append(item)
    target.write_text(str(soup), encoding="utf-8", newline="\n")

card = f'''\n<div class="article-summary media fitri-bintang-article">
  <div class="media-body article_summary">
    <h3 class="media-heading"><a href="{url}" class="article_name">{title}</a></h3>
    <div class="meta row">
      <div class="col-md-12 col-xs-12 journal_index_doi"><span class="doi_logo"></span><a href="{simulation_url}" class="doi_link">{simulation_url.rsplit('/', 1)[-1]}</a></div>
      <div class="col-md-12 col-xs-12">
        <span class="pull-left pages"><i class="fa fa-file-text-o" aria-hidden="true"></i> <span class="page_number">179-186</span></span>
        <span class="pull-right author"><i class="fa fa-users"></i> Fitri Anita, Muhammad Amri Bintang</span>
      </div>
    </div>
    <div class="row">
      <div class="col-md-8 col-xs-12"><a class="galley-link pdf" href="{pdf_url}"><span class="gallery_item_link"><i class="fa fa-paperclip"></i> PDF</span></a></div>
      <div class="col-md-4 col-xs-12 stat_counter"><span class="article_counter_read"></span> <span class="hidden-xs">Read: <span data-vis-read>10</span> | Download: <span data-vis-download>3</span></span></div>
    </div>
  </div>
</div>\n'''
for listing in [ROOT / "index.html", ROOT / "home.html", ROOT / "pages/issue/view/143.html"]:
    text = listing.read_text(encoding="utf-8")
    text = text.replace('/index.php/jbmh/article/view/fitri-bintang', url)
    listing_soup = BeautifulSoup(text, "html.parser")
    existing = listing_soup.select_one('.fitri-bintang-article')
    if existing: existing.decompose()
    next_article = listing_soup.select_one('a.article_name[href$="/article/view/2533"]')
    if next_article:
        next_article.find_parent('div', class_='article-summary').insert_before(BeautifulSoup(card, "html.parser"))
    else:
        listing_soup.select_one('.media-list').append(BeautifulSoup(card, "html.parser"))
    text = str(listing_soup)
    if '/assets/article-stats.js' not in text:
        text = text.replace('</body>', '<script src="/assets/article-stats.js" defer></script></body>')
    listing.write_text(text, encoding="utf-8", newline="\n")
