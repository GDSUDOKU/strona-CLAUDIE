#!/usr/bin/env python3
"""Dymczak Legal — static site generator (PL / EN / DE).

Run:  python3 build.py
Output: pl/, en/, de/, index.html, 404.html, sitemap.xml, robots.txt, CNAME

All texts live in this file. Fill in CONFIG first — anything left empty
shows up as a yellow [...] marker on the legal-notice page and is listed
in the console when you run the script.
"""
import html, json, datetime, pathlib

ROOT = pathlib.Path(__file__).parent

# ----------------------------------------------------------------------------
# CONFIG — fill in before publishing
# ----------------------------------------------------------------------------
CONFIG = {
    "domain": "dymczaklegal.com",
    "email": "grzegorz.dymczak@gmail.com", # consider a mailbox on your own domain later
    "phone": "+48 799 886 934",            # optional
    "city": "",                            # optional, shown in the contact card, e.g. "Wrocław"
    "address": "Braniborska 74, 53-680 Wrocław",  # required in the legal notice
    "nip": "",                             # NIP — leave empty until you have one; the line is then hidden
    "chamber": "Wrocław",                  # Okręgowa Izba Radców Prawnych w ...
    "entry_no": "WR-4479",                 # number on the list of legal counsels
    "insurance_url": "https://oirp.wroclaw.pl/radcowie/ubezpieczenia",  # OC via the chamber
    "insurance_scope_de": "",              # German notice only: territorial scope of the cover (see certificate / broker)
    "show_employers": True,                # name former employers in the About section
}

MISSING = []
YEAR = datetime.date.today().year
TODAY = datetime.date.today().isoformat()
BASE = "https://" + CONFIG["domain"]
LANGS = ["pl", "en", "de"]
LEGAL_FILE = {"pl": "informacje-prawne.html", "en": "legal-notice.html", "de": "impressum.html"}
SIG = {
    "pl": "Radca prawny | Polska–Niemcy",
    "en": "Polish Attorney-at-Law | Poland–Germany Business",
    "de": "Rechtsanwalt in Polen (radca prawny) | Polen–Deutschland",
}
SIGNATURE = SIG["en"]   # used on the language-chooser page


def e(s):
    return html.escape(s, quote=True)


def td(value, label):
    """Value or a visible yellow placeholder (and remember it)."""
    if value:
        return e(value)
    if label not in MISSING:
        MISSING.append(label)
    return '<mark class="todo">[…]</mark>'


