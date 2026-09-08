"""Add the supplied Fitri Anita and Muhammad Amri Bintang article."""
from pathlib import Path
from bs4 import BeautifulSoup
import shutil

ROOT = Path(__file__).resolve().parents[1]
source_pdf = ROOT / "Artikel_Fitri_dan_Bintang_JBMH.pdf"
pdf_dir = ROOT / "assets" / "pdfs"
pdf_dir.mkdir(parents=True, exist_ok=True)
pdf_target = pdf_dir / source_pdf.name
if source_pdf.exists() and not pdf_target.exists():
    shutil.move(source_pdf, pdf_target)

slug = "fitri-bintang"
url = f"/index.php/jbmh/article/view/{slug}"
pdf_url = "/assets/pdfs/Artikel_Fitri_dan_Bintang_JBMH.pdf"
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
temporary_doi = "10.24198/jbmh.v10i2.fitri-bintang"

target = ROOT / "pages" / "article" / "view" / f"{slug}.html"
if True:
    soup = BeautifulSoup((ROOT / "pages/article/view/1997.html").read_text(encoding="utf-8"), "html.parser")
    soup.title.string = f"{title} | Jurnal Bina Mulia Hukum"
    for meta in soup.find_all("meta"):
        name = (meta.get("name") or "").lower()
        if name in {"description", "og:description", "dc.description"}: meta["content"] = abstract
        elif name == "author": meta["content"] = ",".join(authors)
        elif name in {"keywords", "citation_keywords"}: meta["content"] = ",".join(keywords)
        elif name in {"dc.identifier.doi", "citation_doi"}: meta["content"] = temporary_doi
        elif name == "dc.identifier": meta["content"] = slug
        elif name in {"dc.identifier.uri", "citation_abstract_html_url"}: meta["content"] = url
        elif name == "citation_pdf_url": meta["content"] = pdf_url
        elif name in {"dc.title", "citation_title"}: meta["content"] = title
        elif name == "dc.identifier.pagenumber": meta["content"] = "166-178"
    soup.select_one("h1.article-title").string = title
    creator_metas = soup.find_all("meta", attrs={"name": "DC.Creator.PersonalName"})
    citation_authors = soup.find_all("meta", attrs={"name": "citation_author"})
    citation_affiliations = soup.find_all("meta", attrs={"name": "citation_author_institution"})
    for metas, values in ((creator_metas, authors), (citation_authors, authors)):
        for meta, value in zip(metas, values): meta["content"] = value
        for meta in metas[len(values):]: meta["content"] = ""
    for meta in citation_affiliations:
        meta["content"] = "Fakultas Hukum, Universitas Prof. Hazairin, SH."
    doi = soup.select_one(".list-group-item.doi")
    if doi:
        doi_link = doi.select_one("a.doi_link")
        doi_link["href"] = url
        doi_link.string = temporary_doi + " (sementara, belum terdaftar)"
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
    badge = soup.select_one(".dimension_badge")
    if badge: badge.decompose()
    citation = soup.select_one(".csl-entry")
    if citation: citation.string = f"Anita, F., & Bintang, M. A. (2026). {title}. Jurnal Bina Mulia Hukum, 10(2), 166-178."
    references = soup.select_one(".article-references")
    if references: references.decompose()
    target.write_text(str(soup), encoding="utf-8", newline="\n")

card = f'''\n<div class="article-summary media fitri-bintang-article">
  <div class="media-body article_summary">
    <h3 class="media-heading"><a href="{url}" class="article_name">{title}</a></h3>
    <div class="meta row">
      <div class="col-md-12 col-xs-12">
        <span class="pull-left pages"><i class="fa fa-file-text-o" aria-hidden="true"></i> <span class="page_number">166-178</span></span>
        <span class="pull-right author"><i class="fa fa-users"></i> Fitri Anita, Muhammad Amri Bintang</span>
      </div>
    </div>
    <div class="row">
      <div class="col-md-8 col-xs-12"><a class="galley-link pdf" href="{pdf_url}"><span class="gallery_item_link"><i class="fa fa-paperclip"></i> PDF</span></a></div>
    </div>
  </div>
</div>\n'''
for listing in [ROOT / "index.html", ROOT / "home.html", ROOT / "pages/issue/view/143.html"]:
    text = listing.read_text(encoding="utf-8")
    if "fitri-bintang-article" not in text:
        text = text.replace('<div class="media-list">', '<div class="media-list">' + card, 1)
        listing.write_text(text, encoding="utf-8", newline="\n")