# ----------------------------------------------------------------------------
# TEXTS — HOME
# ----------------------------------------------------------------------------
T = {
 "pl": {
  "html_lang": "pl",
  "title": "Dymczak Legal — radca prawny | Polska–Niemcy | negocjacje, umowy, compliance",
  "description": "Radca prawny Grzegorz Dymczak. Własna praktyka dla firm: negocjacje i umowy handlowe, procurement, compliance, prawo spółek, prawo cywilne. Obsługa w języku polskim, angielskim i niemieckim.",
  "skip": "Przejdź do treści",
  "menu": "Menu",
  "nav": [("services", "Zakres usług"), ("approach", "Podejście"), ("about", "O mnie"), ("contact", "Kontakt")],
  "lang_label": "Wybór języka",
  "h1": "Radca prawny dla firm działających na linii Polska–Niemcy.",
  "lead": "Prowadzę własną praktykę prawniczą skierowaną do firm. Negocjuję i redaguję umowy handlowe, doradzam w zakresie compliance, prawa spółek i prawa cywilnego — w języku polskim, angielskim i niemieckim.",
  "cred": "<strong>Radca prawny</strong> wpisany na listę radców prawnych, czynnie wykonujący zawód. Własna praktyka; doradztwo w oparciu o prawo polskie.",
  "cta1": "Napisz do mnie", "cta2": "Zakres usług",
  "cap_name": "Grzegorz Dymczak", "cap_role": "Radca prawny · własna praktyka",
  "photo_alt": "Grzegorz Dymczak, radca prawny, w granatowym garniturze",
  "services_h": "Zakres usług",
  "services_p": "Doradzam firmom, które negocjują, kupują, sprzedają i dostarczają — tam, gdzie umowa musi wytrzymać próbę praktyki.",
  "services": [
   ("Negocjacje handlowe", "Przygotowanie i prowadzenie negocjacji z dostawcami, odbiorcami i partnerami: rozpoznanie, czego naprawdę chce druga strona, strategia, pozycje kluczowe, ocena ryzyka i redakcja końcowego tekstu umowy — z perspektywy dostawcy i producenta."),
   ("Umowy zakupowe i łańcuch dostaw", "Ogólne warunki zakupu, umowy ramowe i dostawcze, umowy jakościowe. Odpowiedzialność, gwarancje, kary umowne, limity odpowiedzialności, własność intelektualna i ciągłość dostaw."),
   ("Dostawcy i sieci handlowe", "Warunki handlowe, rabaty i bonusy (w tym naliczane retroaktywnie), kary i potrącenia, przewaga kontraktowa w obrocie produktami rolnymi i spożywczymi oraz związane z tym spory, w tym sądowe."),
   ("Compliance i łańcuch dostaw", "Polityki i kodeksy postępowania, procedury wewnętrzne, szkolenia, weryfikacja kontrahentów i systemy zgłaszania naruszeń (sygnaliści). Wdrażanie wymogów należytej staranności w łańcuchach dostaw, w tym niemieckiej ustawy LkSG — także dla polskich dostawców niemieckich firm."),
   ("Prawo spółek", "Zakładanie spółek od podstaw, w tym zgłoszenia do KRS przez Portal Rejestrów Sądowych (PRS), oraz bieżąca obsługa korporacyjna: powoływanie i odwoływanie członków zarządu i prokurentów, uchwały, absolutorium, zatwierdzanie sprawozdań finansowych, dokumenty na walne zgromadzenia, umowy wspólników i wsparcie przy transakcjach."),
   ("Prawo cywilne i spory", "Roszczenia kontraktowe i odszkodowawcze, windykacja należności, negocjacje ugodowe oraz reprezentacja przed sądami i organami w Polsce."),
  ],
  "approach_h": "Podejście",
  "approach_p": "Cztery rzeczy, które odróżniają moją pracę.",
  "pillars": [
   ("Obie strony stołu", "Negocjowałem i oceniałem umowy z perspektywy dostawcy, producenta oraz sieci handlowej. Wiem, które postanowienia mają realne znaczenie dla każdej ze stron — i gdzie warto się zatrzymać."),
   ("Trzy języki, bez tłumacza", "Negocjacje, korespondencję i dokumentację prowadzę po polsku, angielsku i niemiecku. Umowa nie traci sensu na styku systemów prawnych i kultur biznesowych."),
   ("Prawo, które wspiera biznes", "Szacuję ryzyka prawne razem z biznesowymi i proponuję rozwiązania możliwe do wdrożenia. Nie blokuję biznesu — pomagam działać w granicach prawa."),
   ("Terminowość", "Dotrzymuję terminów i odpowiadam możliwie szybko, bo decyzje biznesowe rzadko mogą czekać."),
  ],
  "band": "W negocjacjach najpierw trzeba wiedzieć, czego naprawdę chce druga strona. Dopiero potem warto negocjować.",
  "band_alt": "Stylizowana grafika: panorama miasta o zmierzchu",
  "industries_h": "Branże",
  "industries_p": "Rynki, na których negocjacje są codziennością.",
  "industries": [
   ("Automotive i dostawcy", "Umowy zakupowe i dostawcze w łańcuchu dostaw motoryzacyjnych — od komponentów metalowych po elektronikę i systemy."),
   ("Intralogistyka i maszyny", "Producenci wózków i systemów magazynowych: umowy z dostawcami, odbiorcami i dystrybutorami."),
   ("Handel i produkty spożywcze", "Relacje dostawca–sieć handlowa: warunki handlowe, rabaty, bonusy i przewaga kontraktowa."),
  ],
  "about_h": "Radca prawny Grzegorz Dymczak",
  "about_photo_alt": "Grzegorz Dymczak — portret",
  "about_p": [
   "Jestem radcą prawnym prowadzącym własną praktykę. Klient pracuje bezpośrednio ze mną, bez pośredników, a ja odpowiadam za całość zlecenia.",
   "Doświadczenie zdobywałem w działach prawnych firm z branży intralogistyki i wózków widłowych ({employers}) oraz w sieci handlowej Kaufland, gdzie pracowałem jako prawnik i compliance officer.",
   "Brałem udział w negocjacjach z międzynarodowymi dostawcami z sektora automotive. Znam typowe punkty sporne w umowach zakupowych i wiem, jak rozmawiać o nich zarówno z perspektywy dostawcy, jak i producenta.",
   "Studiowałem w Niemczech i posługuję się językiem niemieckim na poziomie zawodowym. Doradzałem także firmom z Francji i Włoch.",
   "Praca radcy prawnego w firmie wiązała się z szacowaniem ryzyka. Staram się nie blokować biznesu, tylko go wspierać w granicach prawa: odpowiadam terminowo i możliwie szybko, a rozwiązania opieram na możliwych i potencjalnych ryzykach, także prawnych.",
  ],
  "about_p2_noemp": "Doświadczenie zdobywałem w działach prawnych firm z branży intralogistyki i wózków widłowych oraz w sieci handlowej, gdzie pracowałem jako prawnik i compliance officer.",
  "highlights": [
   "Negocjacje zakupowe obejmujące m.in. części metalowe, półprzewodniki, opony, systemy kamer, systemy bateryjne i rozwiązania dedykowane",
   "Umowy zakupowe i procurement — z perspektywy dostawcy i producenta",
   "Udział w postępowaniach przeciwko sieciom handlowym dotyczących rabatów retrospektywnych",
   "Wdrażanie niemieckiej ustawy o należytej staranności w łańcuchach dostaw (LkSG) w spółkach",
   "Compliance w sieci handlowej — jako prawnik i compliance officer",
   "Spółki: zakładanie od podstaw i rejestracje w KRS przez Portal Rejestrów Sądowych (PRS)",
   "Obsługa korporacyjna: powoływanie i odwoływanie członków zarządu i prokurentów, absolutorium, zatwierdzanie sprawozdań finansowych, dokumenty na walne zgromadzenia",
   "Studia w Niemczech; praca w języku polskim, angielskim i niemieckim",
  ],
  "quals_h": "Uprawnienia zawodowe",
  "quals": [
   "Jestem <strong>radcą prawnym</strong> — zawodu zaufania publicznego regulowanego ustawą z dnia 6 lipca 1982 r. o radcach prawnych oraz Kodeksem Etyki Radcy Prawnego. Jestem wpisany na listę radców prawnych i czynnie wykonuję zawód.",
   "Radca prawny jest uprawniony do udzielania porad i opinii prawnych, sporządzania projektów umów i innych dokumentów prawnych oraz do występowania w imieniu klientów przed sądami i organami w Polsce. Obowiązuje mnie tajemnica zawodowa.",
   "Szczegóły (izba, numer wpisu) znajdziesz w zakładce <a href=\"{legal}\">Informacje prawne</a>.",
  ],
  "contact_h": "Kontakt",
  "contact_p": "Opisz krótko sprawę lub zapytaj o współpracę. Odpowiem, czy mogę pomóc i na jakich zasadach. Współpracuję z firmami zarówno przy pojedynczych sprawach, jak i na stałe.",
  "contact_note": "W pierwszej wiadomości proszę nie przesyłać dokumentów ani informacji objętych tajemnicą. Wiadomość nie tworzy stosunku zlecenia — zasady współpracy ustalamy odrębnie.",
  "lbl_email": "E-mail", "lbl_phone": "Telefon", "lbl_lang": "Języki", "lbl_place": "Miejsce",
  "langs_val": "polski · English · Deutsch",
  "mail_subject": "Zapytanie — Dymczak Legal",
  "mail_btn": "Napisz e-mail",
  "foot_disc": "Treści na stronie mają charakter informacyjny i nie stanowią porady prawnej. Kontakt ze mną nie nawiązuje stosunku zlecenia.",
  "foot_rights": "© {year} Dymczak Legal — Grzegorz Dymczak, radca prawny.",
  "legal_link": "Informacje prawne i polityka prywatności",
  "jsonld_job": "Radca prawny",
 },
 "en": {
  "html_lang": "en",
  "title": "Dymczak Legal — Attorney-at-Law (radca prawny) | Poland–Germany Business",
  "description": "Grzegorz Dymczak, attorney-at-law (radca prawny) admitted in Poland, in independent practice. Business negotiations, procurement and supply agreements, compliance, company law and civil law. Services in Polish, English and German.",
  "skip": "Skip to content",
  "menu": "Menu",
  "nav": [("services", "Areas of practice"), ("approach", "Approach"), ("about", "About"), ("contact", "Contact")],
  "lang_label": "Language",
  "h1": "Polish attorney-at-law for businesses operating between Poland and Germany.",
  "lead": "I run an independent legal practice for businesses. I negotiate and draft commercial agreements and advise on compliance, company law and civil law — in Polish, English and German.",
  "cred": "<strong>Attorney-at-law (radca prawny)</strong> admitted in Poland, entered on the list of attorneys-at-law (radcowie prawni) and in active practice. Independent practice; advice on Polish law.",
  "cta1": "Get in touch", "cta2": "Areas of practice",
  "cap_name": "Grzegorz Dymczak", "cap_role": "Attorney-at-law (radca prawny) · independent practice",
  "photo_alt": "Grzegorz Dymczak, attorney-at-law, in a navy suit",
  "services_h": "Areas of practice",
  "services_p": "I advise companies that negotiate, buy, sell and supply — where the contract has to hold up in practice.",
  "services": [
   ("Commercial negotiations", "Preparing and conducting negotiations with suppliers, customers and partners: understanding what the other side really wants, strategy, key positions, risk assessment and drafting of the final contract — from the perspective of both supplier and manufacturer."),
   ("Procurement and supply chain contracts", "General terms of purchase, framework and supply agreements, quality agreements. Liability, warranties, contractual penalties, limitations of liability, intellectual property and continuity of supply."),
   ("Suppliers and retail chains", "Commercial terms, rebates and bonuses (including those applied retroactively), penalties and set-offs, abuse of contractual advantage in the trade of agricultural and food products, and related disputes, including court proceedings."),
   ("Compliance and supply chain due diligence", "Policies and codes of conduct, internal procedures, training, counterparty due diligence and whistleblowing systems. Implementation of supply chain due diligence requirements, including the German Supply Chain Due Diligence Act (LkSG) — also for Polish suppliers of German companies."),
   ("Company law", "Incorporating companies from scratch, including filings with the National Court Register (KRS) through the Court Registers Portal (PRS), and ongoing corporate support: appointing and removing management board members and commercial proxies (prokura), resolutions, discharge of board members (absolutorium), approval of financial statements, documents for general meetings, shareholder agreements and transaction support."),
   ("Civil law and disputes", "Contractual and damages claims, debt recovery, settlement negotiations and representation before courts and authorities in Poland."),
  ],
  "approach_h": "Approach",
  "approach_p": "Four things that define how I work.",
  "pillars": [
   ("Both sides of the table", "I have negotiated and assessed contracts from the perspective of a supplier, a manufacturer and a retail chain. I know which provisions really matter to each party — and where it is worth holding the line."),
   ("Three languages, no interpreter", "Negotiations, correspondence and documentation in Polish, English and German. A contract does not lose its meaning where legal systems and business cultures meet."),
   ("Law that supports the business", "I assess legal risks together with business risks and propose solutions that can actually be implemented. I do not block the business — I help it operate within the limits of the law."),
   ("On time", "I keep deadlines and respond as quickly as I can, because business decisions rarely can wait."),
  ],
  "band": "In a negotiation, first find out what the other side really wants. Only then start negotiating.",
  "band_alt": "Stylised illustration of a city skyline at dusk",
  "industries_h": "Sectors",
  "industries_p": "Markets where negotiation is part of everyday business.",
  "industries": [
   ("Automotive and suppliers", "Purchase and supply agreements across the automotive supply chain — from metal components to electronics and systems."),
   ("Intralogistics and machinery", "Manufacturers of forklift trucks and warehouse systems: agreements with suppliers, customers and distributors."),
   ("Retail and food products", "Supplier–retailer relations: commercial terms, rebates, bonuses and contractual advantage."),
  ],
  "about_h": "Grzegorz Dymczak, attorney-at-law (radca prawny)",
  "about_photo_alt": "Grzegorz Dymczak — portrait",
  "about_p": [
   "I am an attorney-at-law (radca prawny) admitted in Poland and I run my own practice. Clients work directly with me, without intermediaries, and I am responsible for the matter from start to finish.",
   "I gained my experience in the legal departments of companies in the intralogistics and forklift industry ({employers}) and at the retail chain Kaufland, where I worked as a lawyer and compliance officer.",
   "I have taken part in negotiations with international suppliers in the automotive sector. I know the typical points of contention in procurement contracts and how to address them from the perspective of both supplier and manufacturer.",
   "I studied in Germany and work in German at a professional level. I have also advised companies from France and Italy.",
   "In-house legal work meant assessing risk. I try not to block the business but to support it within the limits of the law: I reply on time and as quickly as I can, and I base solutions on possible and potential risks, including legal ones.",
  ],
  "about_p2_noemp": "I gained my experience in the legal departments of companies in the intralogistics and forklift industry and at a retail chain, where I worked as a lawyer and compliance officer.",
  "highlights": [
   "Procurement negotiations covering, among others, metal parts, semiconductors, tyres, camera systems, battery systems and dedicated solutions",
   "Purchase agreements and procurement — from the perspective of supplier and manufacturer",
   "Participation in proceedings against retail chains concerning retroactive rebates",
   "Implementation of the German Supply Chain Due Diligence Act (LkSG) in companies",
   "Compliance in retail — as a lawyer and compliance officer",
   "Companies: incorporation from scratch and registrations with the National Court Register (KRS) through the Court Registers Portal (PRS)",
   "Corporate support: appointing and removing board members and commercial proxies (prokura), discharge, approval of financial statements, documents for general meetings",
   "Studied in Germany; working languages: Polish, English and German",
  ],
  "quals_h": "Professional qualification",
  "quals": [
   "I am an <strong>attorney-at-law (radca prawny)</strong> admitted in Poland. In Poland this is a regulated profession of public trust, governed by the Act of 6 July 1982 on Legal Counsels (<em>ustawa o radcach prawnych</em>) and the Code of Ethics of Legal Counsels (<em>Kodeks Etyki Radcy Prawnego</em>). I am entered on the list of attorneys-at-law (radcowie prawni) and in active practice.",
   "An attorney-at-law (radca prawny) is authorised to give legal advice and opinions, prepare contracts and other legal documents, and represent clients before courts and authorities in Poland. Professional secrecy applies. The title was conferred in Poland; admission relates to Poland and does not confer admission in other jurisdictions.",
   "Details (chamber, registration number) are on the <a href=\"{legal}\">Legal notice</a> page.",
  ],
  "contact_h": "Contact",
  "contact_p": "Briefly describe your matter or ask about working together. I will tell you whether I can help and on what terms. I work with companies both on one-off matters and on an ongoing basis.",
  "contact_note": "Please do not send documents or confidential information in your first message. Contacting me does not create an engagement — the terms of cooperation are agreed separately.",
  "lbl_email": "Email", "lbl_phone": "Phone", "lbl_lang": "Languages", "lbl_place": "Location",
  "langs_val": "Polski · English · Deutsch",
  "mail_subject": "Enquiry — Dymczak Legal",
  "mail_btn": "Send an email",
  "foot_disc": "The content of this website is for general information only and does not constitute legal advice. Contacting me does not create an attorney–client relationship.",
  "foot_rights": "© {year} Dymczak Legal — Grzegorz Dymczak, attorney-at-law (radca prawny).",
  "legal_link": "Legal notice and privacy policy",
  "jsonld_job": "Attorney-at-law (radca prawny)",
 },
 "de": {
  "html_lang": "de",
  "title": "Dymczak Legal — Rechtsanwalt in Polen (radca prawny) | Polen–Deutschland",
  "description": "Grzegorz Dymczak, radca prawny — in Polen zugelassener Rechtsanwalt in eigener Praxis. Verhandlungen, Einkaufs- und Lieferverträge, Compliance, Gesellschaftsrecht und Zivilrecht. Beratung auf Polnisch, Englisch und Deutsch.",
  "skip": "Zum Inhalt springen",
  "menu": "Menü",
  "nav": [("services", "Tätigkeitsbereiche"), ("approach", "Arbeitsweise"), ("about", "Über mich"), ("contact", "Kontakt")],
  "lang_label": "Sprache",
  "h1": "Rechtsanwalt in Polen für Unternehmen zwischen Polen und Deutschland.",
  "lead": "Ich berate Unternehmen in eigener Praxis: Verhandlung und Gestaltung von Handelsverträgen, Compliance, Gesellschaftsrecht und Zivilrecht — auf Polnisch, Englisch und Deutsch.",
  "cred": "<strong>Radca prawny</strong> — in Polen zugelassener Rechtsanwalt, in die polnische Liste der radcowie prawni eingetragen und aktiv tätig. Eigene Praxis; Beratung zum polnischen Recht.",
  "cta1": "Kontakt aufnehmen", "cta2": "Tätigkeitsbereiche",
  "cap_name": "Grzegorz Dymczak", "cap_role": "Rechtsanwalt in Polen (radca prawny) · eigene Praxis",
  "photo_alt": "Grzegorz Dymczak, Rechtsanwalt in Polen, im dunkelblauen Anzug",
  "services_h": "Tätigkeitsbereiche",
  "services_p": "Ich berate Unternehmen, die verhandeln, einkaufen, verkaufen und liefern — dort, wo der Vertrag in der Praxis bestehen muss.",
  "services": [
   ("Geschäftsverhandlungen", "Vorbereitung und Führung von Verhandlungen mit Lieferanten, Kunden und Partnern: Klärung, was die Gegenseite wirklich will, Strategie, Kernpositionen, Risikobewertung und Ausarbeitung des Vertragstextes — aus der Sicht von Lieferant und Hersteller."),
   ("Einkaufs- und Lieferkettenverträge", "Allgemeine Einkaufsbedingungen, Rahmen- und Liefer­verträge, Qualitätssicherungsvereinbarungen. Haftung, Gewährleistung, Vertragsstrafen, Haftungsbegrenzungen, geistiges Eigentum und Liefersicherheit."),
   ("Lieferanten und Handelsketten", "Handelskonditionen, Rabatte und Boni (auch rückwirkend angewandte), Vertragsstrafen und Aufrechnungen, Ausnutzung vertraglicher Übermacht im Handel mit landwirtschaftlichen und Lebensmittelerzeugnissen sowie damit verbundene Streitigkeiten, auch gerichtliche."),
   ("Compliance und Lieferkettensorgfalt", "Richtlinien und Verhaltenskodizes, interne Verfahren, Schulungen, Prüfung von Geschäftspartnern und Hinweisgebersysteme. Umsetzung der Sorgfaltspflichten in der Lieferkette, einschließlich des Lieferkettensorgfaltspflichtengesetzes (LkSG) — auch für polnische Zulieferer deutscher Unternehmen."),
   ("Gesellschaftsrecht", "Gründung von Gesellschaften von Grund auf, einschließlich der Anmeldungen zum polnischen Gerichtsregister (KRS) über das Gerichtsregisterportal (PRS), sowie laufende gesellschaftsrechtliche Betreuung: Bestellung und Abberufung von Vorstands- bzw. Geschäftsführungsmitgliedern und Prokuristen, Beschlüsse, Entlastung, Genehmigung der Jahresabschlüsse, Unterlagen für Gesellschafter- und Hauptversammlungen, Gesellschaftervereinbarungen und Begleitung von Transaktionen."),
   ("Zivilrecht und Streitigkeiten", "Vertragliche Ansprüche und Schadensersatz, Forderungsbeitreibung, Vergleichsverhandlungen und Vertretung vor Gerichten und Behörden in Polen."),
  ],
  "approach_h": "Arbeitsweise",
  "approach_p": "Vier Dinge, die meine Arbeit prägen.",
  "pillars": [
   ("Beide Seiten des Tisches", "Ich habe Verträge aus der Perspektive von Lieferant, Hersteller und Handelskette verhandelt und bewertet. Ich weiß, welche Regelungen für jede Seite tatsächlich zählen — und wo es sich lohnt, hart zu bleiben."),
   ("Drei Sprachen, ohne Dolmetscher", "Verhandlungen, Korrespondenz und Dokumentation auf Polnisch, Englisch und Deutsch. Ein Vertrag verliert nichts von seiner Bedeutung, wo Rechtssysteme und Geschäftskulturen aufeinandertreffen."),
   ("Recht, das das Geschäft unterstützt", "Ich bewerte rechtliche Risiken gemeinsam mit den wirtschaftlichen und schlage umsetzbare Lösungen vor. Ich blockiere das Geschäft nicht — ich helfe, innerhalb des rechtlichen Rahmens zu handeln."),
   ("Termintreue", "Ich halte Fristen ein und antworte so schnell wie möglich, denn unternehmerische Entscheidungen können selten warten."),
  ],
  "band": "Wer verhandelt, muss zuerst wissen, was die andere Seite wirklich will. Erst dann beginnt die Verhandlung.",
  "band_alt": "Stilisierte Grafik: Stadtsilhouette in der Dämmerung",
  "industries_h": "Branchen",
  "industries_p": "Märkte, in denen Verhandlungen zum Alltag gehören.",
  "industries": [
   ("Automotive und Zulieferer", "Einkaufs- und Lieferverträge in der Automobil-Lieferkette — von Metallkomponenten bis zu Elektronik und Systemen."),
   ("Intralogistik und Maschinenbau", "Hersteller von Gabelstaplern und Lagersystemen: Verträge mit Lieferanten, Kunden und Händlern."),
   ("Handel und Lebensmittel", "Beziehungen zwischen Lieferant und Handelskette: Handelskonditionen, Rabatte, Boni und vertragliche Übermacht."),
  ],
  "about_h": "Grzegorz Dymczak, Rechtsanwalt in Polen (radca prawny)",
  "about_photo_alt": "Grzegorz Dymczak — Porträt",
  "about_p": [
   "Ich bin in Polen zugelassener Rechtsanwalt (radca prawny) und führe eine eigene Praxis. Mandanten arbeiten direkt mit mir, ohne Zwischenstationen, und ich verantworte das Mandat von Anfang bis Ende.",
   "Meine Erfahrung habe ich in den Rechtsabteilungen von Unternehmen der Intralogistik- und Gabelstaplerbranche ({employers}) sowie bei der Handelskette Kaufland gesammelt, wo ich als Jurist und Compliance Officer tätig war.",
   "Ich habe an Verhandlungen mit internationalen Lieferanten der Automobilbranche teilgenommen. Ich kenne die typischen Streitpunkte in Einkaufsverträgen und weiß, wie man sie aus der Sicht von Lieferant und Hersteller anspricht.",
   "Ich habe in Deutschland studiert und arbeite auf professionellem Niveau auf Deutsch. Außerdem habe ich Unternehmen aus Frankreich und Italien beraten.",
   "Die Tätigkeit als Unternehmensjurist war mit der Bewertung von Risiken verbunden. Ich blockiere das Geschäft nicht, sondern unterstütze es im rechtlichen Rahmen: Ich antworte termingerecht und so schnell wie möglich und bewerte Lösungen anhand möglicher und potenzieller Risiken, auch rechtlicher.",
  ],
  "about_p2_noemp": "Meine Erfahrung habe ich in den Rechtsabteilungen von Unternehmen der Intralogistik- und Gabelstaplerbranche sowie bei einer Handelskette gesammelt, wo ich als Jurist und Compliance Officer tätig war.",
  "highlights": [
   "Einkaufsverhandlungen u. a. zu Metallteilen, Halbleitern, Reifen, Kamerasystemen, Batteriesystemen und kundenspezifischen Lösungen",
   "Einkaufsverträge und Procurement — aus der Sicht von Lieferant und Hersteller",
   "Teilnahme an Verfahren gegen Handelsketten zu rückwirkend angewandten Rabatten",
   "Umsetzung des Lieferkettensorgfaltspflichtengesetzes (LkSG) in Unternehmen",
   "Compliance im Handel — als Jurist und Compliance Officer",
   "Gesellschaften: Gründung von Grund auf und Anmeldungen zum polnischen Gerichtsregister (KRS) über das Gerichtsregisterportal (PRS)",
   "Gesellschaftsrechtliche Betreuung: Bestellung und Abberufung von Vorstands-/Geschäftsführungsmitgliedern und Prokuristen, Entlastung, Genehmigung der Jahresabschlüsse, Unterlagen für Hauptversammlungen",
   "Studium in Deutschland; Arbeitssprachen: Polnisch, Englisch und Deutsch",
  ],
  "quals_h": "Berufliche Qualifikation",
  "quals": [
   "Ich bin <strong>radca prawny</strong> — in Polen zugelassener Rechtsanwalt. In Polen ist dies ein gesetzlich geregelter Beruf des öffentlichen Vertrauens (Gesetz vom 6. Juli 1982 über die radcowie prawni, <em>ustawa o radcach prawnych</em>, und Standesregeln <em>Kodeks Etyki Radcy Prawnego</em>). Ich bin in die Liste der radcowie prawni eingetragen und übe den Beruf aktiv aus.",
   "Ein radca prawny ist befugt, Rechtsrat und Gutachten zu erteilen, Verträge und andere Rechtsdokumente zu erstellen und Mandanten vor Gerichten und Behörden in Polen zu vertreten. Es gilt die berufliche Verschwiegenheitspflicht. Die Berufsbezeichnung des Herkunftsstaates lautet „radca prawny“; die Zulassung besteht in Polen und begründet keine Zulassung zur Rechtsanwaltschaft in Deutschland.",
   "Einzelheiten (Kammer, Eintragungsnummer) finden Sie im <a href=\"{legal}\">Impressum</a>.",
  ],
  "contact_h": "Kontakt",
  "contact_p": "Schildern Sie Ihr Anliegen kurz oder fragen Sie nach einer Zusammenarbeit. Ich melde mich, ob und zu welchen Bedingungen ich helfen kann. Ich arbeite für Unternehmen sowohl bei einzelnen Mandaten als auch dauerhaft.",
  "contact_note": "Bitte senden Sie in der ersten Nachricht keine Dokumente oder vertraulichen Informationen. Die Kontaktaufnahme begründet kein Mandatsverhältnis — die Bedingungen der Zusammenarbeit werden gesondert vereinbart.",
  "lbl_email": "E-Mail", "lbl_phone": "Telefon", "lbl_lang": "Sprachen", "lbl_place": "Standort",
  "langs_val": "Polski · English · Deutsch",
  "mail_subject": "Anfrage — Dymczak Legal",
  "mail_btn": "E-Mail schreiben",
  "foot_disc": "Die Inhalte dieser Website dienen der allgemeinen Information und stellen keine Rechtsberatung dar. Die Kontaktaufnahme begründet kein Mandatsverhältnis.",
  "foot_rights": "© {year} Dymczak Legal — Grzegorz Dymczak, Rechtsanwalt in Polen (radca prawny).",
  "legal_link": "Impressum und Datenschutzerklärung",
  "jsonld_job": "Rechtsanwalt in Polen (radca prawny)",
 },
}

EMPLOYERS = "Linde, STILL, Baoli, Dematic, Fenwick"

EDU = {
 "pl": ("Wykształcenie", [
   ("Szkoła Prawa Niemieckiego (SPN) — Uniwersytet Jagielloński", "Ukończona. Zajęcia w języku niemieckim z różnych gałęzi prawa niemieckiego prowadzili profesorowie z Ruprecht-Karls-Universität Heidelberg i Johannes Gutenberg-Universität Mainz."),
   ("Szkoła Prawa Austriackiego — Uniwersytet Jagielloński", "Ukończona. Zajęcia w języku niemieckim z różnych gałęzi prawa austriackiego prowadzili profesorowie z Uniwersytetu Wiedeńskiego."),
   ("Studia w Niemczech — Universität Konstanz", "Studia na Uniwersytecie w Konstancji nad Jeziorem Bodeńskim."),
 ]),
 "en": ("Education", [
   ("German Law School (Szkoła Prawa Niemieckiego, SPN) — Jagiellonian University", "Completed. Classes in German on various branches of German law, taught by professors from Ruprecht-Karls-Universität Heidelberg and Johannes Gutenberg-Universität Mainz."),
   ("Austrian Law School (Szkoła Prawa Austriackiego) — Jagiellonian University", "Completed. Classes in German on various branches of Austrian law, taught by professors from the University of Vienna."),
   ("Studies in Germany — Universität Konstanz", "Studied at the University of Konstanz on Lake Constance."),
 ]),
 "de": ("Ausbildung", [
   ("Schule des deutschen Rechts (Szkoła Prawa Niemieckiego, SPN) — Jagiellonen-Universität Krakau", "Abgeschlossen. Unterricht auf Deutsch zu verschiedenen Gebieten des deutschen Rechts durch Professoren der Ruprecht-Karls-Universität Heidelberg und der Johannes Gutenberg-Universität Mainz."),
   ("Schule des österreichischen Rechts (Szkoła Prawa Austriackiego) — Jagiellonen-Universität Krakau", "Abgeschlossen. Unterricht auf Deutsch zu verschiedenen Gebieten des österreichischen Rechts durch Professoren der Universität Wien."),
   ("Studium in Deutschland — Universität Konstanz", "Studium an der Universität Konstanz am Bodensee."),
 ]),
}


# ----------------------------------------------------------------------------
# TEXTS — LEGAL PAGES
# ----------------------------------------------------------------------------
def legal_html(lang):
    c = CONFIG
    email = e(c["email"])
    nip_row = lambda lbl: (f"<dt>{lbl}</dt><dd>{e(c['nip'])}</dd>" if c["nip"] else "")
    phone_row = lambda lbl: (f"<dt>{lbl}</dt><dd>{e(c['phone'])}</dd>" if c["phone"] else "")
    if lang == "pl":
        return {
         "title": "Informacje prawne i polityka prywatności — Dymczak Legal",
         "h1": "Informacje prawne i polityka prywatności",
         "body": f"""
<h2>1. Usługodawca</h2>
<dl>
 <dt>Nazwa</dt><dd>Dymczak Legal — praktyka radcy prawnego Grzegorza Dymczaka</dd>
 <dt>Adres</dt><dd>{td(c['address'], 'adres (address)')}</dd>
 {nip_row('NIP')}
 <dt>E-mail</dt><dd><a href="mailto:{email}">{email}</a></dd>
 {phone_row('Telefon')}
</dl>
<h2>2. Informacje o zawodzie</h2>
<dl>
 <dt>Tytuł zawodowy</dt><dd>radca prawny</dd>
 <dt>Państwo nadania tytułu</dt><dd>Rzeczpospolita Polska</dd>
 <dt>Samorząd zawodowy</dt><dd>Krajowa Izba Radców Prawnych; wpis na listę radców prawnych prowadzoną przez Okręgową Izbę Radców Prawnych w {td(c['chamber'], 'izba (chamber)')}</dd>
 <dt>Numer wpisu</dt><dd>{td(c['entry_no'], 'numer wpisu (entry_no)')}</dd>
 <dt>Przepisy zawodowe</dt><dd>ustawa z dnia 6 lipca 1982 r. o radcach prawnych; Kodeks Etyki Radcy Prawnego (dostępne m.in. na stronie <a href="https://kirp.pl" rel="noopener">kirp.pl</a>)</dd>
 <dt>Ubezpieczenie odpowiedzialności cywilnej</dt><dd>Obowiązkowe ubezpieczenie odpowiedzialności cywilnej radców prawnych w ramach umowy generalnej zawartej przez Krajową Izbę Radców Prawnych z UNIQA Towarzystwo Ubezpieczeń S.A., ul. Chłodna 51, 00-867 Warszawa (informacje: <a href="{c['insurance_url']}" rel="noopener">oirp.wroclaw.pl</a>)</dd>
</dl>
<h2>3. Charakter treści</h2>
<p>Treści na stronie mają charakter informacyjny i nie stanowią porady prawnej ani oferty w rozumieniu Kodeksu cywilnego. Kontakt za pośrednictwem strony lub poczty elektronicznej nie nawiązuje stosunku zlecenia. Proszę nie przesyłać w pierwszej wiadomości dokumentów ani informacji objętych tajemnicą; zasady współpracy ustalamy odrębnie.</p>
<h2>4. Polityka prywatności</h2>
<h3>Administrator danych</h3>
<p>Administratorem danych osobowych jest Grzegorz Dymczak, prowadzący praktykę pod nazwą Dymczak Legal (dane w punkcie 1). Kontakt w sprawach danych osobowych: <a href="mailto:{email}">{email}</a>.</p>
<h3>Jakie dane przetwarzam i w jakim celu</h3>
<ul>
 <li><strong>Korespondencja</strong> — jeśli napiszesz do mnie, przetwarzam dane z wiadomości (np. imię, adres e-mail, treść), aby odpowiedzieć na zapytanie i — jeśli dojdzie do współpracy — ją zrealizować. Podstawa prawna: art. 6 ust. 1 lit. f RODO (uzasadniony interes: obsługa zapytań) albo lit. b (działania na żądanie osoby przed zawarciem umowy).</li>
 <li><strong>Dane techniczne (logi serwera)</strong> — przy wejściu na stronę dostawca hostingu może przetwarzać m.in. adres IP, datę i czas oraz żądany zasób, w celu zapewnienia działania i bezpieczeństwa usługi. Podstawa prawna: art. 6 ust. 1 lit. f RODO.</li>
</ul>
<p>Podanie danych jest dobrowolne, ale niezbędne, aby odpowiedzieć na zapytanie.</p>
<h3>Odbiorcy danych</h3>
<p>Strona jest hostowana w usłudze GitHub Pages (GitHub, Inc.). Wiadomości e-mail obsługuje dostawca poczty elektronicznej wskazany w ustawieniach mojej skrzynki. Dane klientów podlegają ponadto tajemnicy zawodowej radcy prawnego.</p>
<h3>Przekazywanie danych poza EOG</h3>
<p>Dostawca hostingu ma siedzibę w Stanach Zjednoczonych. W zakresie, w jakim dochodzi do przekazania danych poza Europejski Obszar Gospodarczy, następuje ono na podstawie mechanizmów przewidzianych w RODO (np. decyzja Komisji Europejskiej o odpowiednim stopniu ochrony albo standardowe klauzule umowne).</p>
<h3>Okres przechowywania</h3>
<p>Korespondencję przechowuję przez czas niezbędny do obsługi sprawy, a następnie przez okres wynikający z przepisów lub potrzeby ustalenia, dochodzenia lub obrony roszczeń. Logi serwera są przechowywane według zasad dostawcy hostingu.</p>
<h3>Pliki cookies i zasoby zewnętrzne</h3>
<p>Strona nie używa plików cookies, narzędzi analitycznych ani marketingowych, nie zapisuje danych w przeglądarce odwiedzającego i nie ładuje czcionek, skryptów ani map z zewnętrznych serwerów.</p>
<h3>Twoje prawa</h3>
<p>Masz prawo dostępu do swoich danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przenoszenia (gdy ma zastosowanie) oraz sprzeciwu wobec przetwarzania opartego na art. 6 ust. 1 lit. f RODO. Aby skorzystać z tych praw, napisz na adres <a href="mailto:{email}">{email}</a>. Masz także prawo wniesienia skargi do Prezesa Urzędu Ochrony Danych Osobowych (<a href="https://uodo.gov.pl" rel="noopener">uodo.gov.pl</a>).</p>
<h2>5. Prawa autorskie</h2>
<p>Treści i zdjęcia zamieszczone na stronie są chronione prawem autorskim. Ich wykorzystanie bez zgody jest niedozwolone, poza przypadkami przewidzianymi w przepisach.</p>
""",
        }
    if lang == "en":
        return {
         "title": "Legal notice and privacy policy — Dymczak Legal",
         "h1": "Legal notice and privacy policy",
         "body": f"""
<h2>1. Service provider</h2>
<dl>
 <dt>Name</dt><dd>Dymczak Legal — practice of Grzegorz Dymczak, radca prawny</dd>
 <dt>Address</dt><dd>{td(c['address'], 'adres (address)')}</dd>
 {nip_row('Tax ID (NIP)')}
 <dt>Email</dt><dd><a href="mailto:{email}">{email}</a></dd>
 {phone_row('Phone')}
</dl>
<h2>2. Professional information</h2>
<dl>
 <dt>Professional title</dt><dd>attorney-at-law (radca prawny)</dd>
 <dt>Country where the title was conferred</dt><dd>Republic of Poland</dd>
 <dt>Professional body</dt><dd>National Chamber of Legal Counsels (Krajowa Izba Radców Prawnych); entered on the list of attorneys-at-law (radcowie prawni) kept by the Regional Chamber of Legal Counsels (Okręgowa Izba Radców Prawnych) in {td(c['chamber'], 'izba (chamber)')}</dd>
 <dt>Registration number</dt><dd>{td(c['entry_no'], 'numer wpisu (entry_no)')}</dd>
 <dt>Professional rules</dt><dd>Act of 6 July 1982 on Legal Counsels (<em>ustawa o radcach prawnych</em>); Code of Ethics of Legal Counsels (<em>Kodeks Etyki Radcy Prawnego</em>), available e.g. via <a href="https://kirp.pl" rel="noopener">kirp.pl</a></dd>
 <dt>Professional liability insurance</dt><dd>Compulsory professional liability insurance for legal counsels under the framework agreement concluded by the National Chamber of Legal Counsels with UNIQA Towarzystwo Ubezpieczeń S.A., ul. Chłodna 51, 00-867 Warsaw, Poland (information: <a href="{c['insurance_url']}" rel="noopener">oirp.wroclaw.pl</a>)</dd>
</dl>
<p>The Polish professional title is “radca prawny”; “attorney-at-law” is its common English equivalent. Admission relates to Poland and does not confer admission in other jurisdictions. Advice relates to Polish law.</p>
<h2>3. Nature of the content</h2>
<p>The content of this website is for general information only. It does not constitute legal advice or a binding offer. Contacting me through this website or by email does not create an attorney–client relationship. Please do not send documents or confidential information in your first message; the terms of cooperation are agreed separately.</p>
<h2>4. Privacy policy</h2>
<h3>Controller</h3>
<p>The controller of personal data is Grzegorz Dymczak, operating under the name Dymczak Legal (details in section 1). Contact for data protection matters: <a href="mailto:{email}">{email}</a>.</p>
<h3>What data I process and why</h3>
<ul>
 <li><strong>Correspondence</strong> — if you write to me, I process the data in your message (e.g. name, email address, content) to answer your enquiry and, if we work together, to perform the engagement. Legal basis: Art. 6(1)(f) GDPR (legitimate interest in handling enquiries) or Art. 6(1)(b) GDPR (steps taken at your request prior to entering into a contract).</li>
 <li><strong>Technical data (server logs)</strong> — when you visit the website, the hosting provider may process, among other things, your IP address, date and time and the requested resource in order to operate and secure the service. Legal basis: Art. 6(1)(f) GDPR.</li>
</ul>
<p>Providing data is voluntary, but necessary for me to answer your enquiry.</p>
<h3>Recipients</h3>
<p>The website is hosted on GitHub Pages (GitHub, Inc.). Emails are handled by the email provider used for my mailbox. Client data is additionally protected by professional secrecy.</p>
<h3>Transfers outside the EEA</h3>
<p>The hosting provider is based in the United States. To the extent that data is transferred outside the European Economic Area, this takes place on the basis of mechanisms provided for in the GDPR (e.g. an adequacy decision of the European Commission or standard contractual clauses).</p>
<h3>Retention</h3>
<p>I keep correspondence for as long as needed to handle the matter and afterwards for the period required by law or necessary to establish, pursue or defend legal claims. Server logs are kept in accordance with the hosting provider’s rules.</p>
<h3>Cookies and external resources</h3>
<p>This website does not use cookies, analytics or marketing tools, does not store data in the visitor’s browser and does not load fonts, scripts or maps from external servers.</p>
<h3>Your rights</h3>
<p>You have the right of access, rectification, erasure, restriction of processing, data portability (where applicable) and the right to object to processing based on Art. 6(1)(f) GDPR. To exercise these rights, write to <a href="mailto:{email}">{email}</a>. You also have the right to lodge a complaint with the Polish supervisory authority, the President of the Personal Data Protection Office (<a href="https://uodo.gov.pl" rel="noopener">uodo.gov.pl</a>), or with the authority in your own Member State.</p>
<h2>5. Copyright</h2>
<p>The content and photographs on this website are protected by copyright. Use without permission is not allowed except where provided by law.</p>
""",
        }
    # German
    return {
     "title": "Impressum und Datenschutzerklärung — Dymczak Legal",
     "h1": "Impressum und Datenschutzerklärung",
     "body": f"""
<h2>1. Anbieter (Angaben gemäß § 5 DDG)</h2>
<dl>
 <dt>Name</dt><dd>Dymczak Legal — Praxis von Grzegorz Dymczak, radca prawny</dd>
 <dt>Anschrift</dt><dd>{td(c['address'], 'adres (address)')}</dd>
 {nip_row('Steuernummer (NIP)')}
 <dt>E-Mail</dt><dd><a href="mailto:{email}">{email}</a></dd>
 {phone_row('Telefon')}
</dl>
<h2>2. Berufsrechtliche Angaben</h2>
<dl>
 <dt>Berufsbezeichnung</dt><dd>radca prawny (Rechtsanwalt in Polen)</dd>
 <dt>Staat der Verleihung</dt><dd>Republik Polen</dd>
 <dt>Zuständige Berufsorganisation</dt><dd>Nationale Kammer der radcowie prawni (Krajowa Izba Radców Prawnych); eingetragen in die Liste der radcowie prawni der Regionalkammer (Okręgowa Izba Radców Prawnych) in {td(c['chamber'], 'izba (chamber)')}</dd>
 <dt>Eintragungsnummer</dt><dd>{td(c['entry_no'], 'numer wpisu (entry_no)')}</dd>
 <dt>Berufsrechtliche Regelungen</dt><dd>Gesetz vom 6. Juli 1982 über die radcowie prawni (<em>ustawa o radcach prawnych</em>); Standesregeln der radcowie prawni (<em>Kodeks Etyki Radcy Prawnego</em>), abrufbar z. B. über <a href="https://kirp.pl" rel="noopener">kirp.pl</a></dd>
 <dt>Berufshaftpflichtversicherung</dt><dd>Pflicht-Berufshaftpflichtversicherung der radcowie prawni im Rahmen des Rahmenvertrags der Nationalen Kammer der radcowie prawni mit UNIQA Towarzystwo Ubezpieczeń S.A., ul. Chłodna 51, 00-867 Warschau, Polen (Informationen: <a href="{c['insurance_url']}" rel="noopener">oirp.wroclaw.pl</a>). Räumlicher Geltungsbereich: {td(c['insurance_scope_de'], 'Geltungsbereich Versicherung DE (insurance_scope_de)')}</dd>
</dl>
<p>Die Berufsbezeichnung des Herkunftsstaates lautet „radca prawny“. Die Zulassung besteht in Polen; eine Zulassung zur Rechtsanwaltschaft in Deutschland besteht nicht. Die Beratung bezieht sich auf polnisches Recht.</p>
<h2>3. Art der Inhalte</h2>
<p>Die Inhalte dieser Website dienen der allgemeinen Information. Sie stellen keine Rechtsberatung und kein verbindliches Angebot dar. Die Kontaktaufnahme über die Website oder per E-Mail begründet kein Mandatsverhältnis. Bitte senden Sie in der ersten Nachricht keine Dokumente oder vertraulichen Informationen; die Bedingungen der Zusammenarbeit werden gesondert vereinbart.</p>
<h2>4. Datenschutzerklärung</h2>
<h3>Verantwortlicher</h3>
<p>Verantwortlicher im Sinne der DSGVO ist Grzegorz Dymczak, tätig unter dem Namen Dymczak Legal (Angaben unter Punkt 1). Kontakt in Datenschutzangelegenheiten: <a href="mailto:{email}">{email}</a>.</p>
<h3>Welche Daten ich verarbeite und wozu</h3>
<ul>
 <li><strong>Korrespondenz</strong> — wenn Sie mir schreiben, verarbeite ich die Daten Ihrer Nachricht (z. B. Name, E-Mail-Adresse, Inhalt), um Ihre Anfrage zu beantworten und, falls es zu einer Zusammenarbeit kommt, diese durchzuführen. Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der Bearbeitung von Anfragen) oder Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen auf Ihre Anfrage).</li>
 <li><strong>Technische Daten (Server-Logfiles)</strong> — beim Aufruf der Website kann der Hosting-Anbieter u. a. Ihre IP-Adresse, Datum und Uhrzeit sowie die abgerufene Ressource verarbeiten, um den Betrieb und die Sicherheit des Dienstes zu gewährleisten. Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO.</li>
</ul>
<p>Die Angabe der Daten ist freiwillig, für die Beantwortung Ihrer Anfrage jedoch erforderlich.</p>
<h3>Empfänger</h3>
<p>Die Website wird über GitHub Pages (GitHub, Inc.) gehostet. E-Mails werden vom E-Mail-Anbieter meines Postfachs verarbeitet. Mandantendaten unterliegen zusätzlich der beruflichen Verschwiegenheitspflicht.</p>
<h3>Übermittlung in Drittländer</h3>
<p>Der Hosting-Anbieter hat seinen Sitz in den Vereinigten Staaten. Soweit Daten außerhalb des Europäischen Wirtschaftsraums übermittelt werden, geschieht dies auf Grundlage der in der DSGVO vorgesehenen Mechanismen (z. B. Angemessenheitsbeschluss der Europäischen Kommission oder Standardvertragsklauseln).</p>
<h3>Speicherdauer</h3>
<p>Korrespondenz speichere ich so lange, wie es für die Bearbeitung erforderlich ist, danach für die gesetzlich vorgeschriebene Dauer oder soweit zur Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen erforderlich. Server-Logfiles werden nach den Regeln des Hosting-Anbieters gespeichert.</p>
<h3>Cookies und externe Ressourcen</h3>
<p>Diese Website verwendet keine Cookies, keine Analyse- und keine Marketing-Werkzeuge, speichert keine Daten im Browser der Besucher und lädt keine Schriftarten, Skripte oder Karten von externen Servern.</p>
<h3>Ihre Rechte</h3>
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit (soweit anwendbar) sowie das Recht, der Verarbeitung auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO zu widersprechen. Zur Ausübung dieser Rechte schreiben Sie an <a href="mailto:{email}">{email}</a>. Sie haben außerdem das Recht auf Beschwerde bei der polnischen Aufsichtsbehörde, dem Präsidenten des Amtes für den Schutz personenbezogener Daten (<a href="https://uodo.gov.pl" rel="noopener">uodo.gov.pl</a>), oder bei der Aufsichtsbehörde Ihres Wohnsitzlandes.</p>
<h2>5. Urheberrecht</h2>
<p>Die Inhalte und Fotografien dieser Website sind urheberrechtlich geschützt. Eine Verwendung ohne Zustimmung ist nur im gesetzlich zulässigen Rahmen erlaubt.</p>
""",
    }


# ----------------------------------------------------------------------------
# HTML building blocks
# ----------------------------------------------------------------------------
def page_url(lang, page):
    return f"{BASE}/{lang}/" + ("" if page == "home" else LEGAL_FILE[lang])


def head(lang, page, title, description):
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{page_url(l, page)}">' for l in LANGS
    )
    og_locale = {"pl": "pl_PL", "en": "en_GB", "de": "de_DE"}[lang]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{page_url(lang, page)}">
{alts}
<link rel="alternate" hreflang="x-default" href="{BASE}/">
<meta name="theme-color" content="#0e1a2b">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dymczak Legal">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{page_url(lang, page)}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:image" content="{BASE}/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="../assets/css/style.css">
"""


def header(lang, page):
    t = T[lang]
    prefix = "" if page == "home" else "index.html"
    nav = "".join(f'<li><a href="{prefix}#{k}">{e(v)}</a></li>' for k, v in t["nav"])
    langs = "".join(
        f'<a href="../{l}/{"" if page == "home" else LEGAL_FILE[l]}" hreflang="{l}" lang="{l}"'
        f'{" aria-current=\"true\"" if l == lang else ""}>{l.upper()}</a>'
        for l in LANGS
    )
    home = "./" if page == "home" else "./"
    return f"""<body>
<a class="skip" href="#main">{e(t['skip'])}</a>
<header class="site-header">
 <div class="wrap header-inner">
  <a class="brand" href="{home}" aria-label="Dymczak Legal">
   <span class="brand__name">Dymczak <span>Legal</span></span>
   <span class="brand__sub">{e(SIG[lang])}</span>
  </a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">{e(t['menu'])}</button>
  <nav class="nav" id="site-nav" aria-label="Menu">
   <ul class="nav__list">{nav}</ul>
   <div class="lang" role="group" aria-label="{e(t['lang_label'])}">{langs}</div>
  </nav>
 </div>
</header>
"""


def footer(lang, page):
    t = T[lang]
    links = "".join(
        f'<a href="../{l}/{"" if page == "home" else LEGAL_FILE[l]}" hreflang="{l}" lang="{l}">{n}</a>'
        for l, n in (("pl", "Polski"), ("en", "English"), ("de", "Deutsch"))
    )
    return f"""<footer class="site-footer">
 <div class="wrap footer-grid">
  <div>
   <p class="footer-brand">Dymczak Legal</p>
   <p>{e(SIG[lang])}</p>
   <p>{e(t['foot_disc'])}</p>
   <p>{e(t['foot_rights'].format(year=YEAR))}</p>
  </div>
  <div class="footer-links">
   <a href="{LEGAL_FILE[lang]}">{e(t['legal_link'])}</a>
   {links}
  </div>
 </div>
</footer>
<script src="../assets/js/main.js" defer></script>
</body>
</html>
"""


def home(lang):
    t = T[lang]
    c = CONFIG
    legal = LEGAL_FILE[lang]
    about_p = list(t["about_p"])
    about_p[1] = about_p[1].format(employers=EMPLOYERS) if c["show_employers"] else t["about_p2_noemp"]
    if (ROOT / "assets/img/band-city.webp").exists():
        band_img = f'<img class="band__img" src="../assets/img/band-city.webp" width="2000" height="1125" alt="{e(t["band_alt"])}" loading="lazy">'
    else:
        band_img = f'<img class="band__img" src="../assets/img/skyline.svg" width="1600" height="900" alt="{e(t["band_alt"])}" loading="lazy">'
    mail = f'mailto:{c["email"]}?subject={e(t["mail_subject"].replace(" ", "%20"))}'

    services = "".join(
        f'<article class="service"><span class="service__n">{i:02d}</span><h3>{e(h)}</h3><p>{e(p)}</p></article>'
        for i, (h, p) in enumerate(t["services"], 1)
    )
    pillars = "".join(f'<div class="pillar"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in t["pillars"])
    inds = "".join(f'<div class="industry"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in t["industries"])
    edu = "".join(f"<li><strong>{e(h)}</strong><span>{e(d)}</span></li>" for h, d in EDU[lang][1])
    hl = "".join(f"<li>{e(x)}</li>" for x in t["highlights"])
    quals = "".join(f"<p>{x.format(legal=legal)}</p>" for x in t["quals"])
    paras = "".join(f"<p>{e(p)}</p>" for p in about_p)

    phone_dt = f'<dt>{e(t["lbl_phone"])}</dt><dd><a href="tel:{e(c["phone"].replace(" ", ""))}">{e(c["phone"])}</a></dd>' if c["phone"] else ""
    city_dt = f'<dt>{e(t["lbl_place"])}</dt><dd>{e(c["city"])}</dd>' if c["city"] else ""

    jsonld = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Dymczak Legal",
        "url": f"{BASE}/{lang}/",
        "description": t["description"],
        "knowsLanguage": ["pl", "en", "de"],
        "areaServed": ["PL", "DE"],
        "founder": {"@type": "Person", "name": "Grzegorz Dymczak", "jobTitle": t["jsonld_job"], "knowsLanguage": ["pl", "en", "de"],
                    "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Jagiellonian University"}, {"@type": "CollegeOrUniversity", "name": "University of Konstanz"}]},
        "image": f"{BASE}/assets/img/og.jpg",
    }

    return (
        head(lang, "home", t["title"], t["description"])
        + f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n</head>\n'
        + header(lang, "home")
        + f"""<main id="main">

<section class="hero">
 <div class="wrap hero__grid">
  <div>
   <p class="eyebrow">{e(SIG[lang])}</p>
   <h1>{e(t['h1'])}</h1>
   <p class="hero__lead">{e(t['lead'])}</p>
   <p class="hero__cred">{t['cred']}</p>
   <div class="hero__cta">
    <a class="btn btn--primary" href="#contact">{e(t['cta1'])}</a>
    <a class="btn btn--ghost" href="#services">{e(t['cta2'])}</a>
   </div>
  </div>
  <figure class="portrait">
   <div class="portrait__img"><img src="../assets/img/portrait-suit.webp" width="1000" height="1500" alt="{e(t['photo_alt'])}" fetchpriority="high"></div>
   <figcaption><strong>{e(t['cap_name'])}</strong>{e(t['cap_role'])}</figcaption>
  </figure>
 </div>
</section>

<section class="section" id="services">
 <div class="wrap">
  <div class="section__head"><h2>{e(t['services_h'])}</h2><p>{e(t['services_p'])}</p></div>
  <div class="services">{services}</div>
 </div>
</section>

<section class="section section--alt" id="approach">
 <div class="wrap">
  <div class="section__head"><h2>{e(t['approach_h'])}</h2><p>{e(t['approach_p'])}</p></div>
  <div class="pillars">{pillars}</div>
 </div>
</section>

<section class="band" aria-label="{e(t['band'])}">
 {band_img}
 <div class="wrap"><blockquote>{e(t['band'])}</blockquote></div>
</section>

<section class="section">
 <div class="wrap">
  <div class="section__head"><h2>{e(t['industries_h'])}</h2><p>{e(t['industries_p'])}</p></div>
  <div class="industries">{inds}</div>
 </div>
</section>

<section class="section section--alt" id="about">
 <div class="wrap about">
  <figure class="about__photo"><img src="../assets/img/portrait-shirt.webp" width="800" height="1200" alt="{e(t['about_photo_alt'])}" loading="lazy"></figure>
  <div>
   <p class="eyebrow eyebrow--dark">{e(SIG[lang])}</p>
   <h2>{e(t['about_h'])}</h2>
   {paras}
   <ul class="highlights">{hl}</ul>
   <div class="edu"><h3>{e(EDU[lang][0])}</h3><ul>{edu}</ul></div>
   <div class="quals"><h3>{e(t['quals_h'])}</h3>{quals}</div>
  </div>
 </div>
</section>

<section class="section contact" id="contact">
 <div class="wrap contact__grid">
  <div>
   <h2>{e(t['contact_h'])}</h2>
   <p class="contact__text">{e(t['contact_p'])}</p>
   <p><a class="btn btn--primary" href="{mail}">{e(t['mail_btn'])}</a></p>
   <p class="contact__note">{e(t['contact_note'])}</p>
  </div>
  <div class="card">
   <dl>
    <dt>{e(t['lbl_email'])}</dt><dd><a class="mail" href="mailto:{e(c['email'])}">{e(c['email'])}</a></dd>
    {phone_dt}
    <dt>{e(t['lbl_lang'])}</dt><dd>{e(t['langs_val'])}</dd>
    {city_dt}
   </dl>
  </div>
 </div>
</section>

</main>
"""
        + footer(lang, "home")
    )


def legal_page(lang):
    t = T[lang]
    L = legal_html(lang)
    return (
        head(lang, "legal", L["title"], t["description"])
        + "</head>\n"
        + header(lang, "legal")
        + f"""<main id="main">
<div class="page-head"><div class="wrap"><h1>{e(L['h1'])}</h1></div></div>
<article class="legal"><div class="wrap">{L['body']}</div></article>
</main>
"""
        + footer(lang, "legal")
    )


ROOT_PAGE = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dymczak Legal — Attorney-at-Law (radca prawny) | Poland–Germany Business</title>
<meta name="description" content="Dymczak Legal — radca prawny / attorney-at-law / Rechtsanwalt in Polen. PL · EN · DE.">
<link rel="canonical" href="{BASE}/">
<link rel="alternate" hreflang="pl" href="{BASE}/pl/">
<link rel="alternate" hreflang="en" href="{BASE}/en/">
<link rel="alternate" hreflang="de" href="{BASE}/de/">
<link rel="alternate" hreflang="x-default" href="{BASE}/">
<meta name="theme-color" content="#0e1a2b">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="assets/css/style.css">
<style>
 body{{background:#0e1a2b;color:#fff;min-height:100vh;display:grid;place-items:center;text-align:center}}
 .pick{{padding:40px 20px}}
 .pick h1{{font-size:clamp(2.2rem,6vw,3.6rem);margin-bottom:6px}}
 .pick h1 span{{color:#b38b4d}}
 .pick p{{color:#aab5c4;letter-spacing:.12em;text-transform:uppercase;font-size:12.5px;margin-bottom:34px}}
 .pick nav{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}}
</style>
</head>
<body>
<main class="pick">
 <h1>Dymczak <span>Legal</span></h1>
 <p>{e(SIGNATURE)}</p>
 <nav aria-label="Language">
  <a class="btn btn--primary" href="pl/" hreflang="pl" lang="pl">Polski</a>
  <a class="btn btn--ghost" href="en/" hreflang="en" lang="en">English</a>
  <a class="btn btn--ghost" href="de/" hreflang="de" lang="de">Deutsch</a>
 </nav>
</main>
<script>
 (function () {{
  var l = ((navigator.languages && navigator.languages[0]) || navigator.language || 'en').toLowerCase();
  var t = l.indexOf('pl') === 0 ? 'pl/' : l.indexOf('de') === 0 ? 'de/' : 'en/';
  location.replace(t);
 }})();
</script>
</body>
</html>
"""

NOT_FOUND = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>404 — Dymczak Legal</title>
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/css/style.css">
<style>
 body{{background:#0e1a2b;color:#fff;min-height:100vh;display:grid;place-items:center;text-align:center}}
 .pick{{padding:40px 20px}} .pick h1{{font-size:clamp(3rem,10vw,6rem);margin:0;color:#b38b4d}}
 .pick p{{color:#ccd5e1}} .pick nav{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:26px}}
</style>
</head>
<body>
<main class="pick">
 <h1>404</h1>
 <p>Nie znaleziono strony · Page not found · Seite nicht gefunden</p>
 <nav><a class="btn btn--primary" href="/pl/">Polski</a><a class="btn btn--ghost" href="/en/">English</a><a class="btn btn--ghost" href="/de/">Deutsch</a></nav>
</main>
</body>
</html>
"""


def sitemap():
    urls = []
    for page in ("home", "legal"):
        for l in LANGS:
            alts = "".join(
                f'<xhtml:link rel="alternate" hreflang="{x}" href="{page_url(x, page)}"/>' for x in LANGS
            ) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/"/>'
            pr = "1.0" if page == "home" else "0.3"
            urls.append(f"<url><loc>{page_url(l, page)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority>{alts}</url>")
    urls.insert(0, f"<url><loc>{BASE}/</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="8" fill="#0e1a2b"/><text x="32" y="43" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="30" fill="#b38b4d">DL</text></svg>
"""


def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def main():
    for l in LANGS:
        write(f"{l}/index.html", home(l))
        write(f"{l}/{LEGAL_FILE[l]}", legal_page(l))
    write("index.html", ROOT_PAGE)
    write("404.html", NOT_FOUND)
    write("sitemap.xml", sitemap())
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    write("CNAME", CONFIG["domain"] + "\n")
    write(".nojekyll", "")
    # favicon.svg / favicon.ico / icon-*.png are static files (DL monogram) — not generated here
    print("Built: pl/ en/ de/ index.html 404.html sitemap.xml robots.txt CNAME")
    if MISSING:
        print("\nTO FILL IN (CONFIG in build.py) — shown as yellow [...] on the legal-notice pages:")
        for m in MISSING:
            print("  -", m)


if __name__ == "__main__":
    main()
